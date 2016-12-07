#! /usr/bin/env python3

from setuptools import setup
from tiborcim.tibc import get_version
from os import name as name
if 'nt' in name:
    data = [('share/pixmaps', ['conf/cim.png', ]),
                ('share/applications', ['conf/cim.desktop', ])]
else:
    data = []

setup(
    name='Tiborcim',
    version=get_version(),
    description="""
    Tiborcim is an cross/transpiler providing a BASIC
    like language for use with the Micro:Bit.
    """,
    author='Zander Brown',
    url='https://github.com/zanderbrown/tiborcim',
    packages=['tiborcim', 'tiborcim.contrib', 'tiborcim.resources'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment :: X11 Applications :: Tk',
        'Intended Audience :: Education',
        'Topic :: Education',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            "tibc = tiborcim.tibc:run",
            "cim = tiborcim.cim:run"
        ],
    },
    data_files=data,
)
