import pathlib
from setuptools import find_packages, setup

import compot

HERE = pathlib.Path(__file__).parent
README = (HERE / 'README.md').read_text()

setup(
    name='compot-ui',
    version=compot.__VERSION__,
    description='A small, stateless, fully compositional TUI framework.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/markovejnovic/compot',
    author='Marko Vejnovic',
    author_email='contact@markovejnovic.com',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console :: Curses',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries'
    ],
    packages=find_packages(exclude='tests/'),
    include_package_data=False,
    install_requires=['wcwidth']
)
