The **ISIC 2017: Part 1 - Lesion Segmentation** dataset is specifically designed for a semantic segmentation task focused on dermatology. Comprising 2750 images, each image in the dataset is associated with 1 single class, namely *lesion*. The primary objective of this dataset is to challenge participants to generate automated predictions of lesion segmentation boundaries from dermoscopic images. Each image is accompanied by expert manual tracings of lesion boundaries represented as binary masks, providing a ground truth for the segmentation task. This dataset serves as a valuable resource for advancing the development and evaluation of algorithms in the field of dermatological image analysis.

## About ISIC 2017 Challenge

The International Skin Imaging Collaboration (ISIC) has begun to aggregate a large-scale publicly accessible dataset of dermoscopy images. Currently, the dataset houses more than 20,000 images from leading clinical centers internationally, acquired from a variety of devices used at each center. The ISIC dataset was the foundation for the first public benchmark challenge on dermoscopic image analysis in 2016. 

The goal of the challenge is to help participants develop image analysis tools to enable the automated diagnosis of melanoma from dermoscopic images. Image analysis of skin lesions is composed of 3 parts:

- Part 1: Lesion Segmentation (current)
- Part 2: Detection and Localization of Visual Dermoscopic Features/Patterns
- Part 3: Disease Classification [(Available on DatasetNinja)]()

For each, data consisted of images and corresponding ground truth annotations, split into training (n=2000), validation (n=150), and holdout test (n=600) datasets. Predictions could be submitted on validation and test datasets. The validation submissions provided instantaneous feedback in the form of performance evaluations, as well as ranking in comparison to other participants. Test submissions only provided feedback after the submission deadline.

## About Lesion Segmentation

Participants were asked to submit automated predictions of lesion segmentations from dermoscopic images in the form of binary masks. Lesion segmentation training data included the original image, paired with the expert manual tracing of the lesion boundaries also in the form of a binary mask, where pixel values of 255 were considered inside the area of the lesion, and pixel values of 0 were outside.

<img width="750" alt="isic2017-pat1-preview" src="https://github.com/dataset-ninja/isic-2017-part-1/assets/123257559/5b2acc80-6faa-4793-b111-3c1763acb790">

<span style="font-size: smaller; font-style: italic;">Images from “Part 1: Lesion Segmentation.” Top: Original images. Bottom: Segmentation masks.</span>
