import os
from tqdm import tqdm

def read_file(path):
    """Reads the contents of a UTF-8 text file and returns it as a string."""
    with open(path, "r", encoding="utf-8") as f:
        file_text = f.read()

    return file_text


def write_file(path, content):
    """Writes the given string content to a UTF-8 text file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def create_folder(path):
    os.makedirs(path, exist_ok=True)


def yeald_list(lst, print_output=True):
    """Yield elements from a list."""
    for c, item in enumerate(lst):
        if print_output:
            print(f"{len(lst) - c} \t| {item}")
        yield item

def tqdm_list(lst, print_output=True):
    """Yield elements from a list."""
    for item in tqdm(lst):
        yield item
