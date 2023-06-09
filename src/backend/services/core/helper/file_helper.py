def read_file(file: str) -> str:
    """
    The function reads the contents of a file and returns it as a string.

    Args:
      file (str): The parameter "file" is a string that represents the file path of the file that needs
    to be read.

    Returns:
      The function `read_file` is returning the contents of the file as a string.
        If file does not exist then return None.
    """
    try:
        f = open(file, 'r')
        return f.read()
    except IOError:
        return None


def write_file(file: str, content: str):
    """
    The function writes the given content to a file with the specified name.

    Args:
      file (str): The file parameter is a string that represents the name or path of the file that we
    want to write to.
      content (str): The content parameter is a string that represents the text that will be written to
    the file.
    """
    with open(file, 'w') as f:
        f.write(content)
