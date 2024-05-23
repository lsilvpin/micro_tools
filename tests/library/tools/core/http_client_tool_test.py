import sys, os, pytest
sys.path.insert(0, os.path.abspath("."))

from main.library.di_container import Container
from main.library.tools.core.http_client_tool import HttpClientTool

container: Container = Container()
http_client_tool: HttpClientTool = container.http_client_tool()

def test_should_simulate_get_with_pytest_mock(mocker):
    # Mocks
    successResponse = mocker.Mock()
    successResponse.status = 200
    successResponse.read.return_value = b"Response data"
    conn = mocker.Mock()
    conn.getresponse.return_value = successResponse
    mocker.patch("http.client.HTTPConnection", return_value=conn)
    
    # Arrange
    url = "http://example.com"
    
    # Act
    response: bytes = http_client_tool.get(url)

    # Assert
    assert response is not None, "Response data should not be None"    
    assert len(response) > 0, "Response data should not be empty"
    assert response == b"Response data", "Response data should be 'Response data'" 

def test_should_simulate_post_with_pytest_mock(mocker):
    # Mocks
    successResponse = mocker.Mock()
    successResponse.status = 200
    successResponse.read.return_value = b"Response data"
    conn = mocker.Mock()
    conn.getresponse.return_value = successResponse
    mocker.patch("http.client.HTTPConnection", return_value=conn)
    
    # Arrange
    url = "http://example.com"
    data = "Request data"
    
    # Act
    response: bytes = http_client_tool.post(url, data)

    # Assert
    assert response is not None, "Response data should not be None"    
    assert len(response) > 0, "Response data should not be empty"
    assert response == b"Response data", "Response data should be 'Response data'"

def test_should_simulate_put_with_pytest_mock(mocker):
    # Mocks
    successResponse = mocker.Mock()
    successResponse.status = 200
    successResponse.read.return_value = b"Response data"
    conn = mocker.Mock()
    conn.getresponse.return_value = successResponse
    mocker.patch("http.client.HTTPConnection", return_value=conn)
    
    # Arrange
    url = "http://example.com"
    data = "Request data"
    
    # Act
    response: bytes = http_client_tool.put(url, data)

    # Assert
    assert response is not None, "Response data should not be None"    
    assert len(response) > 0, "Response data should not be empty"
    assert response == b"Response data", "Response data should be 'Response data'"

def test_should_simulate_delete_with_pytest_mock(mocker):
    # Mocks
    successResponse = mocker.Mock()
    successResponse.status = 200
    successResponse.read.return_value = b"Response data"
    conn = mocker.Mock()
    conn.getresponse.return_value = successResponse
    mocker.patch("http.client.HTTPConnection", return_value=conn)
    
    # Arrange
    url = "http://example.com"
    
    # Act
    response: bytes = http_client_tool.delete(url)

    # Assert
    assert response is not None, "Response data should not be None"    
    assert len(response) > 0, "Response data should not be empty"
    assert response == b"Response data", "Response data should be 'Response data'"