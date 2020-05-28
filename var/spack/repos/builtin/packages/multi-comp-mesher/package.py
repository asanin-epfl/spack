# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class MultiCompMesher(CMakePackage):
    """Multi component mesh generator using CGAL"""

    homepage = "https://github.com/CNS-OIST/MultiCompMesher"
    url = "https://github.com/CNS-OIST/MultiCompMesher/archive/v1.0.0.tar.gz"
    git = "git@github.com:CNS-OIST/MultiCompMesher.git"

    maintainers = ["WeiliangChenOIST", "tristan0x"]

    version("develop", git=git)
    version(
        '1.0.0',
        sha256='519e3aa4d390a6e6ed6ff1cba2a03e685191e45d00c5c06cf184c55a7c1340ab',
    )

    variant(
        "mt",
        default=True,
        description="Use CGAL concurrency mode with Intel TBB",
    )

    depends_on("boost")
    depends_on("cgal@5:")
    depends_on("intel-tbb", when="+mt")

    def cmake_args(self):
        return [
            "-DACTIVATE_CONCURRENCY:BOOL="
            + ("ON" if "+mt" in self.spec else "OFF")
        ]
