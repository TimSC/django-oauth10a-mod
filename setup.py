from setuptools import setup, find_packages
from oauth_provider import __version__ as version
import os

def strip_comments(l):
    return l.split('#', 1)[0].strip()

def reqs(*f):
    return list(filter(None, [strip_comments(l) for l in open(
        os.path.join(os.getcwd(), *f)).readlines()]))

install_requires = reqs('requirements.txt')
test_requires = reqs('test-requirements.txt')

setup(
    name='django-oauth10a-mod',
    version=version,
    description='Support of OAuth 1.0a in Django using python-oauth10a.',
    author='Tim Sheerman-Chase',
    author_email='dev@kinatomic.com',
    url='https://github.com/TimSC/django-oauth10a-mod',
    packages=find_packages(),
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
    ],
    # Make setuptools include all data files under version control,
    # svn and CVS by default
    include_package_data=True,
    zip_safe=False,
    test_requires=test_requires,
    install_requires=install_requires,
)
