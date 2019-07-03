import unicodedata
import string
from loguru import logger
import os
from pathlib import Path


valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 255


def clean_filename(filename, whitelist=valid_filename_chars, replace=" "):
    # replace spaces
    for r in replace:
        filename = filename.replace(r, "_")

    # keep only valid ascii chars
    cleaned_filename = (
        unicodedata.normalize("NFKD", filename).encode("ASCII", "ignore").decode()
    )

    # keep only whitelisted chars
    cleaned_filename = "".join(c for c in cleaned_filename if c in whitelist)
    if len(cleaned_filename) > char_limit:
        print(
            "Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(
                char_limit
            )
        )
    return cleaned_filename[:char_limit]


def clean_filenames_of_data_folder():

    data_path = Path.cwd()

    try:
        for filename in os.listdir(data_path):

            cleaned_filename = clean_filename(filename)
            print("The old filename :")
            print(filename)
            print("-------------------------")
            print("The cleaned filename :")
            print(cleaned_filename)
            os.rename(filename, cleaned_filename)

    except Exception as e:
        print(e)
        logger.error(e)


if __name__ == "__main__":
    clean_filenames_of_data_folder()
