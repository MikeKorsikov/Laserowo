from setuptools import setup, find_packages
import os

def read_requirements():
    """Read requirements from requirements.txt."""
    with open('requirements.txt', 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='laser_hair_removal_app',
    version='0.1.0',
    description='A desktop application for managing laser hair removal business operations.',
    author='Your Name',
    author_email='your-email@example.com',
    url='https://github.com/yourusername/laser-hair-removal-app',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'laser-app=src.main:main',
        ],
    },
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,
    data_files=[
        ('config', ['config/app_config.yaml', 'config/secrets.yaml']),
        ('data', []),
    ],
)