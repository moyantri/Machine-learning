import os
import torch

import albumentations
import pretrainedmodels

import numpy as np
import pandas as pd
import torch.nn as nn

from apex import amp
from sklearn import metrics
from torch.nn import functional as F

from wtfml.data_loaders.image import ClassificationLoader
from wtfml.engine import Engine
from wtfml.utils import EarlyStopping
# logger, engine, utils, data loaders

class SEResNext50_32x4d(nn.Module):
    def __init__(self, pretrained="imagenet"):
        super(SEResNext50_32x4d, self).__init__()
        self.model = pretrainedmodels.__dict__[
            "se_resnext50_32x4d"
        ](pretrained=pretrained)
        self.out = nn.Linear(2048, 1)
    
    def forward(self, image, targets):
        bs, _, _, _ = image.shape
        x = self.model.features(image)
        x = F.adaptive_avg_pool2d(x, 1)
        x = x.reshape(bs, -1)
        out = self.out(x)
        loss = nn.BCEWithLogitsLoss()(
            out, targets.reshape(-1, 1).type_as(out)
        )
        return out, loss

