import os
import sys
from daomop.__version__ import version

from setuptools import setup, find_packages

dependencies = ['requests >= 2.7',
                'astropy >= 0.2.5',
                'vos >= 2.0',
                'numpy >= 1.6.1',
                'Polygon2',
                'scipy']


if sys.version_info[0] > 2:
    print 'The MOP package is only compatible with Python version 2.7+, not yet with 3.x'
    sys.exit(-1)

# # Build the list of validate and scripts to be installed.
#script_dirs = ['validate', 'scripts']
#scripts = []
#for script_dir in script_dirs:
#    for script in os.listdir(script_dir):
#        if script[-1] in ["~", "#"]:
#           continue
#        scripts.append(os.path.join(script_dir, script))

console_scripts = [ 'populate = daomop.populate:main', 'stationary = daomop.stationary:main', 'build_cat = daomop.build_cat:main']

setup(name='daomop',
      version=version,
      url='http://github.com/ijiraq/daomop',
      author='''JJ Kavelaars (jjk@uvic.ca),
              Michele Bannister (micheleb@uvic.ca)''',
      maintainer='M Bannister and JJ Kavelaars',
      maintainer_email='jjk@uvic.ca',
      description="Dominion Astrophysical Observatory Moving Object Pipeline: daomop",
      long_description='See github repp',
      classifiers=['Intended Audience :: Science/Research',
                   'Topic :: Scientific/Engineering :: Astronomy',
                   'Development Status :: 4 - Beta',
                   'Programming Language :: Python :: 2 :: Only',
                   'Operating System :: MacOS :: MacOS X',
                   'Environment :: X11 Applications',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   ],
      install_requires=dependencies,
      entry_points = { 'console_scripts': console_scripts},
      packages=find_packages(exclude=['tests',])
      )