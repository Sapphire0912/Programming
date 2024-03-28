from distutils.core import setup, Extension
import numpy as np

module = Extension(
    '_CArray',
    sources=['CallArray_wrap.c', 'CallArray.c']
)

setup(
    name='CArray',
    version='0.1',
    author='SWIG Docs',
    description='v1',
    ext_modules=[module],
    py_modules=['CArray'],
    include_dirs=[np.get_include()]
)