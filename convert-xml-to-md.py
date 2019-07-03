import os
import shutil
import string
import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

from jinja2 import Template
from loguru import logger

logger.add(
    sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>"
)

# Remove the existing markdown files from the output directory and make a new empty folder
markdown_output_dir = "./_datasets/"
shutil.rmtree(markdown_output_dir)
os.makedirs(markdown_output_dir)


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


def make_markdown_from_xml():
    try:
        source_docs_path = "./docs/"
        for filename in os.listdir(source_docs_path):
            if filename.endswith(".xml"):

                dict = {}

                # Make an output filename to match the input
                filepath = os.path.join(source_docs_path, filename)
                # txt_file_path = filepath.replace(".xml", ".txt")
                markdown_filename = filepath.split("/")[2]
                markdown_filename = markdown_filename.split(".")[0]
                markdown_filename = markdown_filename + ".md"
                jekyll_dataset_dir = "./_datasets/"

                # load and parse the XML file for key and values
                xmlTree = ET.parse(filepath)

                for elem in xmlTree.iter():
                    if elem.text is not None:

                        key = elem.tag
                        value = elem.text.replace(
                            ":", " "
                        )  # removing colons from text areas since markdown
                        if ("pdf_file_name") in key:

                            # The actual document filenames have been already cleaned with this scrubbing function below
                            # So let's match up the metadata with the files
                            value = clean_filename(value)

                            jekyll_docs_dir = "/docs/"
                            docs_folder_path = "./docs/"

                            filepath = docs_folder_path + value
                            path_to_supposed_pdf = Path(filepath)

                            logger.info("Checking the file type at :")
                            logger.info(path_to_supposed_pdf)

                            if path_to_supposed_pdf.is_file():  # pdf file exists
                                logger.info("I did see a PDF, I did, I did.")
                                logger.info(value)
                                value = jekyll_docs_dir + value
                            else:
                                logger.info("PDF does NOT exist! At location :")
                                logger.info(value)
                                value = value.replace(".pdf", ".txt")
                                # make the URL value equal to the full filepath
                                value = jekyll_docs_dir + value
                                logger.info("New TXT File Path : " + value)

                                if not value.endswith((".pdf", ".txt")):
                                    value = "/docs/contact_for_access.txt"

                            logger.info("Corrected URL to PDF/TXT is :" + value)

                        if ("title") in key:
                            value = value.replace(
                                '"', ""
                            )  # Some have " in them, breaks YAML/MD

                        if ("title") in key:
                            value = value.replace("[", " ").replace(
                                "]", " "
                            )  # Some  have [ ] in them, breaks YAML/MD

                        if ("description") in key:
                            value = value.replace("[", " ").replace(
                                "]", " "
                            )  # Some  have [ ] in them, breaks YAML/MD

                        dict[key] = value

                # end of elemTree iteration

                # Populating variables for Jinja template to meet Markdown layout needed by Jekyll
                PacELF_ID = dict.get("PacELF_ID", "N/A")
                title = dict.get("title", "N/A")
                type = dict.get("type", "N/A")
                authors = dict.get("authors", "No authors available.")
                description = dict.get("description", "No abstract available.")
                category = dict.get("category", "No category available.")
                pdf_file_name = dict.get(
                    "pdf_file_name", "/docs/contact_for_access.txt"
                )
                access_rights = dict.get("access_rights", "No access rights available.")
                hardcopy_location = dict.get(
                    "hardcopy_location", "No hardcopy location available."
                )
                pages = dict.get("pages", "N/A")
                work_location = dict.get("work_location", "No work location available.")
                language = dict.get("language", "N/A")
                year = dict.get("year", "N/A")
                decade = dict.get("decade", "N/A")
                journal = dict.get("journal", "No journal available.")
                publisher = dict.get("publisher", "No publisher available. ")

                # Experimenting with markdown generation

                template = Template(
                    "---\n"
                    "schema: pacelf\n"
                    "title: {{ title }}\n"
                    "organization: {{ authors }}\n"
                    "notes: {{ description }}\n"
                    "access: {{ access_rights }}\n"
                    "\n"
                    "resources:\n"
                    "- name: {{ title }}\n"
                    "  url: '{{ pdf_file_name }}'\n"
                    "  format: {{ type }}\n"
                    "  access: {{ access_rights }}\n"
                    "  pages: {{ pages }}\n"
                    " \n"
                    "category: {{ category }}\n"
                    "access: {{ access_rights }}\n"
                    "journal: {{ journal }}\n"
                    "publisher: {{ publisher }}\n"
                    "language: {{ language }} \n"
                    "tags: {{ language }} \n"
                    "hardcopy_location: {{ hardcopy_location }}\n"
                    "work_location: {{ work_location }}\n"
                    "year: {{ year }}\n"
                    "decade: {{ decade }}\n"
                    "PacELF_ID: {{ PacELF_ID }}\n"
                    "---"
                )
                rendered_template = template.render(
                    title=title,
                    PacELF_ID=PacELF_ID,
                    type=type,
                    authors=authors,
                    description=description,
                    category=category,
                    pdf_file_name=pdf_file_name,
                    access_rights=access_rights,
                    hardcopy_location=hardcopy_location,
                    pages=pages,
                    work_location=work_location,
                    language=language,
                    year=year,
                    decade=decade,
                    journal=journal,
                    publisher=publisher,
                )

                # print(rendered_template)
                # logger.info(rendered_template)

                # attempts to clean up markdown in a code block
                # def markup(text, *args, **kwargs):
                #     return markdown(text, *args, **kwargs)
                #
                # marked_template = markup(rendered_template)
                # marked_template = marked_template.replace("<pre><code>", "")
                # marked_template = marked_template.replace("<pre><code>", "").replace(
                #     "</code></pre>", ""
                # )

                # with open(output_dir + markdown_filename, "w") as text_file:
                #     print(rendered_template, file=text_file)
                #     logger.info("Wrote " + markdown_filename + " to " + output_dir)

                with open(jekyll_dataset_dir + markdown_filename, "w") as text_file:
                    print(rendered_template, file=text_file)
                    logger.info(
                        "Wrote " + markdown_filename + " to " + jekyll_dataset_dir
                    )

        # can remove duplicates - convert to set and back to list
        # elemList = list(set(elemList))

    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    make_markdown_from_xml()
