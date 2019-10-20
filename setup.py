import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Talr",
    version="0.0.1",
    author="Shaun Jackman",
    author_email="sjackman@gmail.com",
    description="Targeted Assembly of Linked Reads",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sjackman/talr",
    license="GPLv3",
    python_requires=">=3",
    install_requires=["unicycler, Bandage, bedtools, bwa, ema, ghostscript, graphviz, miller, \
        minimap2, parallel, pypy3, quast, samtools, seqtk, tigmint, trimadap" ],
    packages=["talr"],
    scripts=["bin/talr"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)