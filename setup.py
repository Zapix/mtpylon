# -*- coding: utf-8 -*-
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="mtpylon",
    version="0.0.1",
    author="Aleksandr Aibulatov",
    author_email="zap.aibulatov@gmail.com",
    description="Library to build backend with MTProto protocol",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Zapix/mtpylon",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.9",
        "Framework :: AsyncIO",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'aiohttp>=3.7.4',
        'aiohttp-cors>=0.7.0',
        'rsa>=4.7.2',
        'TgCrypto>=1.2.2',
        'pyaes>=1.6.1',
        'mypy-extensions>=0.4.3',
    ],
    python_requires='>=3.9',
)
