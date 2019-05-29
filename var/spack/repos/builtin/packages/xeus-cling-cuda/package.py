# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class XeusClingCuda(CMakePackage):
    """QuantStack C++ implementation of Jupyter kernel protocol"""

    homepage = "https://github.com/QuantStack/xeus-cling"
    url      = "https://github.com/QuantStack/xeus-cling/archive/0.4.8.tar.gz"
    git      = "https://github.com/QuantStack/xeus.git"

    #version('develop', branch='master')
    version('0.4.8', sha256='d057978e0d821d9c4d0ff2a3e8fcf60758d94af60227d3958fa287c9a2d24b7b')

    conflicts('%gcc@:4.8')
    conflicts('%clang@:3.6')
    conflicts('%intel@:17')

    depends_on('xeus@0.15.0', when='@0.4.8')
    depends_on('pugixml@1.8.1')
    depends_on('cxxopts@2.1.2')
    #depends_on('miniconda3')
    depends_on('cling-cuda')
    
    depends_on('cmake@3.1:', type='build')

