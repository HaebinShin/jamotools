from setuptools import setup, find_packages
import os
if len(os.environ.get("TRAVIS_TAG", ""))==0:
    long_description = ""
else:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')

import re
# https://milkr.io/kfei/5-common-patterns-to-version-your-Python-package/4
def get_version(path):
    VERSIONFILE = path
    initfile_lines = open(VERSIONFILE, 'rt').readlines()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(VSRE, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError('Unable to find version string in %s.' % (VERSIONFILE,))

requirements = [
    "numpy",
    "six",
    "future"
]

setup(name='jamotools',
    version=get_version('src/__init__.py'),
    description='A library for Korean Jamo split and vectorize.',
    long_description=long_description,
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
        'Topic :: Text Processing :: Linguistic',
        'Natural Language :: Korean'
    ],
    url='https://github.com/HaebinShin/jamotools',
    author='Haebin Shin',
    author_email='sunsal0704@gmail.com',
    license='GPL',
    install_requires=requirements,
    packages=['jamotools', 'jamotools.jamo', 'jamotools.vector'],
    package_dir={'jamotools': 'src'},
    zip_safe=False)