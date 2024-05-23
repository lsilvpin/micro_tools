import sys, os, pytest
sys.path.insert(0, os.path.abspath("."))

from main.library.di_container import Container
from main.library.tools.core.settings_tool import SettingsTool


container: Container = Container()
settings_tool: SettingsTool = container.settings_tool()

def test_should_read_setting_successfully():
    # Arrange
    key: str = "temp_key"
    value: str = "temp_value"
    settings_tool.set(key, value)
    
    # Act
    readValue: str = settings_tool.get(key)
    
    # Assert
    assert readValue == value
    
    # Cleanup
    settings_tool.delete(key)

def test_should_read_setting_from_env_successfully():
    # Arrange
    key: str = "env"
    
    # Act
    readValue: str = settings_tool.get(key)
    
    # Assert
    assert readValue is not None
    assert len(readValue) > 0
    assert readValue in ["dev", "hml", "prd"]

def test_should_prioritize_env_value_over_file_value():
    # Arrange
    key: str = "env"
    value: str = "temp_value"
    settings_tool.set(key, value)
    
    # Act
    readValue: str = settings_tool.get(key)

    # Assert
    assert readValue is not None
    assert len(readValue) > 0
    assert readValue != value
    assert readValue in ["dev", "hml", "prd"]
    
    # Cleanup
    settings_tool.delete(key)

def test_should_return_none_when_setting_not_found():
    # Arrange
    key: str = "temp_key"
    
    # Act
    readValue: str = settings_tool.get(key)
    
    # Assert
    assert readValue is None

def test_should_crud_setting_successfully():
    # Arrange
    key: str = "temp_key"
    value: str = "temp_value"
    
    # Act
    uncreatedValue: str = settings_tool.get(key)
    assert uncreatedValue is None, "Setting already exists."    
    settings_tool.set(key, value)
    readValue: str = settings_tool.get(key)
    assert readValue == value, "Setting was not created."
    newValue: str = "new_value"
    settings_tool.set(key, newValue)
    updatedValue: str = settings_tool.get(key)
    assert updatedValue == newValue, "Setting was not updated."

    # Cleanup
    settings_tool.delete(key)
    deletedValue: str = settings_tool.get(key)
    assert deletedValue is None, "Setting was not deleted."
    