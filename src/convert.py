import supervisely as sly
import os
from collections import defaultdict
from dataset_tools.convert import unpack_if_archive
import src.settings as s
from urllib.parse import unquote, urlparse
from supervisely.io.fs import get_file_name, get_file_size
import shutil

from tqdm import tqdm

def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:        
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path
    
def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count
    
def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    batch_size = 50
    train_images_path = os.path.join("Task1","ISIC-2017_Training_Data","ISIC-2017_Training_Data")
    train_anns_path = os.path.join("Task1","ISIC-2017_Training_Part1_GroundTruth","ISIC-2017_Training_Part1_GroundTruth")
    valid_images_path = os.path.join("Task1","ISIC-2017_Validation_Data","ISIC-2017_Validation_Data")
    valid_anns_path = os.path.join("Task1","ISIC-2017_Validation_Part1_GroundTruth","ISIC-2017_Validation_Part1_GroundTruth")
    test_images_path = os.path.join("Task1","ISIC-2017_Test_v2_Data","ISIC-2017_Test_v2_Data")
    test_anns_path = os.path.join("Task1","ISIC-2017_Test_v2_Part1_GroundTruth","ISIC-2017_Test_v2_Part1_GroundTruth")
    test_meta_path = os.path.join("Task1","ISIC-2017_Test_v2_Data","ISIC-2017_Test_v2_Data","ISIC-2017_Test_v2_Data_metadata.csv")
    train_meta_path = os.path.join("Task1","ISIC-2017_Training_Data","ISIC-2017_Training_Data","ISIC-2017_Training_Data_metadata.csv")
    valid_meta_path = os.path.join("Task1","ISIC-2017_Validation_Data","ISIC-2017_Validation_Data","ISIC-2017_Validation_Data_metadata.csv")
    ds_name_to_data = {
        "train": (train_images_path, train_anns_path, train_meta_path),
        "valid": (valid_images_path, valid_anns_path, valid_meta_path),
        "test": (test_images_path, test_anns_path, test_meta_path),
    }


    def create_ann(image_path):
        labels = []
        tags = []
        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]
        image_id = get_file_name(image_path)
        tag = sly.Tag(tag_age, img2meta[image_id][0])
        tags.append(tag)
        tag = sly.Tag(tag_sex, img2meta[image_id][1])
        tags.append(tag)
        ann_name = image_id + "_segmentation.png"
        ann_path = os.path.join(anns_path, ann_name) 
        mask_np = sly.imaging.image.read(ann_path)[:, :, 0]
        obj_mask = mask_np == 255
        geometry = sly.Bitmap(obj_mask)
        label = sly.Label(geometry,lesion)

        return sly.Annotation(img_size=(img_height, img_wight), labels=[label], img_tags=tags)


    lesion = sly.ObjClass("lesion", sly.Bitmap)
    tag_age = sly.TagMeta("age_approximate", sly.TagValueType.ANY_STRING)
    tag_sex = sly.TagMeta("sex", sly.TagValueType.ANY_STRING)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=[lesion], tag_metas=[tag_age,tag_sex])
    api.project.update_meta(project.id, meta.to_json())

    for ds_name, ds_data in ds_name_to_data.items():
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        images_path, anns_path, meta_path = ds_data
        img2meta = defaultdict()
        with open(meta_path) as file:
            csvreader = csv.reader(file)
            for idx, row in enumerate(csvreader):
                if idx == 0:
                    continue
                img2meta[row[0]] = row[1],row[2]

        images_names = [name for name in os.listdir(images_path) if "super" not in name and "csv" not in name]
        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

        for img_names_batch in sly.batched(images_names, batch_size=batch_size):
            images_pathes_batch = [
                os.path.join(images_path, image_name) for image_name in img_names_batch
            ]

            img_infos = api.image.upload_paths(dataset.id, img_names_batch, images_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns_batch = [create_ann(image_path) for image_path in images_pathes_batch]
            api.annotation.upload_anns(img_ids, anns_batch)

            progress.iters_done_report(len(img_names_batch))

    return project
