import sys, os, pytest
sys.path.insert(0, os.path.abspath("."))
from main.library.utils.core.settings_helper import load_environment, get

def setup_function(function):
    # Create .env files for testing
    os.environ.clear()
    with open('.env.test1.env', 'w') as f:
        f.write('TEST_VARIABLE=test1\n')
    with open('.env.test2.env', 'w') as f:
        f.write('TEST_VARIABLE=test2\n')

def teardown_function(function):
    # Remove .env files after testing
    os.remove('.env.test1.env')
    os.remove('.env.test2.env')

def test_should_load_test1_environment_variables_from_file():
    # Test loading .env.test1.env
    load_environment('test1')
    assert get('TEST_VARIABLE') == 'test1'
    # First variables should not be overwritena
    load_environment('test2')
    assert get('TEST_VARIABLE') == 'test1'

def test_should_load_test2_environment_variables_from_file():
    # Test loading .env.test2.env
    load_environment('test2')
    assert get('TEST_VARIABLE') == 'test2'
    # First variables should not be overwriten
    load_environment('test1')
    assert get('TEST_VARIABLE') == 'test2'

def test_should_raise_exception_for_non_existent_env_file():
    # Test loading non-existent .env file
    with pytest.raises(Exception):
        load_environment('nonexistent')