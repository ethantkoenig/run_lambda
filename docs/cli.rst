

Command Line Interface
======================

The ``run_lambda`` package also offers a command-line tool for running Lambda
functions::

    $ run_lambda path/to/main.py path/to/event.json

Installing the ``run_lambda`` package from the Python Package Index
(i.e. via ``pip``) should automatically add the tool to your path. For
information on how to use the tool, run ``run_lambda --help``::

    $ run_lambda --help
    usage: run_lambda [-h] [-f HANDLER_FUNCTION] [-t TIMEOUT]
                      [-c CONTEXT_FILENAME]
                      filename event

    Run AWS Lambda function locally

    positional arguments:
      filename              name of file containing Lambda function
      event                 name of file containing JSON event data

    optional arguments:
      -h, --help            show this help message and exit
      -f HANDLER_FUNCTION, --function HANDLER_FUNCTION
                            Name of handler function. Defaults to "handler"
      -t TIMEOUT, --timeout TIMEOUT
                            Timeout (in seconds) for function call. If not
                            provided, no timeout will be used.
      -c CONTEXT_FILENAME, --context CONTEXT_FILENAME
                            Filename of file containing JSON context data

Context JSON
------------


The context JSON data can include the following fields::

    {
      "aws_request_id": "bf77967d-c53a-5659-9d91-2417e2a3ee58",
      "client_context": {
        "client": {
          "app_package_name": null,
          "app_title": null,
          "app_version_code": null,
          "app_version_name": null,
          "installation_id": null
        },
        "custom": {},
        "env": {}
      },
      "function_name": "my_lambda",
      "function_version": "$LATEST",
      "identity": {
        "cognito_identity_id": null,
        "cognito_identity_pool_id": null
      },
      "invoked_function_arn": "arn:aws:lambda:region-1:813876719243:function:my_lambda",
      "log_group_name": "/aws/lambda/my_lambda",
      "log_stream_name": "2016/12/11/[$LATEST]6ac39f0272c07aa3cd548e6d5a9e8881",
      "memory_limit_in_mb": 128
    }

Any fields that are not present in the provided context JSON will be populated
with default values. Any invalid fields (i.e. any fields other than the ones
listed above) are ignored.


To generate a template context data JSON file like the one shown above, use the
``run_lambda_context_template`` command. For information on how to use the
command, run ``run_lambda_context_template --help``::

    $ run_lambda_context_template --help
    usage: run_lambda_context_template [-h] [-o OUTPUT_FILENAME]

    Generate a template context JSON file

    optional arguments:
      -h, --help          show this help message and exit
      -o OUTPUT_FILENAME  output file for template, prints to stdout if omitted
