from setuptools import setup, find_packages
import src
import os
if len(os.environ.get("TRAVIS_TAG", ""))==0:
    long_description = ""
else:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')


requirements = [
    "numpy",
    "six",
    "future"
]

setup(name='jamotools',
    version=src.__version__,
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