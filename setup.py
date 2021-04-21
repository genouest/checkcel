from setuptools import find_packages, setup

with open('requirements.txt') as f:
    requires = f.read().splitlines()

setup(
    name="govalidator",
    version='0.0.1',
    description="Generate and validate tabulated/spreadsheet files",
    author="Mateo Boudet",
    author_email="mateo.boudet@inrae.fr",
    url="https://github.com/mboudet/validator",
    install_requires=requires,
    packages=find_packages(),
    long_description_content_type="text/markdown",
    license='MIT',
    platforms="Posix; MacOS X; Windows",
    entry_points='''
        [console_scripts]
        govalidator=govalidator.main:main
    ''',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3.7",
    ]
)
