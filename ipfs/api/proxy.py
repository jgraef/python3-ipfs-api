import requests
from io import BytesIO


class ProxyError(Exception):
    pass


class Proxy:
    def __init__(self, rootProxy, path):
        self.rootProxy = rootProxy
        self.path = path

    def __get(self, name):
        return Proxy(self.rootProxy, "{}/{}".format(self.path, name))

    def __getattr__(self, name):
        return self.__get(name)

    def __getitem__(self, name):
        return self.__get(name)

    def __call__(self, *args, _in = None, **opts):
        return self.rootProxy._call_endpoint(self.path, args, opts, _in)

    def __repr__(self):
        return "Proxy({!r})".format(self.path)

    def with_inputenc(self, inputenc):
        return InputEncodingProxy(self, inputenc)

    def with_outputenc(self, outputenc):
        return OutputEncodingProxy(self, outputenc)



class InputEncodingProxy(Proxy):
    def __init__(self, parent, inputenc):
        Proxy.__init__(self, parent.rootProxy, parent.path)
        self.parent = parent
        self.inputenc = inputenc

    def __call__(self, *args, _in = None, **opts):
        if (_in):
            # TODO: Replace this with something better
            buf = BytesIO()
            _in = self.inputenc.dump(_in, buf)
            buf.seek(0)
            _in = buf
            opts["inputenc"] = self.inputenc.name

        return self.parent(*args, _in = _in, **opts)



class OutputEncodingProxy(Proxy):
    def __init__(self, parent, outputenc):
        Proxy.__init__(self, parent.rootProxy, parent.path)
        self.parent = parent
        self.outputenc = outputenc

    def __call__(self, *args, _in = None, **opts):
        opts["encoding"] = self.outputenc.name
        out = self.parent(*args, _in = _in, **opts)
        return self.outputenc.load(out)



class HttpProxy:
    ENDPOINT = "/api/v0"
    
    def __init__(self, host, port):
        self.base_url = "http://{}:{:d}{}".format(host, port, self.ENDPOINT)
        self.root = Proxy(self, "")


    def _call_endpoint(self, path, args, opts, f_in):
        params = []
        for arg in args:
            params.append(("arg", arg))
        for opt_key, opt_val in opts.items():
            params.append((opt_key, opt_val))

        url = self.base_url + path

        # TODO: Support multiple input files
        if (f_in):
            input_files = [("data", ("data", f_in, "application/octet-stream"))]
            method = "POST"
        else:
            input_files = None
            method = "GET"

        print()
        print("Request: {} {}".format(method, "(has body)" if (f_in) else ""))
        print("URL: {}".format(url))
        if (params):
            print("Parameters:")
            for k, v in params:
                print("  {}: {}".format(k, v))
        print()

        resp = requests.request(method, url, params = params, files = input_files, stream = True)

        if (resp.status_code != 200):
            raise ProxyError(resp.text)

        print("Response Headers:")
        for k, v in resp.headers.items():
            print("{}: {}".format(k, v))
        print()

        return resp.raw


    def _encode_input(self, input_data, inputenc):
        if (inputenc):
            print("Encoding as {}".format(encoding))
            body, inputenc_headers = inputenc.dump(input_data)
        return body


    def _decode_output(self, resp, outputenc):
        if (encoding):
            print("Decoding as {}".format(encoding))
            return outputenc.load(resp, headers)
        else:
            return resp
        
