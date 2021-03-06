from setuptools import setup, find_packages

setup(
    name="atspythonutils",
    version="0.1.0",
    description="An API to make some game utilites for TrekMUSH: Among The Stars available via HTTP",
    url="https://github.com/kcphysics/ATSPythonUtils",
    author="KCPhysics",
    packages=find_packages(exclude=["data"]),
    classifiers=[
        "Programmin Language :: Python :: 3.6.8",
        "Natural Language   :: English",
        "License    :: MIT"
    ],
    entry_points={
        "console_scripts": [
            "atsono=atspythonutils.atsono:get_ono",
            "atsbestroute=atspythonutils.atsflightplan:best_route",
            "atspdest=atspythonutils.atsheadings:get_objects_on_line",
            "atspdestobj=atspythonutils.atsheadings:get_objects_on_line_from_object"
        ]
    },
    zip_safe=False,
    install_requires=[
    ],
    package_data = {
        "data": ["data/atsdata.json"]
    }
)