import datetime

from run_lambda import utils


class MockLambdaContext(object):
    def __init__(self,
                 function_name,
                 function_version,
                 invoked_function_arn,
                 memory_limit_in_mb,
                 aws_request_id,
                 log_group_name,
                 log_stream_name,
                 identity=None,
                 client_context=None,
                 default_remaining_time_in_millis=None):
        self._function_name = function_name
        self._function_version = function_version
        self._invoked_function_arn = invoked_function_arn
        self._memory_limit_in_mb = memory_limit_in_mb
        self._aws_request_id = aws_request_id
        self._log_group_name = log_group_name
        self._log_stream_name = log_stream_name
        self._identity = identity
        self._client_context = client_context

        self._default_remaining_time_in_millis = default_remaining_time_in_millis
        self._expiration = None

    @property
    def function_name(self):
        """
        :property: Name of function
        :type: str
        """
        return self._function_name

    @property
    def function_version(self):
        """
        :property: version of Lambda function that is executing
        :rtype: str
        """
        return self._function_version

    @property
    def invoked_function_arn(self):
        """
        :property: ARN used to invoke function
        :rtype: str
        """
        return self._invoked_function_arn

    @property
    def memory_limit(self):
        """
        :property: Memory limit, in MB, as a string
        :rtype: str
        """
        return self._memory_limit_in_mb

    @property
    def aws_request_id(self):
        """
        :property: AWS request id associated with invocation
        :rtype: str
        """
        return self._aws_request_id

    @property
    def log_group_name(self):
        """
        :property: Name of CloudWatch log group where logs are written
        :rtype: str
        """
        return self._log_group_name

    @property
    def log_stream_name(self):
        """
        :property: Name of CloudWatch log stream where logs are written
        :rtype: str
        """
        return self._log_stream_name

    @property
    def identity(self):
        """
        :property: Cognito identity provider. May be ``None``.
        :rtype: MockCognitoIdentity
        """
        return self._identity

    @property
    def client_context(self):
        """
        :property: Information about client application and device when invoked
            via AWS Mobile SDK. May be ``None``.
        :rtype: MockClientContext
        """
        return self._client_context

    def activate(self, timeout_in_seconds):
        """
        :param int timeout_in_seconds:
        """
        self._expiration = datetime.datetime.now() + datetime.timedelta(seconds=timeout_in_seconds)

    def get_remaining_time_in_millis(self):
        """
        Returns remaining execution time, in milliseconds. Should be called
        inside of Lambda function.

        :return: Remaining execution time, in milliseconds
        :rtype: int
        """
        if self._expiration is None:  # if not activated
            default = self._default_remaining_time_in_millis
            return default if default is not None else 1000
        diff = self._expiration - datetime.datetime.now()
        remaining_seconds = diff.total_seconds()
        return max(int(1000 * remaining_seconds), 0)

    @staticmethod
    def of_json(json):
        builder = MockLambdaContext.Builder()
        if "function_name" in json:
            builder.set_function_name(json["function_name"])
        if "function_version" in json:
            builder.set_function_version(json["function_version"])
        if "invoked_function_arn" in json:
            builder.set_invoked_function_arn(json["invoked_function_arn"])
        if "memory_limit_in_mb" in json:
            builder.set_memory_limit_in_mb(json["memory_limit_in_mb"])
        if "aws_request_id" in json:
            builder.set_aws_request_id(json["aws_request_id"])
        if "log_group_name" in json:
            builder.set_log_group_name(json["log_group_name"])
        if "log_stream_name" in json:
            builder.set_log_stream_name(json["log_stream_name"])
        if "identity" in json:
            identity = MockCognitoIdentity.of_json(json["identity"])
            builder.set_identity(identity)
        if "client_context" in json:
            client_context = MockClientContext.of_json(json["client_context"])
            builder.set_client_context(client_context)
        if "default_remaining_time_in_millis" in json:
            builder.set_default_remaining_time_in_millis(
                json["default_remaining_time_in_millis"])
        return builder.build()

    class Builder(object):
        def __init__(self):
            """
            Initializes each context field to a reasonable default
            """
            self._function_name = "function_name"
            self._function_version = "$LATEST"
            self._invoked_function_arn = None
            self._memory_limit_in_mb = "256"
            self._aws_request_id = utils.random_aws_request_id()
            self._log_group_name = None
            self._log_stream_name = None
            self._identity = None
            self._client_context = None
            self._default_remaining_time_in_millis = None

        def build(self):
            """
            Constructs and returns a
            :class:`MockLambdaContext <run_lambda.MockLambdaContext>` instance
            represented by the called builder object.

            :return: A newly constructed context object
            :rtype: MockLambdaContext
            """
            if self._invoked_function_arn is None:
                self._invoked_function_arn = \
                    "arn:aws:lambda:us-east-1:813876719243:function:" + self._function_name
            if self._log_group_name is None:
                self._log_group_name = "/aws/lambda/"+self._function_name
            if self._log_stream_name is None:
                self._log_stream_name = utils.random_log_stream_name(self._function_version)

            return MockLambdaContext(
                function_name=self._function_name,
                function_version=self._function_version,
                invoked_function_arn=self._invoked_function_arn,
                memory_limit_in_mb=self._memory_limit_in_mb,
                aws_request_id=self._aws_request_id,
                log_group_name=self._log_group_name,
                log_stream_name=self._log_stream_name,
                identity=self._identity,
                client_context=self._client_context,
                default_remaining_time_in_millis=self._default_remaining_time_in_millis
            )

        def set_function_name(self, function_name):
            """
            :param str function_name: name of Lambda function
            :return: the updated builder
            :rtype: MockLambdaContext.Builder
            """
            self._function_name = function_name
            return self

        def set_function_version(self, function_version):
            """
            :param str function_version: version of executing Lambda function
            :return: the updated builder
            :rtype: MockLambdaContext.Builder
            """
            self._function_version = function_version
            return self

        def set_invoked_function_arn(self, invoked_function_arn):
            """
            :param str invoked_function_arn: ARN used to invoke function
            :return: the updated builder
            :rtype: MockLambdaContext.Builder
            """
            self._invoked_function_arn = invoked_function_arn
            return self

        def set_memory_limit_in_mb(self, memory_limit_in_mb):
            """
            :param str memory_limit_in_mb: Memory limit, in megabytes, as a
                string
            :return: the updated builder
            :rtype: MockLambdaContext.Builder
            """
            self._memory_limit_in_mb = memory_limit_in_mb
            return self

        def set_aws_request_id(self, aws_request_id):
            """
            :param str aws_request_id: AWS request id associated with invocation
            :return: the updated builder
            :rtype: MockLambdaContext.Builder
            """
            self._aws_request_id = aws_request_id
            return self

        def set_log_group_name(self, log_group_name):
            """
            :param str log_group_name: Name of CloudWatch log group where logs
                are written
            :return: the updated builder
            :rtype: MockLambdaContext.Builder
            """
            self._log_group_name = log_group_name
            return self

        def set_log_stream_name(self, log_stream_name):
            """
            :param str log_stream_name: Name of CloudWatch log stream where logs
                are written
            :return: the updated builder
            :rtype: MockLambdaContext.Builder
            """
            self._log_stream_name = log_stream_name
            return self

        def set_identity(self, identity):
            """
            :param MockCognitoIdentity identity: Cognito identity provider
            :return: the updated builder
            :rtype: MockLambdaContext.Builder
            """
            self._identity = identity
            return self

        def set_client_context(self, client_context):
            """
            :param MockClientContext client_context: Information about client
                application and device
            :return: the updated builder
            :rtype: MockLambdaContext.Builder
            """
            self._client_context = client_context
            return self

        def set_default_remaining_time_in_millis(self, default_remaining_time_in_millis):
            """
            Sets a default value that will be returned from the
            :meth:`~run_lambda.MockLambdaContext.get_remaining_time_in_millis`
            method of the built :class:`MockLambdaContext` value if a Lambda
            function is called without a timeout.

            :param int default_remaining_time_in_millis: default value
            :return: the updated builder
            :rtype: MockLambdaContext.Builder
            """
            self._default_remaining_time_in_millis = default_remaining_time_in_millis
            return self


