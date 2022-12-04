import setuptools

__author__ = 'Sobolev Andrey <email.asobolev@gmail.com>'
__version__ = '1.6.14'

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='simple-print',
    version=__version__,
    install_requires=['termcolor==1.1.0', 'executing==0.8.1', 'asttokens==2.0.5', 'typing-extensions>=4.1.0'],
    extras_require={ 
        'broker': ['pika>=1.3.0', 'pydantic>=1.10.2', 'orjson>=3.8.0'], 
    },
    author='Sobolev Andrey',
    author_email='email.asobolev@gmail.com',
    description='Powerful debugging & logging tool for Python.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url="https://github.com/Sobolev5/simple-print/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)