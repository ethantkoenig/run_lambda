import argparse
import imp
import json
import os
import sys

from run_lambda import run_lambda

def arguments():
    parser = argparse.ArgumentParser(description="Run AWS Lambda function locally")
    parser.add_argument("filename", type=str,
                        help="name of file containing Lambda function")
    parser.add_argument("event", type=str,
                        help="filename of file containing JSON event data")
    parser.add_argument("-f", "--function", metavar="HANDLER_FUNCTION",
                        dest="function_name", type=str, default="handler",
                        help="Name of handler function. Defaults to \"handler\"")
    parser.add_argument("-t", "--timeout", metavar="TIMEOUT",
                        dest="timeout", type=int, default=None,
                        help="Timeout (in seconds) for function call. If not provided, "
                             "no timeout will be used.")
    return parser.parse_args()


def load_module(filepath):
    abspath = os.path.abspath(filepath)
    sys.path.insert(0, os.path.dirname(abspath))

    basename = os.path.basename(abspath)
    module_name, extension = os.path.splitext(basename)
    module_info = imp.find_module(module_name)
    sys.path.pop(0)
    return imp.load_module(module_name, *module_info)


def main():
    args = arguments()

    with open(args.event) as event_file:
        event = json.load(event_file)

    module = load_module(args.filename)
    function = getattr(module, args.function_name)
    result = run_lambda(function, event, timeout_in_seconds=args.timeout)
    result.display()

if __name__ == "__main__":
    main()