class MockCognitoIdentity(object):
    def __init__(self, identity_id=None, identity_pool_id=None):
        self._identity_id = identity_id
        self._identity_pool_id = identity_pool_id

    @property
    def cognito_identity_id(self):
        """
        :property: AWS Cognito identity id. May be ``None``
        :rtype: str
        """
        return self._identity_id

    @property
    def cognito_identity_pool_id(self):
        """
        :property: AWS Cognito identity pool id. May be ``None``.
        :rtype: str
        """
        return self._identity_pool_id

    @staticmethod
    def of_json(json):
        return MockCognitoIdentity(
            identity_id=json.get("cognito_identity_id", None),
            identity_pool_id=json.get("cognito_identity_pool_id", None)
        )


class MockClientContext(object):
    def __init__(self, client, custom=None, env=None):
        self._client = client
        self._custom = custom if custom is not None else {}
        self._env = env if env is not None else {}

    @property
    def client(self):
        """
        :property: Information about client
        :rtype: MockClientContext.Client
        """
        return self._client

    @property
    def custom(self):
        """
        :property: Dictionary of custom values set by client application
        :rtype: dict
        """
        return self._custom

    @property
    def env(self):
        """
        :property: Dictionary of environment information provided by AWS Mobile
            SDK
        :rtype: dict
        """
        return self._env

    @staticmethod
    def of_json(json):
        if "client" in json:
            client = MockClientContext.Client.of_json(json["client"])
        else:
            client = None
        return MockClientContext(
            client=client,
            custom=json.get("custom", {}),
            env=json.get("env", {})
        )

    class Client(object):
        def __init__(self, installation_id, app_title, app_version_name,
                     app_version_code, app_package_name):
            self._installation_id = installation_id
            self._app_title = app_title
            self._app_version_name = app_version_name
            self._app_version_code = app_version_code
            self._app_package_name = app_package_name

        @property
        def installation_id(self):
            """
            :property: Installation id
            :rtype: str
            """
            return self._installation_id

        @property
        def app_title(self):
            """
            :property: App title
            :rtype: str
            """
            return self._app_title

        @property
        def app_version_name(self):
            """
            :property: App version name
            :rtype: str
            """
            return self._app_version_name

        @property
        def app_version_code(self):
            """
            :property: App version code
            :rtype: str
            """
            return self._app_version_code

        @property
        def app_package_name(self):
            """
            :property: App package name
            :rtype: str
            """
            return self._app_package_name

        @staticmethod
        def of_json(json):
            return MockClientContext.Client(
                installation_id=json.get("installation_id", None),
                app_title=json.get("app_title", None),
                app_version_name=json.get("app_version_name", None),
                app_version_code=json.get("app_version_code", None),
                app_package_name=json.get("app_package_name", None)
            )
