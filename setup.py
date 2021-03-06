from distutils.core import setup, find_packages
from io import open

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
with open(path.join(here, 'LICENSE'), encoding='utf-8') as f:
    license = f.read()
    
setup(
    name='CritRoller',
    version='1.0',
    description='A small GUI application to roll custom Critical hits and Fumbles in the Pathfinder game system.'
    license=license
    long_description=long_description,
    url='https://github.com/analphagamma/CritRoller',
    author='Peter Bocz',
    install_requires = ['PyQt5']
)
