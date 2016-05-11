from spack import *
from spack.package_test import *
import sys
import os
import shutil

class Openblas(Package):
    """OpenBLAS: An optimized BLAS library"""
    homepage = "http://www.openblas.net"
    url      = "http://github.com/xianyi/OpenBLAS/archive/v0.2.15.tar.gz"

    version('0.2.18', '805e7f660877d588ea7e3792cda2ee65')
    version('0.2.17', '664a12807f2a2a7cda4781e3ab2ae0e1')
    version('0.2.16', 'fef46ab92463bdbb1479dcec594ef6dc')
    version('0.2.15', 'b1190f3d3471685f17cfd1ec1d252ac9')

    variant('shared', default=True,  description="Build shared libraries as well as static libs.")
    variant('openmp', default=False, description="Enable OpenMP support.")
    variant('fpic',   default=True,  description="Build position independent code")

    # virtual dependency
    provides('blas')
    provides('lapack')

    patch('make.patch')

    def install(self, spec, prefix):
        # Openblas is picky about compilers. Configure fails with
        # FC=/abs/path/to/f77, whereas FC=f77 works fine.
        # To circumvent this, provide basename only:
        make_defs = ['CC=%s' % os.path.basename(spack_cc),
                     'FC=%s' % os.path.basename(spack_f77),
                     'MAKE_NO_J=1']

        make_targets = ['libs', 'netlib']

        # Build shared if variant is set.
        if '+shared' in spec:
            make_targets += ['shared']
        else:
            if '+fpic' in spec:
                make_defs.extend(['CFLAGS=-fPIC', 'FFLAGS=-fPIC'])
            make_defs += ['NO_SHARED=1']

        # fix missing _dggsvd_ and _sggsvd_
        if spec.satisfies('@0.2.16'):
            make_defs += ['BUILD_LAPACK_DEPRECATED=1']

        # Add support for OpenMP
        if '+openmp' in spec:
            # Note: Apple's most recent Clang 7.3.0 still does not support OpenMP.
            # What is worse, Openblas (as of 0.2.18) hardcoded that OpenMP cannot
            # be used with any (!) compiler named clang, bummer.
            if spec.satisfies('%clang'):
                raise InstallError('OpenBLAS does not support OpenMP with clang!')

            make_defs += ['USE_OPENMP=1']

        make_args = make_defs + make_targets
        make(*make_args)

        make("tests", *make_defs)

        # no quotes around prefix (spack doesn't use a shell)
        make('install', "PREFIX=%s" % prefix, *make_defs)

        # Blas virtual package should provide blas.a and libblas.a
        with working_dir(prefix.lib):
            symlink('libopenblas.a', 'blas.a')
            symlink('libopenblas.a', 'libblas.a')
            if '+shared' in spec:
                symlink('libopenblas.%s' % dso_suffix, 'libblas.%s' % dso_suffix)

        # Lapack virtual package should provide liblapack.a
        with working_dir(prefix.lib):
            symlink('libopenblas.a', 'liblapack.a')
            if '+shared' in spec:
                symlink('libopenblas.%s' % dso_suffix, 'liblapack.%s' % dso_suffix)

        # Openblas may pass its own test but still fail to compile Lapack
        # symbols. To make sure we get working Blas and Lapack, do a small test.
        self.check_install(spec)


    def setup_dependent_package(self, module, dspec):
        # This is WIP for a prototype interface for virtual packages.
        # We can update this as more builds start depending on BLAS/LAPACK.
        libdir = find_library_path('libopenblas.a', self.prefix.lib64, self.prefix.lib)

        self.spec.blas_static_lib   = join_path(libdir, 'libopenblas.a')
        self.spec.lapack_static_lib = self.spec.blas_static_lib

        if '+shared' in self.spec:
            self.spec.blas_shared_lib   = join_path(libdir, 'libopenblas.%s' % dso_suffix)
            self.spec.lapack_shared_lib = self.spec.blas_shared_lib

    def check_install(self, spec):
        source_file = join_path(os.path.dirname(self.module.__file__),
                                'test_cblas_dgemm.c')
        blessed_file = join_path(os.path.dirname(self.module.__file__),
                                 'test_cblas_dgemm.output')

        include_flags = ["-I%s" % join_path(spec.prefix, "include")]
        link_flags = ["-L%s" % join_path(spec.prefix, "lib"),
                      "-llapack",
                      "-lblas",
                      "-lpthread"]
        if '+openmp' in spec:
            link_flags.extend([self.compiler.openmp_flag])

        output = compile_c_and_execute(source_file,include_flags,link_flags)
        compare_output_file(output,blessed_file)
