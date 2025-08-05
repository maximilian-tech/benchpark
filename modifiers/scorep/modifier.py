# Copyright 2025 TU Dresden
#
# SPDX-License-Identifier: Apache-2.0

from ramble.modkit import *


def add_mode(mode_name, mode_option, description):
    mode(
        name=mode_name,
        description=description,
    )

    env_var_modification(
        mode_name,
        mode_option,
        when=mode_name.isupper(),
        modes=[mode_name],
    )

class Scorep(BasicModifier):
    """Define a modifier for Score-P"""

    name = "scorep"

    tags("profiler","tracer", "performance-analysis")

    maintainers("maximilian-tech")

    # The filename for metadata forwarded from Benchpark to Score-P
    # _scorep_experiment_directory = "{experiment_run_dir}/{experiment_name}_scorep-output"
    # _scorep_experiment_directory_var = "SCOREP_EXPERIMENT_DIRECTORY"

    _default_mode = "SCOREP_ENABLE_PROFILING"

    add_mode(
        mode_name=_default_mode,
        mode_option="True",
        description="Enable profiling mode",
    )

    env_var_modification(
        "SCOREP_WRAPPER_INSTRUMENTER_FLAGS",
        "--nocompiler",
        when=True,
        modes=["SCOREP_WRAPPER_INSTRUMENTER_FLAGS"],
    )

    def modify_experiment(self, app):
        """If app has built-in Caliper configuration, do not set CALI_CONFIG.
        Config parameters are parsed out into SPOT_CONFIG and OTHER_CALI_CONFIG if the application still requires them.
        """
        return

    add_mode(
        mode_name="SCOREP_CUDA_ENABLE",
        mode_option="yes",
        description="Profile CUDA API functions",
    )

    software_spec("scorep", pkg_spec="scorep")

    required_package("scorep")
