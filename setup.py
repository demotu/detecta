import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="detecta",
    version="0.0.5",
    author="Marcos Duarte",
    author_email="duartexyz@gmail.com",
    description="Detect events in data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/demotu/detecta",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
