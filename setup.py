from setuptools import setup, find_packages
#from distutils.core import setup
# from Cython.Build import cythonize

VERSION="0.9.3"

setup(name='PyFlowChart',
    version=VERSION,
    description='Application to help manage cirriculum flowcharts at CalPoly',
    author='Jim Heald',
    author_email='james.r.heald@gmail.com',
    url='https://github.com/steelcowboy/PyFlowChart',
    license='Modified BSD',
    packages=find_packages(),
    package_data = { '/usr/share/applications': [ 'pyflowchart.desktop' ] },
    # ext_modules = cythonize(["pyflowchart/*.py", "pyflowchart/coursetools/*.py", "pyflowchart/interface/*.py"]),
    entry_points={'gui_scripts': [
        'pyflowchart = pyflowchart.main:main'
        ]}
)
