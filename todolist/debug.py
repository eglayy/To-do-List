import uuid

from django.db import connection


def print_queries(queries):
    tag = uuid.uuid4()
    print(f"[{tag}] SQL PROFILER")
    total_time = 0.0
    total_queries = 0
    for counter, query in enumerate(queries, start=1):
        nice_sql = query["sql"].replace('"', "").replace(",", ", ")
        sql = "\033[1;31m[%s]\033[0m %s" % (query["time"], nice_sql)
        total_time = total_time + float(query["time"])

        # if counter <= 20:
        print(f"[{tag}] {sql}\n")
        total_queries = counter

    print(f"[{tag}] \033[1;32m[" f"TOTAL TIME: {total_time} seconds, QUERIES: {total_queries}" f"]\033[0m")


class SqlPrintingMiddleware(object):
    """
    Middleware which prints out a list of all SQL queries done
    for each view that is processed.  This is only useful for debugging.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if len(connection.queries) > 0:
            print_queries(connection.queries)
        return response
