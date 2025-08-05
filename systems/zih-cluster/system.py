# Copyright 2023 TU Dresden
#
# SPDX-License-Identifier: Apache-2.0


from benchpark.directives import variant, maintainers
from benchpark.system import System
from benchpark.openmpsystem import OpenMPSystem
from benchpark.paths import hardware_descriptions


class ZihCluster(System):

    maintainers("maximilian-tech")

    id_to_resources = {
        "barnard": {
            "sys_cores_per_node": 104,
            "sys_cores_os_reserved_per_node": 0,  # No core or thread reservation
            "sys_cores_os_reserved_per_node_list": None,
            "system_site": "zih",
            "hardware_key": str(hardware_descriptions)
            + "/Eviden-sapphirerapids-Infiniband/hardware_description.yaml",
        },
        "romeo": {
            "sys_cores_per_node": 128,
            "sys_cores_os_reserved_per_node": 0,  # No core or thread reservation
            "sys_cores_os_reserved_per_node_list": None,
            "system_site": "zih",
            "hardware_key": str(hardware_descriptions)
            + "/NEC-zen2-Infiniband/hardware_description.yaml",
        },
    }

    variant(
        "cluster",
        default="barnard",
        values=("barnard", "romeo"),
        description="Which cluster to run on",
    )

    variant(
        "compiler",
        default="gcc",
        values=(["gcc"]),
        description="Which compiler to use",
    )

    def __init__(self, spec):
        super().__init__(spec)
        self.programming_models = [OpenMPSystem()]

        self.scheduler = "slurm"
        attrs = self.id_to_resources.get(self.spec.variants["cluster"][0])
        print(f"{self.spec.variants["cluster"]=}")
        print(f"{attrs=}")
        for k, v in attrs.items():
            setattr(self, k, v)
    
    
    def _is(self, cluster):
        if self.spec.variants["cluster"][0] == cluster:
            return True
        return False
    

    @staticmethod
    def _romeo_packages() -> dict:
        selections = {
            "packages": {
                "pkgconf": {
                    "externals": [ {"spec": "pkgconf@2.2.0 arch=linux-rhel9-zen2", "modules": ["pkgconf/2.2.0"]} ],
                    "buildable": False,
                },
                "binutils": {
                    "externals": [ {"spec": "binutils@2.42.0%gcc@13.3.0 arch=linux-rhel9-zen2", "modules": ["binutils/2.42"]} ],
                    "buildable": False,
                },
                "fftw": {
                    "externals": [ {"spec": "fftw@3.3.10 arch=linux-rhel9-zen2", "modules": ["FFTW/3.3.10"]} ],
                    "buildable": False,
                },
                "cmake": {
                    "externals": [{"spec": "cmake@3.29.3 arch=linux-rhel9-zen2", "modules": ["CMake/3.29.3"]} ],
                    "buildable": False,
                },
                "python": {
                    "externals": [{"spec": "python@3.12.3 arch=linux-rhel9-zen2","modules": ["Python/3.12.3"]}],
                    #"buildable": False,
                },
                "hwloc": {
                    "externals": [{"spec": "hwloc@2.10.0 arch=linux-rhel9-zen2", "modules": ["hwloc/2.10.0"]}],
                    "buildable": False,
                },
                "mpi": {
                    "buildable": False,
                    "externals": [{"spec": "openmpi@5.0.3%gcc@13.3.0 arch=linux-rhel9-zen2","modules": ["OpenMPI/5.0.3"],}],
                },
                "tar": {
                    "externals": [{"spec": "tar@1.34", "prefix": "/usr"}],
                    "buildable": False,
                },
                "autoconf": {
                    "externals": [{"spec": "autoconf@2.69", "prefix": "/usr"}],
                    "buildable": False,
                },
                "gmake": {
                    "externals": [{"spec": "gmake@4.3.0", "prefix": "/usr"}],
                    "buildable": False,
                },
            }
        }

        return selections
        

    @staticmethod
    def _barnard_packages() -> dict:
        selections = {
            "packages": {
                "pkgconf": {
                    "externals": [ {"spec": "pkgconf@2.2.0 arch=linux-rhel8-sapphirerapids", "modules": ["pkgconf/2.2.0"]} ],
                    "buildable": False,
                },
                "binutils": {
                    "externals": [ {"spec": "binutils@2.42.0%gcc@13.3.0 arch=linux-rhel8-sapphirerapids", "modules": ["binutils/2.42"]} ],
                    "buildable": False,
                },
                "fftw": {
                    "externals": [ {"spec": "fftw@3.3.10 arch=linux-rhel8-sapphirerapids", "modules": ["FFTW/3.3.10"]} ],
                    "buildable": False,
                },
                "cmake": {
                    "externals": [{"spec": "cmake@3.29.3 arch=linux-rhel8-sapphirerapids", "modules": ["CMake/3.29.3"]} ],
                    "buildable": False,
                },
                "python": {
                    "externals": [{"spec": "python@3.12.3 arch=linux-rhel8-sapphirerapids","modules": ["Python/3.12.3"]}],
                    #"buildable": False,
                },
                "hwloc": {
                    "externals": [{"spec": "hwloc@2.10.0 arch=linux-rhel8-sapphirerapids", "modules": ["hwloc/2.10.0"]}],
                    "buildable": False,
                },
                "mpi": {
                    "buildable": False,
                    "externals": [{"spec": "openmpi@5.0.3%gcc@13.3.0 arch=linux-rhel8-sapphirerapids", "modules": ["OpenMPI/5.0.3"],}],
                },
                "tar": {
                    "externals": [{"spec": "tar@1.30 arch=linux-rhel8-sapphirerapids", "prefix": "/usr"}],
                    "buildable": False,
                },
                "autoconf": {
                    "externals": [{"spec": "autoconf@2.69 arch=linux-rhel8-sapphirerapids", "prefix": "/usr"}],
                    "buildable": False,
                },
                "gmake": {
                    "externals": [{"spec": "gmake@4.2.1 arch=linux-rhel8-sapphirerapids", "prefix": "/usr"}],
                    "buildable": False,
                },
            }
        }

        return selections

    def compute_packages_section(self):
        if self._is("barnard"):
            selections = self._barnard_packages()
        elif self._is("romeo") in self.spec.variants:
            selections = self._romeo_packages()
        else:
           print(f"{self.spec.variants=}",flush=True)
           raise RuntimeError("No cluster match!!")
        return selections

    def compute_compilers_section(self):
        selections = {}
        if self._is("barnard"):
            selections = {
                "compilers": [
                    {
                        "compiler": {
                            "spec": "gcc@13.3.0",
                            "paths": {
                                "cc": "/software/rapids/r25.06/GCCcore/13.3.0/bin/gcc",
                                "cxx": "/software/rapids/r25.06/GCCcore/13.3.0/bin/g++",
                                "f77": "/software/rapids/r25.06/GCCcore/13.3.0/bin/gfortran",
                                "fc": "/software/rapids/r25.06/GCCcore/13.3.0/bin/gfortran",
                            },
                            "flags": {},
                            "operating_system": "rhel8",
                            "target": "x86_64",
                            "modules": ["release/25.06","gompi/2024a","Python/3.12.3","FFTW/3.3.10","CMake/3.29.3", "hwloc/2.10.0"],
                            "environment": {},
                            "extra_rpaths": [],
                        }
                    }
                ]
            }
        
        if self._is("romeo"):
            selections = {
                "compilers": [
                    {
                        "compiler": {
                            "spec": "gcc@13.3.0",
                            "paths": {
                                "cc": "/software/rome/r25.06/GCCcore/13.3.0/bin/gcc",
                                "cxx": "/software/rome/r25.06/GCCcore/13.3.0/bin/g++",
                                "f77": "/software/rome/r25.06/GCCcore/13.3.0/bin/gfortran",
                                "fc": "/software/rome/r25.06/GCCcore/13.3.0/bin/gfortran",
                            },
                            "flags": {},
                            "operating_system": "rhel9",
                            "target": "x86_64",
                            "modules": ["release/25.06","gompi/2024a","Python/3.12.3","FFTW/3.3.10","CMake/3.29.3", "hwloc/2.10.0"],
                            "environment": {},
                            "extra_rpaths": [],
                        }
                    }
                ]
            }
        
        return selections

    def compute_software_section(self):
        return {
            "software": {
                "packages": {
                    "default-compiler": {"pkg_spec": self.spec.variants["compiler"][0]},
                    "default-mpi": {"pkg_spec": "opennmpi"},
                    "compiler-gcc": {"pkg_spec": "gcc"},
                    #"blas": {"pkg_spec": "intel-oneapi-mkl"},
                    #"lapack": {"pkg_spec": "intel-oneapi-mkl"},
                    "mpi-gcc": {"pkg_spec": "openmpi"},
                }
            }
        }
