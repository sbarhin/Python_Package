from setuptools import setup, find_packages

setup(
    name='pycomms_pay',
    version='1.1.1',
    description='A package for seamless Email, SMS and Payment Packages Integration',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/sbarhin/Python_Package',
    author='Shaukat Arhin',
    author_email='shaubint123@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'google-auth',
        'google-auth-oauthlib',
        'google-auth-httplib2',
        'google-api-python-client',
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
