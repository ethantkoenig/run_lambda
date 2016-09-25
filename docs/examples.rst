

Examples
========

Example Unit Test
-----------------

Suppose we have a Lambda function in ``my_function.py``::

    import logging
    import random

    def handler(event, context):
        logger = logging.getLogger()
        n = event["number"]
        scale = random.randint(1, 10)
        product = n * scale
        logger.info("Log group name: %s", context.log_group_name)
        return product


We can write a unit test for the function::

    import mock
    import run_lambda
    import unittest

    import my_function

    class MyTests(unittest.TestCase):
        def test(self):
            event = {"number": 10}
            log_group_name = "test_log_group_name"
            context = run_lambda.MockLambdaContext.Builder()\
                .set_log_group_name(log_group_name)\
                .build()
            patches = {"random.randint", mock.MagicMock(return_value=5)}
            result = run_lambda.run_lambda(my_function.handler, event, context,
                                           patches=patches)
            self.assertEqual(result.value, 50)
            self.assertIn(log_group_name, result.summary.log)
