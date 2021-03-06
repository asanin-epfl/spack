# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySymengine(PythonPackage):
    """Python wrappers for SymEngine, a symbolic manipulation library."""

    homepage = "https://github.com/symengine/symengine.py"
    url      = "https://pypi.io/packages/source/s/symengine/symengine-0.2.0.tar.gz"
    git      = "https://github.com/symengine/symengine.py.git"

    version('develop', branch='master')
    version('0.3.0', sha256='0ecccfe5a09b25b6640afca12de62062bdb60ed2712d6c16cc47fc1ba1e851ac')
    version('0.2.0', sha256='78a14aea7aad5e7cbfb5cabe141581f9bba30e3c319690e5db8ad99fdf2d8885')

    # Build dependencies
    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'))
    depends_on('py-setuptools',     type='build')
    depends_on('py-cython@0.19.1:', type='build')
    depends_on('cmake@2.8.7:',      type='build')
    depends_on('symengine@0.3.0:')

    def build_args(self, spec, prefix):
        return ['build_ext', '--symengine-dir={0}'.format(spec['symengine'].prefix)]
