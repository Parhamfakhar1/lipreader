from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lipreader",
    version="0.1.0",
    author="Your Name",
    description="CPU-based lip reading toolkit for command recognition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/parhamfakhar1/lipreader",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "opencv-python",
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "lipreader=lipreader.cli:main",
        ],
    },
)