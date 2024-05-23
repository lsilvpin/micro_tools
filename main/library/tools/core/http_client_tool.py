import sys, os
sys.path.insert(0, os.path.abspath("."))
import http.client
from main.library.tools.core.log_tool import LogTool
from main.library.tools.core.settings_tool import SettingsTool


class HttpClientTool:
    def __init__(self, settings_tool: SettingsTool, log_tool: LogTool):
        self.settings_tool = settings_tool
        self.log_tool = log_tool
    
    def get(self, url: str) -> bytes:
        assert url is not None, "URL cannot be None"
        assert url.startswith("http://") or url.startswith("https://"), "URL must start with 'http://' or 'https://'"
        isHttps: bool = url.startswith("https://")
        hostWithPort: str = url.split("/")[2]
        host: str = hostWithPort.split(":")[0]
        hasPort: bool = ":" in hostWithPort
        port: str = "80" if not isHttps else "443"
        if hasPort:
            port = hostWithPort.split(":")[1] 
        if port == "":
            port = "443" if isHttps else "80"
        uri: str = url.split(hostWithPort)[1]
        conn = http.client.HTTPSConnection(host, port) if isHttps else http.client.HTTPConnection(host, port)
        assert conn is not None, "Connection cannot be None"
        conn.request("GET", uri)
        response = conn.getresponse()
        assert response is not None, "Response cannot be None"
        status_code: int = response.status
        response_data: bytes = response.read()
        self.__validate_response(status_code, response.reason, response_data)
        return response_data
    
    def post(self, url: str, data: str) -> bytes:
        assert url is not None, "URL cannot be None"
        assert url.startswith("http://") or url.startswith("https://"), "URL must start with 'http://' or 'https://'"
        isHttps: bool = url.startswith("https://")
        hostWithPort: str = url.split("/")[2]
        host: str = hostWithPort.split(":")[0]
        hasPort: bool = ":" in hostWithPort
        port: str = "80" if not isHttps else "443"
        if hasPort:
            port = hostWithPort.split(":")[1] 
        if port == "":
            port = "443" if isHttps else "80"
        uri: str = url.split(hostWithPort)[1]
        conn = http.client.HTTPSConnection(host, port) if isHttps else http.client.HTTPConnection(host, port)
        assert conn is not None, "Connection cannot be None"
        conn.request("POST", uri, data)
        response = conn.getresponse()
        assert response is not None, "Response cannot be None"
        status_code: int = response.status
        response_data: bytes = response.read()
        self.__validate_response(status_code, response.reason, response_data)
        return response_data
    
    def put(self, url: str, data: str) -> bytes:
        assert url is not None, "URL cannot be None"
        assert url.startswith("http://") or url.startswith("https://"), "URL must start with 'http://' or 'https://'"
        isHttps: bool = url.startswith("https://")
        hostWithPort: str = url.split("/")[2]
        host: str = hostWithPort.split(":")[0]
        hasPort: bool = ":" in hostWithPort
        port: str = "80" if not isHttps else "443"
        if hasPort:
            port = hostWithPort.split(":")[1] 
        if port == "":
            port = "443" if isHttps else "80"
        uri: str = url.split(hostWithPort)[1]
        conn = http.client.HTTPSConnection(host, port) if isHttps else http.client.HTTPConnection(host, port)
        assert conn is not None, "Connection cannot be None"
        conn.request("PUT", uri, data)
        response = conn.getresponse()
        assert response is not None, "Response cannot be None"
        status_code: int = response.status
        response_data: bytes = response.read()
        self.__validate_response(status_code, response.reason, response_data)
        return response_data
    
    def delete(self, url: str) -> bytes:
        assert url is not None, "URL cannot be None"
        assert url.startswith("http://") or url.startswith("https://"), "URL must start with 'http://' or 'https://'"
        isHttps: bool = url.startswith("https://")
        hostWithPort: str = url.split("/")[2]
        host: str = hostWithPort.split(":")[0]
        hasPort: bool = ":" in hostWithPort
        port: str = "80" if not isHttps else "443"
        if hasPort:
            port = hostWithPort.split(":")[1] 
        if port == "":
            port = "443" if isHttps else "80"
        uri: str = url.split(hostWithPort)[1]
        conn = http.client.HTTPSConnection(host, port) if isHttps else http.client.HTTPConnection(host, port)
        assert conn is not None, "Connection cannot be None"
        conn.request("DELETE", uri)
        response = conn.getresponse()
        assert response is not None, "Response cannot be None"
        status_code: int = response.status
        response_data: bytes = response.read()
        self.__validate_response(status_code, response.reason, response_data)
        return response_data
    
    def __validate_response(self, status_code: int, reason: str, response_data: bytes):
        if status_code < 200:
            if reason is not None and reason != "":
                if response_data is not None and response_data != b"":
                    raise Exception(f"Request failed with status code {status_code}, reason {reason}, and response data {response_data}")
                else:
                    raise Exception(f"Request failed with status code {status_code} and reason {reason}")
            else:
                raise Exception(f"Request failed with status code {status_code}")