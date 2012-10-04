from setuptools import setup
import os
import re
import common


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

README = read('README.rst')

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


def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'(\s*git)|(\s*hg)', line):
            pass
        else:
            requirements.append(line)
    return requirements


def parse_dependency_links(file_name):
    dependency_links = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'\s*-[ef]\s+', line):
            dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))

    return dependency_links


setup(
    name='switch2bill-common',
    version=common.__version__,
    description='Common Django/Python helpers for Star2Billing projects',
    long_description=README,
    url='http://github.com/Star2Billing/switch2bill-common',
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
    install_requires=parse_requirements('requirements.txt'),
    dependency_links=parse_dependency_links('requirements.txt'),
)
