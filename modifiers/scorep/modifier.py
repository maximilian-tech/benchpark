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
        "SCOREP_WRAPPER_INSTRUMENTER_WRAPPER",
        "--nocompiler",
        when=True,
        modes=["SCOREP_WRAPPER_INSTRUMENTER_WRAPPER"],
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

    # add_mode(
    #     mode_name="topdown-all",
    #     mode_option="topdown.all",
    #     description="Top-down analysis for Intel CPUs (all levels)",
    # )

    # Write out the metadata file once all variables are resolved
    # register_phase("build_metadata", pipeline="setup", run_after=["make_experiments"])
    #
    # def _build_metadata(self, workspace, app_inst):
    #     """Write the caliper metadata to json"""
    #
    #     cali_metadata = {}
    #
    #     # system metadata
    #     system_metadata = [
    #         "sys_cores_per_node",  # required
    #         "scheduler",  # required
    #         "rocm_arch",
    #         "cuda_arch",
    #         "sys_cores_os_reserved_per_node",
    #         "sys_cores_os_reserved_per_node_list",
    #         "sys_gpus_per_node",
    #         "sys_mem_per_node",
    #         "system_site",
    #     ]
    #     for key in system_metadata:
    #         # Certain keys not required or may not be present
    #         if key in app_inst.variables.keys():
    #             cali_metadata[key] = app_inst.variables[key]
    #
    #     # Load the Caliper metadata variable from ramble.yaml
    #     experiment_metadata = app_inst.expander.expand_var_name(
    #         "caliper_metadata", typed=True, merge_used_stage=False
    #     )
    #     app_inst.expander.flush_used_variable_stage()
    #     # rebuild dictionary with expanded variables
    #     for key, val in experiment_metadata.items():
    #         cali_metadata[key] = app_inst.expander.expand_var(val)
    #
    #     # Write to the Caliper metadata file
    #     cali_metadata_file = self.expander.expand_var(self._caliper_metadata_file)
    #     with open(cali_metadata_file, "w") as f:
    #         f.write(json.dumps(cali_metadata))

    #software_spec("scorep", pkg_spec="scorep")

    required_package("scorep")
