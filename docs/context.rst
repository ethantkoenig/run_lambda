

Context Objects
===============

The ``run_lambda`` module provides classes for mocking AWS Lambda Context objects.
See `here <https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html>`_
for more information about AWS Lambda Context objects.

MockLambdaContext class
-----------------------

.. autoclass:: run_lambda::MockLambdaContext()
    :members:

MockLambdaContext.Builder class
-------------------------------

It is strongly encouraged to use the
:class:`MockLambdaContext.Builder <run_lambda.MockLambdaContext.Builder>` class
to construct :class:`MockLambdaContext <run_lambda.MockLambdaContext>` instances.

.. autoclass:: run_lambda::MockLambdaContext.Builder()
    :members:

MockCognitoIdentity class
-------------------------

.. autoclass:: run_lambda::MockCognitoIdentity()
    :members:

MockClientContext class
-----------------------

.. autoclass:: run_lambda::MockClientContext()
    :members:

MockClientContext.Client class
------------------------------

.. autoclass:: run_lambda::MockClientContext.Client()
    :members:
