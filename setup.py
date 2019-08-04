
from setuptools import setup, find_packages
from treesync.version import __version__

setup(
    name='treesync',
    keywords='rsync tree sync',
    description='python utility to rsync push / pull configured trees with known arguments',
    author='Ilkka Tuohela',
    author_email='hile@iki.fi',
    url='https://github.com/hile/treesync/',
    version=__version__,
    license='PSF',
    packages=find_packages(),
    python_requires='>3.6.0',
    entry_points={
        'console_scripts': [
            'treesync=treesync.bin.treesync:main',
        ],
    },
    install_requires=(
        'systematic',
    ),
    setup_requires=['pytest-runner'],
    tests_require=(
        'pytest',
        'pytest-runner',
        'pytest-datafiles',
    ),
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: System',
        'Topic :: System :: Systems Administration',
    ],
)
