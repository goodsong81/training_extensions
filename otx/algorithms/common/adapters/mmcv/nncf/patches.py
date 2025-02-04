"""Patch mmcv and mpa stuff."""
# Copyright (C) 2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
#

from copy import deepcopy

from otx.algorithms.common.adapters.nncf import (
    NNCF_PATCHER,
    is_nncf_enabled,
    no_nncf_trace_wrapper,
)

if is_nncf_enabled():
    from nncf.torch.nncf_network import NNCFNetwork

    # pylint: disable-next=ungrouped-imports
    from otx.algorithms.common.adapters.nncf.patches import nncf_train_step

    # add wrapper train_step method
    NNCFNetwork.train_step = nncf_train_step


# pylint: disable-next=unused-argument,invalid-name
def _evaluation_wrapper(self, fn, runner, *args, **kwargs):
    # TODO: move this patch to upper level (mmcv)
    # as this is not only nncf required feature.
    # one example is ReduceLROnPlateauLrUpdaterHook
    out = fn(runner, *args, **kwargs)
    setattr(runner, "all_metrics", deepcopy(runner.log_buffer.output))
    return out


NNCF_PATCHER.patch("mmcv.runner.EvalHook.evaluate", _evaluation_wrapper)
NNCF_PATCHER.patch("otx.mpa.modules.hooks.eval_hook.CustomEvalHook.evaluate", _evaluation_wrapper)

NNCF_PATCHER.patch(
    "otx.mpa.modules.hooks.recording_forward_hooks.FeatureVectorHook.func",
    no_nncf_trace_wrapper,
)
NNCF_PATCHER.patch(
    "otx.mpa.modules.hooks.recording_forward_hooks.ActivationMapHook.func",
    no_nncf_trace_wrapper,
)
NNCF_PATCHER.patch(
    "otx.mpa.modules.hooks.recording_forward_hooks.ReciproCAMHook.func",
    no_nncf_trace_wrapper,
)
