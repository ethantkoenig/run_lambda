from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


with open(path.join(here, "README.rst"), "r") as f:
    long_description = f.read()


setup(
    name="run_lambda",
    version="0.1.5",
    description="Run AWS Lambda functions locally",
    long_description=long_description,
    url="https://github.com/ethantkoenig/run_lambda",
    author="Ethan Koenig",
    author_email="ethantkoenig@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    keywords=["aws", "lambda", "run", "local", "locally"],
    packages=find_packages(),
    install_requires=["memory_profiler", "mock", "psutil", "six"],
    test_suite="tests",
    entry_points={
        'console_scripts': ['run_lambda=run_lambda.__main__:main',
                            'run_lambda_context_template=run_lambda.__gen_context:main']
    }
)
