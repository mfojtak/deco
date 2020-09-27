import codecs
from setuptools import setup, find_packages

with codecs.open('README.md', 'r', 'utf8') as reader:
    long_description = reader.read()



setup(
    name='deco',
    version='0.0.3',
    packages=find_packages(),
    url='https://github.com/mfojtak/deco',
    license='MIT',
    author='mfojtak',
    author_email='mfojtak@seznam.cz',
    description='deco',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=["tensorflow", "numpy", "keras-bert", "pyarrow", 
                        "quart", "faiss-cpu", "tensorflow-text", "sentencepiece"],
    scripts=['export_to_serving.py', 'server.py'],
    classifiers=(
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
