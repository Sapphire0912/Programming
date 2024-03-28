from distutils.core import setup, Extension

module = Extension(
    '_testC',
    sources=['testC_wrap.c', 'testC.c'],
)

setup(
    name='testC',
    version='0.1',
    author='SWIG Docs',
    description="first",
    ext_modules=[module],
    py_modules=['testC']
)
