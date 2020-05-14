# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LibsonataReport(CMakePackage):
    """
    `libsonata` provides C++ API for reading SONATA Nodes / Edges

    See also:
    https://github.com/AllenInstitute/sonata/blob/master/docs/SONATA_DEVELOPER_GUIDE.md
    """
    homepage = "https://github.com/BlueBrain/libsonata"
    # Using my fork for testing
    git = "https://github.com/BlueBrain/libsonata.git"

    version('reports', branch='reports', preferred=True, submodules=True, get_full_repo=True)
    version('develop', branch='master', submodules=False, get_full_repo=True)
    version('0.1.2', tag='v0.1.2', submodules=False, get_full_repo=True)
    version('0.1.0', tag='v0.1.0', submodules=False, get_full_repo=True)
    version('0.0.3', tag='v0.0.3', submodules=False)

    variant('mpi', default=True, description="Enable MPI backend")

    depends_on('cmake@3.3:', type='build')
    depends_on('py-setuptools-scm', type='build', when='@0.1:')
    depends_on('fmt@4.0:')
    depends_on('highfive+mpi', when='+mpi')
    depends_on('highfive~mpi', when='~mpi')
    depends_on('mpi', when='+mpi')
    depends_on('catch~single_header', when='@0.1.3:')
    depends_on('spdlog', when='@0.1.3:')

    def cmake_args(self):
        result = [
            '-DEXTLIB_FROM_SUBMODULES=ON',
            '-DREPORTS_ONLY=ON',
        ]
        if self.spec.satisfies('+mpi'):
            result.extend([
                '-DCMAKE_C_COMPILER:STRING={0}'.format(
                    self.spec['mpi'].mpicc
                ),
                '-DCMAKE_CXX_COMPILER:STRING={0}'.format(
                    self.spec['mpi'].mpicxx
                ),
                '-DREPORTS_ENABLE_MPI=ON',
            ])
        return result

    @property
    def libs(self):
        """Export the libsonata library.
        Sample usage: spec['libsonata'].libs.ld_flags
        """
        search_paths = [[self.prefix.lib64, False], [self.prefix.lib, False]]
        is_shared = '+shared' in self.spec
        for path, recursive in search_paths:
            libs = find_libraries(['libsonata', 'libsonatareport'], root=path,
                                  shared=True, recursive=False)
            if libs:
                return libs
        return None
