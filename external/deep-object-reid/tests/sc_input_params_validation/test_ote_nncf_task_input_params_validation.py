# Copyright (C) 2021-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
#

import pytest
from otx.api.configuration.configurable_parameters import ConfigurableParameters
from otx.api.entities.datasets import DatasetEntity
from otx.api.entities.label_schema import LabelSchemaEntity
from otx.api.entities.model import ModelConfiguration, ModelEntity
from otx.api.test_suite.e2e_test_system import e2e_pytest_unit
from otx.api.tests.parameters_validation.validation_helper import (
    check_value_error_exception_raised,
)
from otx.api.usecases.tasks.interfaces.export_interface import ExportType
from otx.api.usecases.tasks.interfaces.optimization_interface import OptimizationType

from torchreid_tasks.nncf_task import OTXClassificationNNCFTask


class MockNNCFTask(OTXClassificationNNCFTask):
    def __init__(self):
        pass


class TestNNCFTaskInputParamsValidation:
    @staticmethod
    def model():
        model_configuration = ModelConfiguration(
            configurable_parameters=ConfigurableParameters(
                header="header", description="description"
            ),
            label_schema=LabelSchemaEntity(),
        )
        return ModelEntity(
            train_dataset=DatasetEntity(), configuration=model_configuration
        )

    @e2e_pytest_unit
    def test_ote_nncf_classification_task_init_params_validation(self):
        """
        <b>Description:</b>
        Check OTXClassificationNNCFTask object initialization parameters validation

        <b>Input data:</b>
        OTXClassificationNNCFTask object initialization parameters with unexpected type

        <b>Expected results:</b>
        Test passes if ValueError exception is raised when unexpected type object is specified as
        OTXClassificationNNCFTask object initialization parameter
        """
        with pytest.raises(ValueError):
            OTXClassificationNNCFTask(task_environment="unexpected string")  # type: ignore

    @e2e_pytest_unit
    def test_ote_nncf_classification_task_optimize_params_validation(self):
        """
        <b>Description:</b>
        Check OTXClassificationNNCFTask object "optimize" method input parameters validation

        <b>Input data:</b>
        OTXClassificationNNCFTask object. "optimize" method unexpected-type input parameters

        <b>Expected results:</b>
        Test passes if ValueError exception is raised when unexpected type object is specified as
        input parameter for "optimize" method
        """
        task = MockNNCFTask()
        correct_values_dict = {
            "optimization_type": OptimizationType.NNCF,
            "dataset": DatasetEntity(),
            "output_model": self.model(),
        }
        unexpected_str = "unexpected string"
        unexpected_values = [
            # Unexpected string is specified as "optimization_type" parameter
            ("optimization_type", unexpected_str),
            # Unexpected string is specified as "dataset" parameter
            ("dataset", unexpected_str),
            # Unexpected string is specified as "output_model" parameter
            ("output_model", unexpected_str),
            # Unexpected string is specified as "optimization_parameters" parameter
            ("optimization_parameters", unexpected_str),
        ]
        check_value_error_exception_raised(
            correct_parameters=correct_values_dict,
            unexpected_values=unexpected_values,
            class_or_function=task.optimize,
        )

    @e2e_pytest_unit
    def test_ote_nncf_classification_task_save_model_params_validation(self):
        """
        <b>Description:</b>
        Check OTXClassificationNNCFTask object "save_model" method input parameters validation

        <b>Input data:</b>
        OTXClassificationNNCFTask object, "output_model" non-ModelEntity object

        <b>Expected results:</b>
        Test passes if ValueError exception is raised when unexpected type object is specified as
        input parameter for "save_model" method
        """
        task = MockNNCFTask()
        with pytest.raises(ValueError):
            task.save_model(output_model="unexpected string")  # type: ignore

    @e2e_pytest_unit
    def test_ote_nncf_classification_task_export_params_validation(self):
        """
        <b>Description:</b>
        Check OTXClassificationNNCFTask object "export" method input parameters validation

        <b>Input data:</b>
        OTXClassificationNNCFTask object. "export" method unexpected-type input parameters

        <b>Expected results:</b>
        Test passes if ValueError exception is raised when unexpected type object is specified as
        input parameter for "export" method
        """
        task = MockNNCFTask()
        correct_values_dict = {
            "export_type": ExportType.OPENVINO,
            "output_model": self.model(),
        }
        unexpected_str = "unexpected string"
        unexpected_values = [
            # Unexpected string is specified as "export_type" parameter
            ("export_type", unexpected_str),
            # Unexpected string is specified as "output_model" parameter
            ("output_model", unexpected_str),
        ]
        check_value_error_exception_raised(
            correct_parameters=correct_values_dict,
            unexpected_values=unexpected_values,
            class_or_function=task.export,
        )
