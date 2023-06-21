"""
Setup file for nasa_edx_extensions Django plugin.
"""

from __future__ import print_function

from setuptools import setup

from utils import get_version, load_requirements


with open("README.rst", "r") as fh:
    README = fh.read()


VERSION = get_version('nasa_edx_extensions', '__init__.py')
APP_NAME = "nasa_edx_extensions = nasa_edx_extensions.apps:NasaEdxExtensionsConfig"


setup(
    name='nasa-edx-extensions',
    version=VERSION,
    author='Raccoon Gang',
    author_email='contact@raccoongang.com',
    description='Nasa EDX Extensions',
    license='AGPL',
    long_description=README,
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.8',
    ],
    packages=[
        'nasa_edx_extensions',
    ],
    include_package_data=True,
    install_requires=load_requirements('requirements/base.in'),
    zip_safe=False,
    entry_points={"lms.djangoapp": [APP_NAME]},
)
