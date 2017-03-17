

Examples
========

Example Unit Test
-----------------

Suppose we have the following Lambda function in ``my_function.py``::

    import logging
    import random

    def handler(event, context):
        logger = logging.getLogger()
        logger.info("Log group name: %s", context.log_group_name)
        n = event["number"]
        scale = random.randint(1, 10)
        product = n * scale
        return product


We can write a unit test for the function as follows::

    import mock
    import run_lambda
    import unittest

    import my_function

    class MyFunctionTest(unittest.TestCase):
        def test(self):
            log_group_name = "test_log_group_name"
            context = run_lambda.MockLambdaContext.Builder()\
                .set_log_group_name(log_group_name)\
                .build()

            # mock random.randint to always return 5
            patches = {"random.randint": mock.MagicMock(return_value=5)}

            result = run_lambda.run_lambda(my_function.handler,
                                           event={"number": 10},
                                           context=context,
                                           patches=patches)

            # assert that return value is as expected
            self.assertEqual(result.value, 50)

            # assert that log_group_name was logged
            self.assertIn(log_group_name, result.summary.log)
