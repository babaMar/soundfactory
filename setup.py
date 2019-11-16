from setuptools import setup

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
    python_requires='>=3.5',
    install_requires=requirements,
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
