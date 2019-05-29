# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cxxopts(CMakePackage):
    """This is a lightweight C++ option parser library, supporting the standard
       GNU style syntax for options.
    """

    homepage = 'https://github.com/jarro2783/cxxopts'
    url      = 'https://github.com/jarro2783/cxxopts'
    git      = 'https://github.com/jarro2783/cxxopts'
    
    version('2.1.2', '4840953410eb3c2db94aea09c6b92931b4a9790affa575aabea7e061376a2925',
            url='https://github.com/jarro2783/cxxopts/tarball/v2.1.2')

    depends_on('cmake@3.1:', type='build')

