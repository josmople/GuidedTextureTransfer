import torch
import torch.utils.data as data

import torchvision.transforms as T

from glob import glob as _glob
from PIL import Image


class ValueDataset(data.Dataset):

    def __init__(self, values, transform=None):
        self.values = values
        self.transform = transform

    def __len__(self):
        return len(self.values)

    def __getitem__(self, idx):
        value = self.values[idx]
        if self.transform is None:
            return value
        return self.transform(value)


class ZipDataset(data.Dataset):

    def __init__(self, dataset, *others, zip_transform=None):
        assert all([len(dataset) == len(other) for other in others]), "Sizes of all dataset must be the same"

        self.dataset = dataset
        self.others = others
        self.zip_transform = zip_transform

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        array = [other[idx] for other in self.others]
        array.insert(0, self.dataset[idx])
        if self.zip_transform is None:
            return tuple(array)
        return self.zip_transform(*array)

class ImageDataset(ValueDataset):

    @staticmethod
    def glob(pathname, *, recursive=False, key=None, reverse=False):
        return sorted(_glob(pathname, recursive=recursive), key=key, reverse=reverse)

    def __init__(self, pathtemplate, transform=None, *, recursive=False, key=None, reverse=False):
        imgpaths = ImageDataset.glob(pathtemplate, recursive=recursive, key=key, reverse=reverse)
        super().__init__(imgpaths, T.Compose([
            T.Lambda(lambda path: Image.open(path)),
            transform or (lambda x: x)
        ]))
