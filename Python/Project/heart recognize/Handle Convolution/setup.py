from distutils.core import setup, Extension
import numpy as np

module = Extension(
    '_Cconvolution',
    sources=['convolution_wrap.c', 'convolution.c']
)

setup(
    name='Cconvolution',
    version='0.1',
    author='SWIG Docs',
    description='v1',
    ext_modules=[module],
    py_modules=['Cconvolution'],
    include_dirs=[np.get_include()]
)