from pathlib import Path


class WrongFileExtension(Exception):
    """"Custom exception"""

def open_txt_file(path):
    file = Path(path)
    filpath = str(file.absolute()).replace("\\","/")

    msg = (f"File was not found:\n{filpath}")
    if not file.is_file():
        raise FileNotFoundError(msg)

    if file.suffix == "txt":
        msg = (f"File extenstion is not txt:\n{filpath}")
        raise WrongFileExtension(msg)

    return file