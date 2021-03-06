from setuptools import setup, find_packages
import os
import re
import django_lets_go


def read(*parts):
    return open(os.path.join(os.path.dirname(__file__), *parts)).read()


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
    name='django-lets-go',
    version=django_lets_go.__version__,
    description='Django helpers, goodies, mix of snippets, etc...',
    long_description=read('README.rst'),
    url='http://github.com/areski/django-lets-go',
    author='Belaid Arezqui',
    author_email='areski@gmail.com',
    license='MIT License',
    zip_safe=False,
    packages=find_packages(exclude=["tests", "demoproject", "docs"]),
    package_data={},
    install_requires=parse_requirements('requirements.txt'),
    dependency_links=parse_dependency_links('requirements.txt'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
