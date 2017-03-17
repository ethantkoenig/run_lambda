
run_lambda
==========

``run_lambda`` is a Python package for running Python
`AWS Lambda <https://aws.amazon.com/lambda/>`_ functions locally. It offers a
Python module for automated testing of Lambda functions, as well as a
command-line interface for ad-hoc local invocations.

Doesn't something like this already exist?
------------------------------------------

Not exactly. There are other programs for locally running Python Lambda
functions. However, all of the other utilities (that I know of) only provide
a command-line tool. A command-line tool is great for quick manual invocations.
However, if you want to create robust, automated tests for your Lambda functions,
a Python module that you can import and call is more appropriate.
``run_lambda`` is unique because it offers both a simple command-line tool for
manual invocations, and an importable Python module for automated tests.

Features
--------

``run_lambda`` supports

- An interface for examining the result (return value, exception, timeout) of
  a function call
- A full implementation of AWS Context objects
- Function calls with or without a timeout
- Resource usage profiling (memory and run-time)
- Convenient mocking of objects and services inside Lambda functions

Installation
------------

The easiest way to install is via ``pip``::

    $ pip install run_lambda

You can also download the source from
`Github <https://www.github.com/ethantkoenig/python_run_lambda>`_.

Documentation
-------------

Documentation for the package can be found `here <https://www.pythonhosted.org/run-lambda>`_.
