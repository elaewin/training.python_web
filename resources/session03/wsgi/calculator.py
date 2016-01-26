#!/usr/bin/env python
import re
import pdb


def intro_text():
    page = """
    <h1>Online Calculator</h1>
    <p>This page will perform simple calculations, based on your input.</p>
    <p>To use the calculator, enter the type of operation, followed by two 
    numbers, separated by slashes into the page's URL. Accepted operation
    types are: add, subtract, multiply, divide.</p>
    <p>For example: http://localhost:8080/<em><strong>add/4/5</strong></em></p>
    <h3>Your numbers:</h3>
    <p>{a}, {b}</p>
    <h3>Answer:</h3>
    <p>{answer}</p>
    """
    return page


def strip_path(path):
    strippedpath = path.lstrip('/')
    # correct_form = r'^[\w]+/[\d]+/[\d]+$'
    # match = re.match(correct_form, strippedpath)
    # if not match:
    #     raise NameError
    try:
        operation, a, b = strippedpath.split('/')
        return operation, a, b
    except Exception as e:
        raise e


# def incorrect_syntax():
#     answer = "Oops! The calculator didn't understand what you entered in the URL."
#     a = "--"
#     b = "--"
#     return answer, a, b


def perform_calculation(operation, a, b):
    num1 = float(a)
    num2 = float(b)
    try:
        if operation == "add":
            answer = num1 + num2
        elif operation == "subtract":
            answer = num1 - num2
        elif operation == "multiply":
            answer = num1 * num2
        elif operation == "divide":
            try:
                answer = num1 / num2
            except ZeroDivisionError:
                return "No Answer. Cannot divide by zero!"
        else:
            answer = "Unknown calculation type."
        return str(answer)
    except Exception as e:
        return str(e)


def application(environ, start_response):
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        elif len(path) < 2:
            response_body = intro_text().format(a="--", b="--", answer="No answer yet.")
            status = "200 OK"
        else:
            operation, num1, num2 = strip_path(path)
            calc = perform_calculation(operation, num1, num2)
            response_body = intro_text().format(a=num1, b=num2, answer=calc)
            status = "200 OK"
    except NameError:
        status = "404 Not Found"
        response_body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        response_body = "<h1>Internal Server Error</h1>"
    finally:
        response_headers = [('Content-Type', 'text/html'),
                            ('Content-Length', str(len(response_body)))]
        start_response(status, response_headers)

        return [response_body.encode('utf8')]


# def resolve_path(path):
#     # strip the initial slash from the path
#     # pdb.set_trace()
#     strippedpath = path.lstrip('/')
#     # split the path into three elements
#     try:
#         operation, a, b = strippedpath.split('/')
#         num1 = float(a)
#         num2 = float(b)
#     # check the first element of the path for type of operation
#     # perform the operation based on the first element
#         if operation == "add":
#             answer = num1 + num2
#         elif operation == "subtract":
#             answer = num1 - num2
#         elif operation == "multiply":
#             answer = num1 * num2
#         elif operation == "divide":
#             try:
#                 answer = num1 / num2
#             except ZeroDivisionError:
#                 answer = "Cannot divide by zero."
#         return a, b, str(answer)
#     except Exception as e:
#         return str(e)


# def application(environ, start_response):
#     try:
#         path = environ.get('PATH_INFO', None)
#         if path is None:
#             raise NameError
#         num1, num2, calc = resolve_path(path)
#         response_body = intro_text().format(a=num1, b=num2, answer=calc)
#         status = "200 OK"
#     except NameError:
#         status = "404 Not Found"
#         response_body = "<h1>Not Found</h1>"
#     except Exception:
#         status = "500 Internal Server Error"
#         response_body = "<h1>Internal Server Error</h1>"
#     finally:
#         response_headers = [('Content-Type', 'text/html'),
#                             ('Content-Length', str(len(response_body)))]
#         start_response(status, response_headers)

#         return [response_body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()