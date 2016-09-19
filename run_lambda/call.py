import logging
import mock
import multiprocessing
import memory_profiler
import signal
import timeit
import traceback
from six import StringIO

import sys

from run_lambda import context as context_module


def run_lambda(handle, event, context=None, timeout_in_seconds=None, patches=None):
    """
    Run the Lambda function ``handle``, with the specified arguments and
    parameters.

    :param function handle: Lambda function to call
    :param dict event: dictionary containing event data
    :param MockLambdaContext context: context object. If not provided, a
        default context object will be used.
    :param int timeout_in_seconds: timeout in seconds. If not provided, the
        function will be called with no timeout
    :param dict patches: dictionary of name-to-value mappings that will be
        patched inside the Lambda function
    :return: value returned by Lambda function
    :rtype: LambdaResult
    """
    if context is None:
        context = context_module.MockLambdaContext.Builder().build()

    patches_list = [] if patches is None \
        else [mock.patch(name, value) for name, value in patches.items()]
    for patch in patches_list:
        patch.start()

    setup_timeout(context, timeout_in_seconds)

    builder = None
    result = None
    try:
        builder = LambdaCallSummary.Builder(context)
        value = handle(event, context)
        result = LambdaResult(builder.build(), value=value)
    except LambdaTimeout:
        result = LambdaResult(builder.build(), timed_out=True)
    except Exception as e:
        traceback.print_exc(file=builder.log)
        result = LambdaResult(builder.build(), exception=e)
    finally:
        signal.alarm(0)  # disable any pending alarms
        for patch in patches_list:
            patch.stop()
        return result


def setup_timeout(context, timeout_in_seconds=None):
    if timeout_in_seconds is not None:
        def on_timeout(signum, frame):
            raise LambdaTimeout()
        signal.signal(signal.SIGALRM, on_timeout)
        signal.alarm(timeout_in_seconds)
        context.activate(timeout_in_seconds)


class LambdaTimeout(Exception):
    pass


class LambdaResult(object):
    """
    Represents the result of locally running a Lambda function.
    """
    def __init__(self, summary, value=None, timed_out=False, exception=None):
        self._summary = summary
        self._value = value
        self._timed_out = timed_out
        self._exception = exception

    @property
    def summary(self):
        """
        :property: Summary of call to Lambda function
        :rtype: LambdaCallSummary
        """
        return self._summary

    @property
    def value(self):
        """
        :property: The value returned by the call to the Lambda function, or
            ``None`` if no value was returned.
        :rtype: any
        """
        return self._value

    @property
    def timed_out(self):
        """
        :property: Whether the call to the Lambda function timed out
        :rtype: bool
        """
        return self._timed_out

    @property
    def exception(self):
        """
        :property: The exception raised by the call to the Lambda function, or
            ``None`` if no exception was raised
        :rtype: Exception
        """
        return self._exception

    def __str__(self):
        return "{{summary={s}; value={v}; timed_out={t}; exception={e}}}"\
            .format(s=str(self._summary), v=self._value,
                    t=self._timed_out, e=repr(self._exception))

    def display(self, outfile=sys.stdout):
        if self._timed_out:
            outfile.write("Timed out\n\n")
        elif self._exception is not None:
            outfile.write("Raised an exception: {}\n\n".format(repr(self._exception)))
        else:
            outfile.write("Returned value {}\n\n".format(self._value))
        self._summary.display(outfile=outfile)


class LambdaCallSummary(object):
    def __init__(self, duration_in_millis, max_memory_used_in_mb, log):
        self._duration_in_millis = duration_in_millis
        self._max_memory_used_in_mb = max_memory_used_in_mb
        self._log = log

    @property
    def duration_in_millis(self):
        """
        Duration of call, in milliseconds. This value may vary from the
        duration the call would have taken if actually run in AWS.

        :property: Duration of call, in milliseconds
        :rtype: int
        """
        return self._duration_in_millis

    @property
    def max_memory_used_in_mb(self):
        """
        Maximum amount of memory used during call to Lambda function,
        in megabytes. This value is an estimate of how much memory the call
        would have used if actually run in AWS. We have found that these
        estimates are almost always within 5MB of the amount of memory used by
        corresponding remote calls.

        :property: Maximum amount of memory used during call to Lambda function,
            in megabytes.
        :rtype: int
        """
        return self._max_memory_used_in_mb

    @property
    def log(self):
        """
        :property: The contents of the log for this lambda function.
        :rtype: str
        """
        return self._log

    def __str__(self):
        return "{{duration={d} milliseconds; max_memory={m} MB; log={l}}}"\
            .format(d=self._duration_in_millis,
                    m=self._max_memory_used_in_mb,
                    l=repr(self._log))

    def display(self, outfile=sys.stdout):
        outfile.write("Duration: {} ms\n\n".format(self._duration_in_millis))
        outfile.write("Max memory used: {} MB\n\n"
                      .format(self._max_memory_used_in_mb))
        outfile.write("Log:\n")
        outfile.write(self._log)

    class Builder(object):
        def __init__(self, context):
            self._context = context

            self._start_time = timeit.default_timer()
            self._start_mem = memory_profiler.memory_usage()[0]

            self._log = StringIO()
            self._log.write("START RequestId: {r} Version: {v}\n".format(
                r=context.aws_request_id, v=context.function_version
            ))
            self._previous_stdout = sys.stdout

            handler = logging.StreamHandler(stream=self._log)
            logging.getLogger().addHandler(handler)
            sys.stdout = self._log

        def build(self):
            end_time = timeit.default_timer()
            end_mem = memory_profiler.memory_usage()[0]

            sys.stdout = self._previous_stdout

            self._log.write("END RequestId: {r}\n".format(
                r=self._context.aws_request_id))

            duration_in_millis = int(1000 * (end_time - self._start_time))
            # The memory overhead of setting up the AWS Lambda environment
            # (when actually run in AWS) is roughly 14 MB
            max_memory_used_in_mb = (end_mem - self._start_mem) / 1048576 + 14

            self._log.write(
                "REPORT RequestId: {r}\tDuration: {d} ms\t"
                "Max Memory Used: {m} MB\n"
                .format(r=self._context.aws_request_id,
                        d=duration_in_millis,
                        m=max_memory_used_in_mb))

            log = self._log.getvalue()
            return LambdaCallSummary(duration_in_millis, max_memory_used_in_mb, log)

        @property
        def log(self):
            return self._log
