import socket
import sys
import mimetypes
import pathlib
import pdb
import os


def response_ok(body=b"this is a pretty minimal response", mimetype=b"text/plain"):
    """returns a basic HTTP response"""
    resp = []
    resp.append(b"HTTP/1.1 200 OK")
    resp.append(b"Content-Type:" + mimetype)
    resp.append(b"")
    resp.append(body)
    return b"\r\n".join(resp)


def response_method_not_allowed():
    """returns a 405 Method Not Allowed response"""
    resp = []
    resp.append("HTTP/1.1 405 Method Not Allowed")
    resp.append("")
    return "\r\n".join(resp).encode('utf8')


def response_not_found():
    """returns a 404 Not Found response"""
    resp = []
    resp.append("HTTP/1.1 404 Not Found")
    resp.append("")
    return "\r\n".join(resp).encode('utf8')


def parse_request(request):
    first_line = request.split("\r\n", 1)[0]
    method, uri, protocol = first_line.split()
    if method != "GET":
        raise NotImplementedError("We only accept GET")
    return uri


def resolve_uri(uri):
    """This method should return appropriate content and a mime type"""
    mime_type = ''
    content = ''
    # print('the URI is "{}" '.format(uri))
    path = pathlib.Path("webroot{0}".format(uri))
    # print("the path is {}".format(path))
    # pdb.set_trace()
    try:
        if not path.exists():
            # print("path does not exist. A NameError message should be sent.")
            raise NameError
        else:
            # print("path exists")
            if path.is_dir():
                # print("path is a directory.")
                mime_type = 'text/plain'
                # print("directory mime type is: {}".format(mime_type))
                root = "webroot"
                directory = os.listdir(root)
                content = "\n".join(directory).encode('utf8')
                # print("directory contents: {}".format(content))
            else:
                try:
                    # uri = pathlib.Path(uri)
                    mime_type = (mimetypes.types_map[path.suffix])
                    # print('The mime type is "{}".'.format(mime_type))
                    content = path.read_bytes()
                except Exception as e:
                    print("failed to find the mime type with the error {}.".format(str(e)))
                    raise
    except Exception as e:
        # In case of other errors, so I can see them more easily.
        print(str(e))
        raise
    return content, mime_type.encode('utf8')


def server(log_buffer=sys.stderr):
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("making a server on {0}:{1}".format(*address), file=log_buffer)
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print('waiting for a connection', file=log_buffer)
            conn, addr = sock.accept()  # blocking
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)
                request = ''
                while True:
                    data = conn.recv(1024)
                    request += data.decode('utf8')
                    if len(data) < 1024:
                        break

                try:
                    uri = parse_request(request)
                except NotImplementedError:
                    response = response_method_not_allowed()
                else:
                    try:
                        content, mime_type = resolve_uri(uri)
                    except NameError:
                        print("sending NameError.")
                        response = response_not_found()
                    else:
                        response = response_ok(content, mime_type)

                print('sending response', file=log_buffer)
                conn.sendall(response)
            finally:
                conn.close()

    except KeyboardInterrupt:
        sock.close()
        return


if __name__ == '__main__':
    server()
    sys.exit(0)
