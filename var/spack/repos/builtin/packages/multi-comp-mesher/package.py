# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class MultiCompMesher(CMakePackage):
    """Multi component mesh generator using CGAL"""

    homepage = "https://github.com/CNS-OIST/MultiCompMesher"
    url = "git@github.com:CNS-OIST/MultiCompMesher.git"

    maintainers = ["WeiliangChenOIST", "tristan0x"]

    version("develop", git=url)

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
