import sys, os, pytest
sys.path.insert(0, os.path.abspath("."))
from main.library.di_container import Container
from main.library.tools.core.log_tool import LogTool

container = Container()
log_tool = container.log_tool()

def test_should_info(capsys):
    log_tool.info("This is an informational message")
    captured = capsys.readouterr()
    assert "This is an informational message" in captured.out

def test_should_warn(capsys):
    log_tool.warn("This is a warning message")
    captured = capsys.readouterr()
    assert "This is a warning message" in captured.out

def test_should_error(capsys):
    log_tool.error("This is an error message")
    captured = capsys.readouterr()
    assert "This is an error message" in captured.err
