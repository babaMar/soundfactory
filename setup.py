from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

    
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

    
setup(
    name="soundfactory",
    version="0.0.1",
    author="babaMar",
    author_email="author@example.com",
    description="Manage sound and images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/babaMar/soundfactory",
    # packages=find_packages(),
    python_requires='>=3.5',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'soundfactory = soundfactory:main',
        ]
    }
)
