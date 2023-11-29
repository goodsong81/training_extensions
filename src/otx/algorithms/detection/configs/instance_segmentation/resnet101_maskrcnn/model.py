"""Model configuration of Resnet101-MaskRCNN model for Instance-Seg Task."""

# Copyright (C) 2022-2023 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

# pylint: disable=invalid-name

_base_ = [
    "../resnet50_maskrcnn/model.py"
]

model = dict(
    pretrained="torchvision://resnet101",
    backbone=dict(
        depth=101,
    ),
)
load_from = "https://download.openmmlab.com/mmdetection/v2.0/mask_rcnn/mask_rcnn_r101_fpn_mstrain-poly_3x_coco/mask_rcnn_r101_fpn_mstrain-poly_3x_coco_20210524_200244-5675c317.pth"
