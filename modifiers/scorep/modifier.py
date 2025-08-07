# Copyright 2025 TU Dresden
#
# SPDX-License-Identifier: Apache-2.0

from ramble.modkit import *


def add_mode(mode_name, variable_name, mode_option, description):
    mode(
        name=mode_name,
        description=description,
    )

    env_var_modification(
        variable_name,
        mode_option,
        when=True,
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

    #_default_mode = "SCOREP_ENABLE_PROFILING"

    add_mode(
        mode_name="profile",
        variable_name="SCOREP_ENABLE_PROFILING",
        mode_option="True",
        description="Enable profiling mode",
    )

    add_mode(
        mode_name="trace",
        variable_name="SCOREP_ENABLE_TRACING",
        mode_option="True",
        description="Enable io mode",
    )

    add_mode(
        mode_name="io",
        variable_name="SCOREP_IO_POSIX",
        mode_option="True",
        description="Enable io mode",
    )

    add_mode(
        mode_name="memory",
        variable_name="SCOREP_MEMORY_RECORDING",
        mode_option="True",
        description="Enable io mode",
    )

    # add_mode(
    #     mode_name="cuda",
    #     variable_name="SCOREP_CUDA_ENABLE",
    #     mode_option="True",
    #     description="Enable io mode",
    # )
    
    # add_mode(
    #     mode_name="hip",
    #     variable_name="SCOREP_HIP_ENABLE",
    #     mode_option="True",
    #     description="Enable io mode",        
    # )    

    software_spec("scorep", pkg_spec="scorep")

    required_package("scorep")
