import codecs
from setuptools import setup, find_packages

with codecs.open('README.md', 'r', 'utf8') as reader:
    long_description = reader.read()



setup(
    name='deco',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/mfojtak/deco',
    license='MIT',
    author='mfojtak',
    author_email='mfojtak@seznam.cz',
    description='deco',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=["tensorflow-gpu", "numpy", "keras-bert", "pyarrow", "quart", "faiss-cpu",
        "sentencepiece @ https://github.com/google/sentencepiece/releases/download/v0.1.84/sentencepiece-0.1.84-cp37-cp37m-manylinux1_x86_64.whl",
        "tf_sentencepiece @ https://github.com/google/sentencepiece/releases/download/v0.1.84/tf_sentencepiece-0.1.84-py2.py3-none-manylinux1_x86_64.whl"],
    scripts=['export_to_serving.py', 'server.py'],
    classifiers=(
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
