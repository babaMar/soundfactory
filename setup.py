import os
from setuptools import setup, dist
dist.Distribution().fetch_build_eggs(['Cython>=0.29.17', 'numpy>=1.18.4'])


from Cython.Build import cythonize
import numpy

os.environ["CPPFLAGS"] = os.getenv("CPPFLAGS", "") + "-I" + numpy.get_include()

tests_require = [
        'pytest',
        'pytest-mock',
        'pytest-cov'
        ]


with open("README.md", "r") as fh:
    long_description = fh.read()

    
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

    
setup(
    name="soundfactory",
    packages=["soundfactory"],
    version="0.1.0",
    author="TSAK",
    author_email="tsakians@gmail.com",
    description="simple tools for audio-signal manipulations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/babaMar/soundfactory",
    license='MIT',
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=requirements,
    ext_modules=cythonize("soundfactory/cyutils/*.pyx"),
    tests_require=[tests_require],
    extras_require={
        'tests': tests_require
    },
    entry_points={
        'console_scripts': [
            'soundfactory = soundfactory.cli:main',
        ]
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Topic :: Artistic Software',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
