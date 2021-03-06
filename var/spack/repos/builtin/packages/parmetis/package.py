# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import sys


class Parmetis(CMakePackage):
    """ParMETIS is an MPI-based parallel library that implements a variety of
       algorithms for partitioning unstructured graphs, meshes, and for
       computing fill-reducing orderings of sparse matrices."""

    homepage = 'http://glaros.dtc.umn.edu/gkhome/metis/parmetis/overview'
    url      = 'http://glaros.dtc.umn.edu/gkhome/fetch/sw/parmetis/parmetis-4.0.3.tar.gz'
    list_url = 'http://glaros.dtc.umn.edu/gkhome/fetch/sw/parmetis/OLD'

    version('4.0.3', 'f69c479586bf6bb7aff6a9bc0c739628')
    version('4.0.2', '0912a953da5bb9b5e5e10542298ffdce')

    variant('shared', default=True, description='Enables the build of shared libraries.')
    variant('gdb', default=False, description='Enables gdb support.')

    depends_on('cmake@2.8:', type='build')
    depends_on('mpi')
    depends_on('metis@5:')

    patch('enable_external_metis.patch')
    # bug fixes from PETSc developers
    # https://bitbucket.org/petsc/pkg-parmetis/commits/1c1a9fd0f408dc4d42c57f5c3ee6ace411eb222b/raw/  # NOQA: E501
    patch('pkg-parmetis-1c1a9fd0f408dc4d42c57f5c3ee6ace411eb222b.patch')
    # https://bitbucket.org/petsc/pkg-parmetis/commits/82409d68aa1d6cbc70740d0f35024aae17f7d5cb/raw/  # NOQA: E501
    patch('pkg-parmetis-82409d68aa1d6cbc70740d0f35024aae17f7d5cb.patch')

    def flag_handler(self, name, flags):
        if name == 'cflags':
            if '%pgi' in self.spec:
                my_flags = flags + ['-c11']
                return (None, None, my_flags)
        return (None, None, flags)

    def url_for_version(self, version):
        url = 'http://glaros.dtc.umn.edu/gkhome/fetch/sw/parmetis'
        if version < Version('3.2.0'):
            url += '/OLD'
        url += '/parmetis-{0}.tar.gz'.format(version)
        return url

    def cmake_args(self):
        spec = self.spec

        options = []
        options.extend([
            '-DGKLIB_PATH:PATH=%s/GKlib' % spec['metis'].prefix.include,
            '-DMETIS_PATH:PATH=%s' % spec['metis'].prefix,
            '-DCMAKE_C_COMPILER:STRING=%s' % spec['mpi'].mpicc,
            '-DCMAKE_CXX_COMPILER:STRING=%s' % spec['mpi'].mpicxx
        ])

        if '+shared' in spec:
            options.append('-DSHARED:BOOL=ON')
        else:
            # Remove all RPATH options
            # (RPATHxxx options somehow trigger cmake to link dynamically)
            rpath_options = []
            for o in options:
                if o.find('RPATH') >= 0:
                    rpath_options.append(o)
            for o in rpath_options:
                options.remove(o)

        if '+gdb' in spec:
            options.append('-DGDB:BOOL=ON')

        return options

    @run_after('install')
    def darwin_fix(self):
        # The shared library is not installed correctly on Darwin; fix this
        if (sys.platform == 'darwin') and ('+shared' in self.spec):
            fix_darwin_install_name(prefix.lib)
