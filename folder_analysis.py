def read_text_file(path):
    """Reads the contents of a UTF-8 text file and returns it as a string."""
    with open(path, "r", encoding="utf-8") as f:
        file_text = f.read()

    return file_text


def write_text_file(path, content):
    """Writes the given string content to a UTF-8 text file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def yeald_list(lst, print_output=True):
    """Yield elements from a list."""
    for c, item in enumerate(lst):
        if print_output:
            print(f"{len(lst) - c} \t| {item}")
        yield item
