from setuptools import setup
import glob

setup(
    name="nepse",
    version="0.1.0",
    description="Unofficial API to interface with https://www.nepalstock.com.np",
    url="https://github.com/basic-bgnr/NepseUnofficialApi",
    author="basic-bgnr",
    packages=["nepse"],
    install_requires=[
        "beautifulsoup4>=4.12.2",
        "Flask>=2.3.2",
        "pywasm>=1.0.8",
        "requests>=2.18.4",
    ],
    include_package_data=True,
    data_files=glob.glob("nepse/**"),
    classifiers=[
        "Development Status :: 0.1.0 - Beta",
        "Intended Audience :: Research",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
    ],
)
