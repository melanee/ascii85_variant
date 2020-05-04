import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ascii_x85sl",
    version="0.0.2",
    author="Melanee Hannah",
    author_email="melaneehannah@oogets.email",
    description="A ascii85 variant package with optional symbols translation to alpha characters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/melanee/x85sl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL V03 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

