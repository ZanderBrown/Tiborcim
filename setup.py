from setuptools import setup
from tiborcim.tibc import get_version

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
            "cim = tiborcim.tiborcim:run"
        ],
    },
    data_files=[('/usr/share/pixmaps', ['conf/cim.png', ]),
                ('/usr/share/applications', ['conf/cim.desktop', ])],
)
