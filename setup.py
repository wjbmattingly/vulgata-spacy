from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

VERSION = '0.0.1'
DESCRIPTION = 'A library for finding Vulgate references in Medieval Latin texts.'

setup(
    name="vulgata-spacy",
    author="WJB Mattingly",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=["pandas>=1.0.0,<2.0.0",
                     "protobuf<=3.20.0",
                     "spacy>=3.3.0",
                     "gensim>=4.2.0",
                     "annoy>=1.10.0",
                     "jellyfish>=0.8.0"
                     ],
    include_package_data = True
)
