import sys
import inspect
from rest_framework.response import Response


def unpredicted_exception_handler(log_type):
    def decorator(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                _, value, traceback = sys.exc_info()
                log_string = '\nTYPE: %s \nFILE: %s \nFUNC: %s \nLINE: %s \nERRR: %s \nINPT: %s' % (log_type, inspect.getfile(
                    func), func.__name__, str(traceback.tb_next.tb_lineno), str(value), str(args) + str(kwargs))
                print(log_string)
                return Response({"Error": str(value)}, 500)
        return inner

    return decorator
