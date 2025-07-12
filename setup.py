from setuptools import setup, find_packages

setup(
    name="n-body-simulation",  # Replace with your project name
    version="0.1",
    packages=find_packages(where="src"),  # Automatically finds all packages under src/
    package_dir={"": "src"},  # Tells setuptools that packages are under src
    install_requires=[  # List any external dependencies here
        'contourpy==1.3.2',
        'cycler==0.12.1',
        'fonttools==4.58.5',
        'kiwisolver==1.4.8',
        'matplotlib==3.10.3',
        'numpy==2.3.1',
        'packaging==25.0',
        'pillow==11.3.0',
        'pygame==2.6.1',
        'pyparsing==3.2.3',
        'python-dateutil==2.9.0.post0',
        'six==1.17.0'
    ],
    include_package_data=True
)
