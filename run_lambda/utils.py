import binascii
import datetime
import os


def random_aws_request_id():
    return "-".join(random_hex(l) for l in [8, 4, 4, 4, 12])


def random_log_stream_name(version):
    today = datetime.date.today()
    return "{t}/[{v}]{h}".format(t=today.strftime("%Y/%m/%d"), v=version,
                                 h=random_hex(32))


def random_hex(length):
    result = binascii.b2a_hex(os.urandom((length + 1) // 2))
    if not isinstance(result, str):
        result = result.decode("ascii")
    if length % 2 == 1:
        return result[:-1]
    return result
