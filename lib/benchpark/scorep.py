# Copyright 2023 Lawrence Livermore National Security, LLC and other
# Benchpark Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import warnings
from benchpark.directives import variant
from benchpark.experiment import ExperimentHelper


class Scorep:
    variant(
        "scorep",
        default="none",
        values=(
            "none",
            "profile",
            "trace",
            "io",
            "memory",
            #"cuda",
            #"hip"
        ),
        multi=True,
        description="scorep mode",
    )

    class Helper(ExperimentHelper):
        def compute_modifiers_section(self):
            modifier_list = []
            if self.spec.satisfies("scorep=none"):
                return modifier_list

            for var in list(self.spec.variants["scorep"]):
                scorep_modifier_modes = {
                    "name":"scorep",
                    "mode":var
                }
                modifier_list.append(scorep_modifier_modes)
            return modifier_list

        def compute_package_section(self):
            # set package versions
            scorep_version = "9.3.0-dev-MR300"

            # get system config options
            # TODO: Get compiler/mpi/package handles directly from system.py
            system_specs = {}
            system_specs["compiler"] = "default-compiler"

            # set package spack specs
            package_specs = {}
            # Set How Score-P shall be installed
            if not self.spec.satisfies("scorep=none"):
                package_specs["scorep"] = {
                    "pkg_spec": f"scorep@{scorep_version}", #ToDo. How do Include CUDA/HIP?
                    #"compiler": system_specs["compiler"],
                }
                pass

            return {
                "packages": {k: v for k, v in package_specs.items() if v},
                "environments": {"scorep": {"packages": list(package_specs.keys())}},
            }

        def get_helper_name_prefix(self):
            if not self.spec.satisfies("scorep=none"):
                scorep_prefix = ["scorep"]
                for var in list(self.spec.variants["scorep"]):
                    if self.spec.satisfies(f"scorep={var}"):
                        scorep_prefix.append(var.replace("-", "_"))
                return "_".join(scorep_prefix)
            else:
                return "scorep_none"

        def get_spack_variants(self):
            return "~scorep" if self.spec.satisfies("scorep=none") else "+scorep"

        def compute_variables_section(self):
            """Add Caliper metadata variables for the ramble.yaml"""
            if self.spec.satisfies("scorep=none"):
                return {}

            metadata_dict = {
                "application_name": "{application_name}",
                "experiment_name": "{experiment_name}",
                "n_nodes": "{n_nodes}",
                "n_ranks": "{n_ranks}",
                "n_threads_per_proc": "{n_threads_per_proc}",
                "n_resources": "{n_resources}",
                "process_problem_size": "{process_problem_size}",
                "total_problem_size": "{total_problem_size}",
            }
            # parse the spec for more metadata
            for i, variant_spec in enumerate(str.split(str(self.spec.variants))):
                values = variant_spec.split("=")
                if len(values) == 1:
                    if i == 0:
                        metadata_dict["benchpark_spec"] = values
                    elif values[0] == "'":
                        pass
                elif len(values) == 2:
                    metadata_dict[values[0]] = values[1]
                else:
                    warnings.warn(
                        "Possible incorrect values sent to Score-P as metadata"
                    )
            return {"scorep_metadata": metadata_dict}

