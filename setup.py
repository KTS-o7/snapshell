from setuptools import setup, find_packages

setup(
    name='snapshell',
    version='1.1.1',
    author='Krishnatejaswi S',
    author_email='shentharkrishnatejaswi@gmail.com',
    description='An AI-powered tool to suggest Linux commands based on user input',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/KTS-o7/snapshell',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'groq',
        'requests',
        'instructor',
        'pydantic',
        'tqdm',  
    ],
    entry_points={
        'console_scripts': [
            'snapshell=snapshell.cli:main',
        ],
    },
    setup_requires=[
        'setuptools',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
