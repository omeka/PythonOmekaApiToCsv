import httplib2
import urllib
import mimetypes

class OmekaClient:
    
    def __init__(self, endpoint, key=None):
        self._endpoint = endpoint
        self._key = key
        self._http = httplib2.Http()
    
    def get(self, resource, id=None, query={}):
        return self._request("GET", resource, id=id, query=query)
    
    def post(self, resource, data, query={}, headers={}):
        return self._request("POST", resource, data=data, query=query, headers=headers)
    
    def put(self, resource, id, data, query={}):
        return self._request("PUT", resource, id, data=data, query=query)
    
    def delete(self, resource, id, query={}):
        return self._request("DELETE", resource, id, query=query)
    
    def post_file(self, data, filename, contents):
        """ data is JSON metadata, filename is a string, contents is file contents """
        BOUNDARY = '----------E19zNvXGzXaLvS5C'
        CRLF = '\r\n'
        headers = {'Content-Type': 'multipart/form-data; boundary=' + BOUNDARY}
        L = []
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="data"')
        L.append('')
        L.append(data)
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="file"; filename="%s"' % filename)
        L.append('Content-Type: %s' % self.get_content_type(filename))
        L.append('')
        L.append(contents)
        L.append('--' + BOUNDARY)
        body = CRLF.join(L)
        headers['content-length'] = str(len(body))
        query = {}
        return self.post("files", body, query, headers)
     
    def get_content_type(self, filename):
        """ use mimetypes to detect type of file to be uploaded """
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

    def _request(self, method, resource, id=None, data=None, query=None, headers=None):
        url = self._endpoint + "/" + resource
        if id is not None:
            url += "/" + str(id)
        if self._key is not None:
            query["key"] = self._key
        url += "?" + urllib.urlencode(query)
        resp, content = self._http.request(url, method, body=data, headers=headers)
        return resp, content
