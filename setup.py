from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='corrGraph',
    version='0.1.0a2',
    author='Mawuli Adjei',
    author_email='mawuliadjei@gmail.com',
    description='A python module built using graph theory to analyse how attributes/features in a dataset correlate with each other',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mawuliadjei/corrGraph',
    packages=find_packages(),
    install_requires=required,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
