from pathlib import Path


class WrongFileExtension(Exception):
    """"Custom exception"""

def open_txt_file(path):
    file = Path(path)

    msg = (f"File was not found:\n{file.absolute()}")
    if not file.is_file():
        raise FileNotFoundError(msg)

    if file.suffix == "txt":
        msg = (f"File extenstion is not txt:\n{file.absolute()}")
        raise WrongFileExtension(msg)

    return file