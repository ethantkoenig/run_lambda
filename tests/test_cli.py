import json
import random
import string
import tempfile
import unittest

import mock
import six

import run_lambda


class RunLambdaCliTest(unittest.TestCase):

    def test_simple(self):
        event = self.make_json_file({"number": 10.0})
        args = self.arguments("tests/square_root.py", event, "handle")
        output = self.call(args)
        self.check_output(output)

    def test_context(self):
        event = self.make_json_file(self.random_dict())
        context_dict = self.random_context()
        context = self.make_json_file(context_dict)
        args = self.arguments("tests/test_cli.py", event, context_filename=context,
                              function_name="print_fields")
        output = self.call(args)
        self.check_output(output)
        for name in context_dict.values():
            if isinstance(name, str):
                self.assertIn(name, output)

    def test_loop(self):
        event = self.make_json_file(self.random_dict())
        args = self.arguments("tests/test_cli.py", event,
                              function_name="loop", timeout_in_seconds=1)
        output = self.call(args)
        self.check_output(output)
        self.assertIn("Timed out", output)

    def test_throw(self):
        event_dict = self.random_dict()
        event_dict.pop("key", None)
        event = self.make_json_file(event_dict)
        args = self.arguments("tests/test_cli.py", event,
                              function_name="throw", timeout_in_seconds=2)
        output = self.call(args)
        self.check_output(output)
        self.assertIn("Raised an exception: ", output)

    # --- helper functions ---

    def check_output(self, output):
        self.assertIsInstance(output, str)
        self.assertIn("Log", output)
        self.assertIn("Max memory used: ", output)
        self.assertIn("START RequestId: ", output)

    @staticmethod
    def make_json_file(data):
        _, tmp_filename = tempfile.mkstemp()
        with open(tmp_filename, "w") as tmp:
            json.dump(data, tmp)
        return tmp_filename

    @staticmethod
    def arguments(filename, event_filename, function_name=None,
                  context_filename=None, timeout_in_seconds=None):
        result = ["run_lambda"]
        if function_name is not None:
            result.append("-f")
            result.append(function_name)
        if context_filename is not None:
            result.append("-c")
            result.append(context_filename)
        if timeout_in_seconds is not None:
            result.append("-t")
            result.append(str(timeout_in_seconds))
        result.append(filename)
        result.append(event_filename)
        return result

    @staticmethod
    def call(arguments):
        output = six.StringIO()
        with mock.patch("sys.stdout", output):
            with mock.patch("sys.argv", arguments):
                run_lambda.__main__.main()
        return str(output.getvalue())

    @staticmethod
    def random_context():
        result = {}
        if random.getrandbits(1):
            result["function_name"] = RunLambdaCliTest.random_string()
        if random.getrandbits(1):
            result["function_version"] = RunLambdaCliTest.random_string()
        if random.getrandbits(1):
            result["invoked_function_arn"] = RunLambdaCliTest.random_string()
        if random.getrandbits(1):
            result["memory_limit_in_mb"] = str(random.randint(100, 200))
        if random.getrandbits(1):
            result["aws_request_id"] = RunLambdaCliTest.random_string()
        if random.getrandbits(1):
            result["log_group_name"] = RunLambdaCliTest.random_string()
        if random.getrandbits(1):
            result["log_stream_name"] = RunLambdaCliTest.random_string()
        if random.getrandbits(1):
            result["identity"] = RunLambdaCliTest.random_identity()
        if random.getrandbits(1):
            result["client_context"] = RunLambdaCliTest.random_client_context()
        return result

    @staticmethod
    def random_identity():
        return {
            "cognito_identity_id": RunLambdaCliTest.random_string(),
            "cognito_identity_pool_id": RunLambdaCliTest.random_string()
        }

    @staticmethod
    def random_client_context():
        return {
            "client": dict(
                installation_id=RunLambdaCliTest.random_string(),
                app_title=RunLambdaCliTest.random_string(),
                app_version_name=RunLambdaCliTest.random_string(),
                app_version_code=RunLambdaCliTest.random_string(),
                app_package_name=RunLambdaCliTest.random_string(),
            ),
            "custom": RunLambdaCliTest.random_dict(),
            "env": RunLambdaCliTest.random_dict()
        }

    @staticmethod
    def random_dict():
        result = {}
        for i in range(random.randint(0, 5)):
            k = RunLambdaCliTest.random_string()
            v = RunLambdaCliTest.random_string()
            result[k] = v
        return result

    @staticmethod
    def random_string():
        length = random.randint(1, 10)
        return "".join(random.choice(string.ascii_letters)
                       for _ in range(length))

# test lambda functions


def print_fields(event, context):
    """
    :param dict event:
    :param run_lambda.MockLambdaContext context:
    :return:
    """
    print(context.function_name)
    print(context.function_version)
    print(context.invoked_function_arn)
    print(context.memory_limit)
    print(context.aws_request_id)
    print(context.log_group_name)
    print(context.log_stream_name)
    print(context.identity)
    print(context.client_context)
    return True


def loop(event, context):
    while True:
        pass


def throw(event, context):
    if "key" not in event:
        raise ValueError(event)
    elif "key2" not in event:
        raise ValueError(event)



if __name__ == "__main__":
    unittest.main()
