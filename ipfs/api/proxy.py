"""
This modules handles HTTP RPC requests, by exposing them via proxies.
"""

import requests
from io import BytesIO


class ProxyError(Exception):
    """ Raised when the HTTP server returns an error code. """



class Proxy:
    """
    A proxy is a wrapper around an HTTP call to an specific path.

    When you have a ``proxy`` for an path e.g. ``/api/v0/`` you can get the
    proxy for ``/api/v0/block`` either by accessing an attribute ``proxy.block``
    or by accessing an item ``proxy["block"]``.
    """

    def __init__(self, rootProxy, path):
        self.rootProxy = rootProxy
        self.path = path

    def _get(self, name):
        """
        Return a proxy for a child with the given name

        :param name: Name of child
        :return:     Proxy for child
        """
        return Proxy(self.rootProxy, "{}/{}".format(self.path, name))

    def __getattr__(self, name):
        return self._get(name)

    def __getitem__(self, name):
        return self._get(name)

    def __call__(self, *args, _in = None, **opts):
        """
        Call the HTTP RPC method referenced by this proxy. This is done by
        passing the path, arguments, options and input stream to an internal
        method of the root proxy.
        """
        return self.rootProxy._call_endpoint(self.path, args, opts, _in)

    def __repr__(self):
        return "Proxy({!r})".format(self.path)

    def with_inputenc(self, inputenc):
        """
        Return a proxy with the same path, but with the input wrapped with
        the specified encoding.

        :param inputenc: The input encoding that will be applied to any input
                         before sending the HTTP request.
        :return:         A new proxy with the same path but, but with the
                         specified input encoding.
        """
        return InputEncodingProxy(self, inputenc)

    def with_outputenc(self, outputenc):
        """
        Return a proxy with the same path, but with the output wrapped with
        the specified encoding.

        :param outputenc: The output encoding that will be applied to any
                          output before sending the HTTP request.
        :return:          A new proxy with the same path but, but with the
                          specified output encoding.
        """
        return OutputEncodingProxy(self, outputenc)



class InputEncodingProxy(Proxy):
    """
    A proxy that handles input encoding.
    """
    
    def __init__(self, parent, inputenc):
        Proxy.__init__(self, parent.rootProxy, parent.path)
        self.parent = parent
        self.inputenc = inputenc

    def __call__(self, *args, _in = None, **opts):
        if (_in):
            # TODO: jgraef: Replace this with something better
            #
            # todo: mec-is: I will if you first will let me know what this
            # callable is supposed to be doing by writing a decent docstring... (;
            #
            # NOTE: inputenc.dump expects a writable stream for output, but
            # calling a proxy with input expects a readable stream for input.
            # Is there a stream type, which is readable on one end and writable
            # on the other, but doesn't buffer all the data?
            buf = BytesIO()
            _in = self.inputenc.dump(_in, buf)
            buf.seek(0)
            _in = buf
            opts["inputenc"] = self.inputenc.name

        return self.parent(*args, _in = _in, **opts)



class OutputEncodingProxy(Proxy):
    """
    A proxy that handles input encoding.
    """
    def __init__(self, parent, outputenc):
        Proxy.__init__(self, parent.rootProxy, parent.path)
        self.parent = parent
        self.outputenc = outputenc

    def __call__(self, *args, _in = None, **opts):
        opts["encoding"] = self.outputenc.name
        out = self.parent(*args, _in = _in, **opts)
        return self.outputenc.load(out)



class HttpProxy:
    """
    The root proxy which offers the root attribute from which all proxies are
    derived. This class also actually does the work of doing an HTTP request.
    """
    
    ENDPOINT = "/api/v0"
    """ The api endpoint we're using. Currently API v0. """
    
    DEBUG = False
    """ Whether to output debugging information for HTTP requests. """
    
    def __init__(self, host, port):
        """ Create an instance of a HTTPProxy. All method calls will be
            executed through HTTP requests.
        """
        self.base_url = "http://{}:{:d}{}".format(host, port, self.ENDPOINT)
        self.root = Proxy(self, "")
        self.session = requests.Session()


    def _call_endpoint(self, path, args, opts, f_in):
        """
        Actually perform an HTTP request thus calling an HTTP RPC function

        :param path: The path to the RPC function relative to the API endpoint
        
        :param args: Iterable of arguments that will be passed as arguments
                     to the RPC function. This is like passing a normal argument
                     to an ipfs shell command.
                     
        :param opts: A dictionary of options for that RPC call. This is like
                     passing a long option (e.g. --recursive true) to an ipfs
                     shell command.
        
        :param f_in: Optional input stream. This is like piping a file into
                     an ipfs shell command.

        :return:     A readable file-like object with the return data of the
                     RPC call, i.e. the body of the HTTP response.

        :raise: Raises a :py:exc:ProxyError if the server responds with an
                error code
        """

        params = []
        for arg in args:
            if (arg != None):
                params.append(("arg", arg))
        for opt_key, opt_val in opts.items():
            if (opt_val != None):
                params.append((opt_key, str(opt_val)))

        url = self.base_url + path

        # TODO: Support multiple input files
        if (f_in):
            input_files = [("data", ("data", f_in, "application/octet-stream"))]
            method = "POST"
        else:
            input_files = None
            method = "GET"

        if (self.DEBUG):
            print()
            print("Request: {} {}".format(method, "(has body)" if (f_in) else ""))
            print("URL: {}".format(url))
            if (params):
                print("Parameters:")
                for k, v in params:
                    print("  {}: {}".format(k, v))
            print()

        resp = self.session.request(method, url, params = params, files = input_files, stream = True)

        if (resp.status_code != 200):
            raise ProxyError(resp.text)

        if (self.DEBUG):
            print("Response Headers:")
            for k, v in resp.headers.items():
                print("{}: {}".format(k, v))
            print()

        return resp.raw


__all__ = [
    "ProxyError",
    "Proxy",
    "InputEncodingProxy",
    "OutputEncodingProxy",
    "HttpProxy"
]
