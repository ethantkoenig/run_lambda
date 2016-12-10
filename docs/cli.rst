

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
      event                 filename of file containing JSON event data

    optional arguments:
      -h, --help            show this help message and exit
      -f HANDLER_FUNCTION, --function HANDLER_FUNCTION
                            Name of handler function. Defaults to "handler"
      -t TIMEOUT, --timeout TIMEOUT
                            Timeout (in seconds) for function call. If not
                            provided, no timeout will be used.
      -c CONTEXT_FILENAME, --context CONTEXT_FILENAME
                            Filename of file containing JSON context data

To generate a template context data JSON file, use the ``run_lambda_context_template``
command. For information on how to use it, run ``run_lambda_context_template --help``::

    $ run_lambda_context_template --help
    usage: run_lambda_context_template [-h] [-o OUTPUT_FILENAME]

    Generate a template context JSON file

    optional arguments:
      -h, --help          show this help message and exit
      -o OUTPUT_FILENAME  output file for template, prints to stdout if omitted
