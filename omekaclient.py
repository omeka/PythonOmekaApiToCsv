# Omeka Client written by Jim Safley
# https://github.com/jimsafley/omeka-client-py

import httplib2
import urllib


class OmekaClient:
    
    def __init__(self, endpoint, key=None):
        self._endpoint = endpoint
        self._key = key
        self._http = httplib2.Http()
    
    def get(self, resource, id=None, query={}):
        return self._request("GET", resource, id=id, query=query)
    
    def post(self, resource, data, query={}):
        return self._request("POST", resource, data=data, query=query)
    
    def put(self, resource, id, data, query={}):
        return self._request("PUT", resource, id, data=data, query=query)
    
    def delete(self, resource, id, query={}):
        return self._request("DELETE", resource, id, query=query)
    
    def _request(self, method, resource, id=None, data=None, query=None):
        url = self._endpoint + "/" + resource
        if id is not None:
            url += "/" + str(id)
        if self._key is not None:
            query["key"] = self._key
        url += "?" + urllib.urlencode(query)
        return self._http.request(url, method, body=data)
