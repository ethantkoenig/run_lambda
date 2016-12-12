import argparse
import json

import run_lambda.utils as utils


def arguments():
    parser = argparse.ArgumentParser(description="Generate a template context JSON file")
    parser.add_argument("-o", dest="filename", metavar="OUTPUT_FILENAME",
                        type=str, default=None,
                        help="output file for template, prints to stdout if omitted")
    return parser.parse_args()


def context_json():
    return {
        "function_name": "my_lambda",
        "function_version": "$LATEST",
        "invoked_function_arn": "arn:aws:lambda:region-1:813876719243:function:my_lambda",
        "memory_limit_in_mb": 128,
        "aws_request_id": utils.random_aws_request_id(),
        "log_group_name": "/aws/lambda/my_lambda",
        "log_stream_name": utils.random_log_stream_name("$LATEST"),
        "identity" : {
            "cognito_identity_id": None,
            "cognito_identity_pool_id": None
        },
        "client_context": {
            "client": dict(
                installation_id=None,
                app_title=None,
                app_version_name=None,
                app_version_code=None,
                app_package_name=None,
            ),
            "custom": dict(),
            "env": dict()
        }
    }


def main():
    args = arguments()

    context = context_json()
    if args.filename is not None:
        with open(args.filename, "w") as f:
            json.dump(context, f, indent=2, sort_keys=True)
    else:
        print(json.dumps(context, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
