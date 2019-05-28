# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ClingCuda(CMakePackage):
    """Cling is an interactive C++ interpreter, built on top of Clang and LLVM
       compiler infrastructure. Cling realizes the read-eval-print loop (REPL)
       concept, in order to leverage rapid application development. Implemented
       as a small extension to LLVM and Clang, the interpreter reuses their
       strengths such as the praised concise and expressive compiler diagnostics.
    """

    homepage = 'https://root.cern.ch/cling'
    url = 'https://github.com/root-project/cling/archive/v0.5.tar.gz'
    git = 'https://github.com/root-project/cling.git'

    family = 'compiler'  # Used by lmod

    # NOTE: The debug version of LLVM is an order of magnitude larger than
    # the release version, and may take up 20-30 GB of space. If you want
    # to save space, build with `build_type=Release`.

    variant('shared_libs', default=False,
            description="Build all components as shared libraries, faster, "
            "less memory to build, less stable")
    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))

    # Build dependency
    depends_on('cmake@3.4.3:', type='build')

    # Universal dependency
    depends_on('python@2.7:2.8')

    version('develop', git='http://root.cern.ch/git/llvm.git', branch='cling-patches')
    resource(name='clang',
             git='http://root.cern.ch/git/clang.git',
             branch='cling-patches', destination='tools',
             placement='clang')
    resource(name='cling',
             git='https://github.com/SimeonEhrig/cling',
             branch='test_release',
             destination='tools',
             placement='cling')

    # LLVM 4 and 5 does not build with GCC 8
    conflicts('%gcc@8:',       when='@:5')
    conflicts('%gcc@:5.0.999', when='@8:')

    def cmake_args(self):
        spec = self.spec
        cmake_args = [
            '-DLLVM_REQUIRES_RTTI:BOOL=ON',
            '-DLLVM_ENABLE_RTTI:BOOL=ON',
        ]

        if '+shared_libs' in spec:
            cmake_args.append('-DBUILD_SHARED_LIBS:Bool=ON')
        if spec.satisfies('platform=linux'):
            cmake_args.append('-DCMAKE_BUILD_WITH_INSTALL_RPATH=1')
        return cmake_args
