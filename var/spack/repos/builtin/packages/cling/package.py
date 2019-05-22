# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cling(CMakePackage):
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

    # TODO: The current version of this package unconditionally disables CUDA.
    #       Better would be to add a "cuda" variant that:
    #        - Adds dependency on the "cuda" package when enabled
    #        - Sets the necessary CMake flags when enabled
    #        - Disables CUDA (as this current version does) only when the
    #          variant is also disabled.

    # variant('cuda', default=False,
    #         description="Build the LLVM with CUDA features enabled")

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

    resources = {
        'clang': {
            'url': 'http://root.cern.ch/git/clang.git',
            'destination': 'tools',
            'placement': 'clang',
        },
        'cling': {
            'url': 'http://root.cern.ch/git/cling.git',
            'destination': 'tools',
            'placement': 'cling',
        },
    }

    releases = [
        {
            'version': 'develop',
            'repo': 'http://root.cern.ch/git/llvm.git',
            'resources': {
                'clang': 'cling-patches',
                'cling': 'master',
            }
        },
#        {
#            'version': '0.5.0',
#            'repo': 'http://root.cern.ch/git/llvm.git',
#            'resources': {
#                'compiler-rt': '547893456e22c75d16189a13881bc866',
#                'openmp': 'b6f9bf1df85fe4b0ab9d273adcef6f6d',
#            }
#        }
    ]

    for release in releases:
        if release['version'] == 'develop':
            version(release['version'], git=release['repo'], branch='cling-patches')

            for name, rBranch in release['resources'].items():
                resource(name=name,
                         git=resources[name]['url'],
                         branch=rBranch,
                         destination=resources[name]['destination'],
                         placement=resources[name].get('placement', None))
        else:
            pass

#            version(release['version'], release['md5'], url=llvm_url % release)
#            for name, md5 in release['resources'].items():
#                resource(name=name,
#                         url=resources[name]['url'] % release,
#                         md5=md5,
#                         destination=resources[name]['destination'],
#                         when='@%s%s' % (release['version'],
#                                         resources[name].get('variant', "")),
#                         placement=resources[name].get('placement', None))

    # LLVM 4 and 5 does not build with GCC 8
    conflicts('%gcc@8:',       when='@:5')
    conflicts('%gcc@:5.0.999', when='@8:')

    def cmake_args(self):
        spec = self.spec
        cmake_args = [
            '-DLLVM_REQUIRES_RTTI:BOOL=ON',
            '-DLLVM_ENABLE_RTTI:BOOL=ON',
        ]

        # TODO: Instead of unconditionally disabling CUDA, add a "cuda" variant
        #       (see TODO above), and set the paths if enabled.
#        cmake_args.extend([
#            '-DCUDA_TOOLKIT_ROOT_DIR:PATH=IGNORE',
#            '-DCUDA_SDK_ROOT_DIR:PATH=IGNORE',
#            '-DCUDA_NVCC_EXECUTABLE:FILEPATH=IGNORE',
#            '-DLIBOMPTARGET_DEP_CUDA_DRIVER_LIBRARIES:STRING=IGNORE'])

        if '+shared_libs' in spec:
            cmake_args.append('-DBUILD_SHARED_LIBS:Bool=ON')
        if spec.satisfies('platform=linux'):
            cmake_args.append('-DCMAKE_BUILD_WITH_INSTALL_RPATH=1')
        return cmake_args
