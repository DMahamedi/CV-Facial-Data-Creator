import re
import os


def get_max_counter(folder_path: str, filetype: str = 'jpg') -> int:
    pattern = re.compile(rf"^\d{{2}}_(\d{{6}})\.{filetype}$")
    max_counter = -1

    for filename in os.listdir(folder_path):
        match = pattern.match(filename)
        if match:
            print('match')
            counter = int(match.group(1))
            max_counter = max(max_counter, counter)
    return max_counter

def make_output_file(folder_path: str) -> None:
    os.makedirs(os.path.dirname(folder_path), exist_ok=True)