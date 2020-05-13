import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jenkrunner-ploq", # Replace with your own username
    version="0.0.1",
    author="Marcus Gustafsson",
    author_email="hello@vinq.se",
    description="Simple tool for running Jenkins job on the command line",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ploq/jenkrunner",
    packages=setuptools.find_packages(),
    scripts=["bin/jenkrunner"],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
