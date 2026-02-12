from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def read_requirements():
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return ["opencv-python", "numpy"]

setup(
    name="lipreader",
    version="0.1.0",
    author="Parham Fakhari",
    author_email="parhamfakhari.nab2020@gmail.com",
    description="A CPU-only lip reading toolkit for command recognition from video",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/parhamfakhar1/lipreader",
    project_urls={
        "Bug Tracker": "https://github.com/parhamfakhar1/lipreader/issues",
        "Source Code": "https://github.com/parhamfakhar1/lipreader",
    },
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "lipreader=lipreader.cli:main",
        ],
    },
    include_package_data=True,
)