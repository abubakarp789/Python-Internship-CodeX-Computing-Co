from setuptools import setup, find_packages

setup(
    name="file-transfer-assistant",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'PySide6>=6.0.0',
        'psutil>=5.8.0',
        'pywin32>=300;platform_system=="Windows"',
    ],
    entry_points={
        'console_scripts': [
            'file-transfer-assistant=src.__main__:main',
        ],
    },
    author="Abu Bakar",
    author_email="abubakarp789@gmail.com",
    description="A simple file transfer assistant application",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/abubakarp789/Python-Internship-CodeX-Computing-Co/FileTransferAssistant",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',
)
