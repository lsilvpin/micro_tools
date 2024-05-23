import os


def get_root_dir():
    """
    Returns the root directory of the project by searching for the 'requirements.txt' file in the current directory
    and its parent directories.

    Raises:
        FileNotFoundError: If the 'requirements.txt' file is not found in any parent directory.

    Returns:
        str: The absolute path of the root directory.
    """
    current_dir = os.getcwd()
    while True:
        if os.path.isfile(os.path.join(current_dir, 'requirements.txt')):
            return current_dir
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            raise FileNotFoundError("Could not find requirements.txt in any parent directory.")
        current_dir = parent_dir
