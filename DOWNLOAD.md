Dataset **ISIC 2017: Part 1 - Lesion Segmentation** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/Z/o/T8/27SoDHibjGLxQHr8cCGfVpQTLsCHNZpkkseHG4NORxZawCwUAUCo4IYjoJQO0rW1drysIfrwicrxSEyUgtwZzXgcQmzZg490EXPJvJzCmE7u5XGXbkEPX8PZYqEA.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='ISIC 2017: Part 1 - Lesion Segmentation', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://challenge.isic-archive.com/data/#2017).