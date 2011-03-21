from setuptools import setup
import os

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('common'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[len('common')+1:] # Strip "dummyapp/" or "dummyapp\"
        for f in filenames:
            data_files.append(os.path.join(prefix, f))

setup(
    name='switch2bill-common',
    version='0.1',
    description='Django Common Libs',
    author='Belaid Arezqui',
    author_email='areski@gmail.com',
    packages=packages,
    package_dir={'common': 'common'},
    package_data={'common': data_files},
    entry_points={'django.apps': 'common = common'},
)
