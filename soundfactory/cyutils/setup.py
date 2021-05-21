import os
from numpy import get_include
from distutils.core import setup
from Cython.Build import cythonize

os.environ["CPPFLAGS"] = os.getenv("CPPFLAGS", "") + "-I" + get_include()


setup(ext_modules=cythonize('builder_utils.pyx'))
