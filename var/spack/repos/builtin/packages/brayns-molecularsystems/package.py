# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class BraynsMolecularsystems(CMakePackage):
    """Brayns use-case plugin for interactive visualization of
     molecular systems"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/viz/Brayns-UC-MolecularSystems"
    git = "ssh://bbpcode.epfl.ch/viz/Brayns-UC-MolecularSystems.git"

    generator = 'Ninja'

    version('develop')
    version('0.1.0', tag='v0.1.0')

    depends_on('cmake@3.1:', type='build')
    depends_on('ninja', type='build')
    depends_on('brayns')
