from setuptools import setup
import os
from common import VERSION

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('common'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[len('common') + 1:]  # Strip "common/"
        for f in filenames:
            data_files.append(os.path.join(prefix, f))

setup(
    name='switch2bill-common',
    version="-".join(map(str, VERSION[0:3])) + "".join(VERSION[3:]),
    description='Common Libs from Star2Billing projects',
    author='Belaid Arezqui',
    author_email='areski@gmail.com',
    license='MPL 2.0 License',
    classifiers=[
        'Development Status :: 1 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers, Users',
        'License :: OSI Approved :: MPL 2.0 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python, Javascript, HTML',
        'Topic :: Django Helpers Templates common utils',
        ],
    packages=packages,
    package_dir={'common': 'common'},
    package_data={'common': data_files},
    entry_points={'django.apps': 'common = common'},
)
