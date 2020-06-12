# -*- coding: utf-8 -*-

# This program is designed to create XML sidecar files for harvesting metadata into Mediaflux.
#
# Author: Jay van Schyndel
# Date: 02 May 2017.
#
# Significant modifications done by: Daniel Baird
# Date: 2018 and early 2019
#

#  Scenario. Metadata is stored in an MS Excel file in various columns.
#  Excel has been used to create a new column representing the metadata in the required XML format.
#  The file is then saved as a CSV.

# This program will open the CSV file, read the appropriate column and save the XML into a sidecar file based on the name of the data file.

# Note the program assumes there is a header row in the CSV file. It skips processesing the first row.

#
# new example: python ./scripts/csvColumnToXMLFile.py "./rawdata/excel/PacELF Phases 1_2_3 13Dec2018.csv" "/Users/pvrdwb/projects/PacELFDocs/PacELFphase3/" ./docs --location="HardcopyLocation2018"
#
# old example: python csvColumnToXMLFile.py  rawSpreadsheet/PacELF_Phase_1_AND_2.csv  ~/projects/PacELFDocs/PacELF\ PDFs  ./docs
#

import os
import re
import sys
import csv
import shutil
import argparse

parser = argparse.ArgumentParser(description="Create XML sidecar files from a CSV file")

parser.add_argument(
    "metadata_csv", metavar="metadataCSV", help="CSV file containing the XML"
)
parser.add_argument(
    "src_folder", metavar="sourceFolder", help="directory containing the source files"
)
parser.add_argument(
    "dest_folder", metavar="destinationFolder", help="Path of the destination folder"
)

parser.add_argument(
    "--title",
    metavar="titleColumn",
    help="Column containing the title",
    default="Title",
)
parser.add_argument(
    "--xml", metavar="xmlColumn", help="Column containing the XML", default="XML"
)
parser.add_argument(
    "--access",
    metavar="accessColumn",
    help="Column containing the Access Rights",
    default="Access Rights",
)
parser.add_argument(
    "--type", metavar="accessColumn", help="Column containing the Type", default="Type"
)
parser.add_argument(
    "--file",
    metavar="fileColumn",
    help="Column containing the data file name",
    default="PDF",
)
parser.add_argument(
    "--location",
    metavar="primaryLocationColumn",
    help="Column containing the primary hardcopy location",
    default="Hardcopy Locations",
)

try:
    args = parser.parse_args()
except:
    sys.exit(0)

print("Processing CSV file: ", args.metadata_csv)

# this is all the location typos we've found
loc_replacements = {}
loc_replacements[r"JCU WHOCC Ichimori collectoin"] = r"JCU WHOCC Ichimori collection"
loc_replacements[r"JCU WHOCC Ichimori Collection"] = r"JCU WHOCC Ichimori collection"
loc_replacements[r"JCU WHOCC ICHIMORI Collection"] = r"JCU WHOCC Ichimori collection"
loc_replacements[r"JCU WHO Ichimori Collection"] = r"JCU WHOCC Ichimori collection"
loc_replacements[r"JCU WHO Ichimori collection"] = r"JCU WHOCC Ichimori collection"
loc_replacements[r"JCU WHO CC Ichimori Collection"] = r"JCU WHOCC Ichimori collection"
loc_replacements[r"JCUWHOCC Ichimori collection"] = r"JCU WHOCC Ichimori collection"
loc_replacements[r"JCUWHOCC Ichimori Collection"] = r"JCU WHOCC Ichimori collection"
loc_replacements[r"Ichimori Collection"] = r"JCU WHOCC Ichimori collection"
loc_replacements[r"JCU WHOCC Nagasaki Collection"] = r"JCU WHOCC Ichimori collection"
loc_replacements[r"JCU WHOCC Nagasaki collection"] = r"JCU WHOCC Ichimori collection"
loc_replacements[r"WHO DPS Suva"] = r"WHO DPS Fiji"
loc_replacements[r"WHO HQ Geneva"] = r"WHO Geneva"

# -----------------------------------------------------------------------------
def clean_hc_location(loc):
    if loc in loc_replacements:
        return loc_replacements[loc]
    else:
        return loc


# -----------------------------------------------------------------------------
def clean_xml_content(xml_string):
    """
        Given some xml in string form that we got right from the spreadsheet,
        clean it up
    """
    for old_loc in loc_replacements:
        old = r"<hardcopy_location>([^<]*)" + old_loc + r"([^<]*)</hardcopy_location>"
        new = (
            r"<hardcopy_location>\1"
            + loc_replacements[old_loc]
            + r"\2</hardcopy_location>"
        )
        xml_string = re.sub(old, new, xml_string)

    return xml_string


# -----------------------------------------------------------------------------
def get_location_info(location):
    locations = {}
    locations[
        "JCU WHOCC Ichimori collection"
    ] = "James Cook University, Bldg 41 Rm 207, Townsville, Queensland 4811, Australia"
    locations[
        "JCU WHOCC"
    ] = "James Cook University, Bldg 41 Rm 207, Townsville, Queensland 4811, Australia"
    locations[
        "JCU Cairns (PMG)"
    ] = "James Cook University, Bldg E1 Rm 003C, Cairns, Queensland 4870, Australia"
    locations[
        "WHO DPS Fiji"
    ] = "World Health Organization, Level 4, Provident Plaza One, Downtown Boulevard, 33 Ellery Street, Suva, Fiji"
    locations[
        "WHO WPRO Manila"
    ] = "P.O. Box 2932, United Nations Ave. cor. Taft Ave, 1000 Manila, Philippines"
    locations["WHO Geneva"] = "Avenue Appia 20, 1202 Geneva, Switzerland"
    locations[
        "JCU library"
    ] = "James Cook University, Eddie Koiko Mabo library, Bldg 18, Townsville, Queensland 4811, Australia"
    return locations[location]


# -----------------------------------------------------------------------------

with open(args.metadata_csv, "rb") as csvfile:
    metadataReader = csv.DictReader(csvfile, delimiter=",")

    counts = {
        "rows": 0,
        "docs": 0,
        "restrict": 0,
        "hc": 0,
        "restrict_hc": 0,
        "write_err": 0,
        "copy_err": 0,
        "sidecar_err": 0,
        "no_doc": 0,
        "doc_missing": 0,
        "sidecars": 0,
    }

    for row in metadataReader:

        counts["rows"] += 1

        # Skipping first row as it contains the header row.
        if counts["rows"] > 1:

            real_file = row[args.file]
            xml_content = row[args.xml]

            # clean the XML (this part is special to the specific data we're getting)
            xml_content = clean_xml_content(xml_content)

            doc_access = row[args.access]
            doc_type = row[args.type]
            hc_location = (
                row[args.location].split(";")[0].strip()
            )  # semicolon separated list -- get the first one
            hc_location = clean_hc_location(hc_location)
            doc_title = row[args.title]

            # bail if there's no title
            if doc_title == "":
                continue
            else:
                # print("LOOKING: " + doc_title)
                counts["docs"] += 1
                pass

            # destination for the xml file
            flat_file_name, file_ext = os.path.splitext(real_file)

            # maybe there are subdirs in the file name, we'll flatten those out
            flat_file_name = flat_file_name.replace("/", "#")

            # copy the file there
            # maybe we have to fake up the content coz it's restricted or something
            fake_content = False

            if doc_access == "Restricted" and doc_type == "Hardcopy" and hc_location:
                # it's a restricted hardcopy with a location
                counts["restrict_hc"] += 1
                fake_content = "".join(
                    [
                        'The document "',
                        doc_title,
                        '" is restricted due to data sensitivity. ',
                        "Please e-mail pacelf@jcu.edu.au or write to:\n\n    ",
                        get_location_info(hc_location),
                        "\n\nto negotiate gaining access to this item.",
                    ]
                )

            elif (
                doc_access == "Restricted"
                and doc_type == "Hardcopy"
                and not hc_location
            ):
                # it's a restricted hardcopy with no location
                counts["restrict_hc"] += 1
                fake_content = "".join(
                    [
                        'The document "',
                        doc_title,
                        '" is restricted due to data sensitivity. ',
                        "Please e-mail pacelf@jcu.edu.au to negotiate gaining access to this item.",
                    ]
                )

            elif doc_access != "Restricted" and doc_type == "Hardcopy" and hc_location:
                # it's an unrestricted hardcopy with a location
                counts["hc"] += 1
                fake_content = "".join(
                    [
                        'The document "',
                        doc_title,
                        '" is not available in digital format. ',
                        "A copy is held at:\n\n    ",
                        get_location_info(hc_location),
                        "\n\nplease write or email pacelf@jcu.edu.au to request a copy.",
                    ]
                )

            elif (
                doc_access != "Restricted"
                and doc_type == "Hardcopy"
                and not hc_location
            ):
                # it's an unrestricted hardcopy with no location
                counts["hc"] += 1
                fake_content = "".join(
                    [
                        'The document "',
                        doc_title,
                        '" is not available in digital format. ',
                        "Please e-mail pacelf@jcu.edu.au to request a copy.",
                    ]
                )

            elif doc_access == "Restricted" and doc_type != "Hardcopy":
                # it's a restricted PDF
                counts["restrict"] += 1
                fake_content = "".join(
                    [
                        'The document "',
                        doc_title,
                        '" is restricted due to data sensitivity. ',
                        "Please e-mail pacelf@jcu.edu.au to negotiate gaining access to this item.",
                    ]
                )

            elif flat_file_name == "":
                # any other situation where there's no doc
                counts["no_doc"] += 1
                fake_content = "".join(
                    [
                        'The document "',
                        doc_title,
                        '" is not available in digital format. ',
                        "Please e-mail pacelf@jcu.edu.au to discuss access.",
                    ]
                )

            if flat_file_name == "":
                flat_file_name = "PacELF_Phase2_" + str(counts["rows"])

            #
            # by now have fake content to use, or we expect the doc to be available.
            #

            # destination for the real file
            real_dest_file = os.path.join(args.dest_folder, flat_file_name + file_ext)
            # destination for the proxy document (.txt extension)
            fake_dest_path = os.path.join(args.dest_folder, flat_file_name + ".txt")

            if fake_content:
                # write the fake content, if we have it
                try:
                    file = open(fake_dest_path, "w")
                    file.write(fake_content)
                    file.close()
                    # print(unicode('PROXIED: ') + unicode(doc_title))
                except ValueError as e:
                    counts["write_err"] += 1
                    print("Couldn't write content to: " + real_dest_file)
                    print(e)
            else:
                # we didn't have fake content, so use the real doc/pdf
                real_file_path = os.path.join(args.src_folder, real_file)

                if real_file == "":
                    print('No doc file specified for "' + doc_title + '"')
                    counts["no_doc"] += 1
                    continue

                # try to copy the file --------

                # first let's get some common error versions of the filename
                fn_to_try = [real_file_path]
                fn_to_try.append(
                    re.sub(r"\.pdf$", r" .pdf", real_file_path)
                )  # space before the pdf
                fn_to_try.append(re.sub(r"\\", r"/", real_file_path))  # other slashes
                fn_to_try.append(re.sub(r"$", r".pdf", real_file_path))  # add .pdf
                fn_to_try.append(
                    re.sub(
                        r"Multicountry Pacific", r"multicountry pacific", real_file_path
                    )
                )  # upper case
                fn_to_try.append(
                    re.sub(
                        r"Mulitcountry Pacific", r"multicountry pacific", real_file_path
                    )
                )  # typo & upper case

                # some straight fixes
                fn_to_try.append(
                    re.sub(
                        r"\\\.pdf$",
                        r"PDF version\.pdf",
                        re.sub(
                            r"Mulitcountry Pacific",
                            r"multicountry pacific",
                            real_file_path,
                        ),
                    )
                )  # two fixes
                fn_to_try.append(
                    re.sub(
                        r"PacELF_102", r"PacELF_102 Jarno et al 2006", real_file_path
                    )
                )  # add author
                fn_to_try.append(
                    re.sub(
                        r"PacELF_448",
                        r"PacELF_448 Andrews et al 2012 PLOS PATHOGENS ",
                        real_file_path,
                    )
                )
                fn_to_try.append(
                    re.sub(
                        r"PacELF_493",
                        r"PacELF_493 Brelsfoard et al 2008 PLOS NTDs Interspecific hybridization South Pacific filariasis vectors",
                        real_file_path,
                    )
                )
                fn_to_try.append(
                    re.sub(
                        r"PacELF_508",
                        r"PacELF_508 Burkot et al 2013 MAL J Barrier screens",
                        real_file_path,
                    )
                )
                fn_to_try.append(
                    re.sub(
                        r"PacELF_314",
                        r"PacELF_314 Stolk et al 2013 PLOS NTDs",
                        real_file_path,
                    )
                )
                fn_to_try.append(
                    re.sub(
                        r"PacELF_317",
                        r"PacELF_317 Debrah et al 2006 PLOS PATHOGENS Doxycycline reduces VGF and improves pathology LF",
                        real_file_path,
                    )
                )
                fn_to_try.append(
                    re.sub(
                        r"PacELF_319",
                        r"PacELF_319 Hooper et al 2014 PLOS NTDs Asseesing progress in reducing at risk population after 13 years",
                        real_file_path,
                    )
                )
                fn_to_try.append(
                    re.sub(
                        r"\\2001-05 PRG Fiji May-Jun 2011\\",
                        r"/2011-05 PRG Fiji May-Jun 2011/",
                        real_file_path,
                    )
                )
                fn_to_try.append(
                    re.sub(
                        r"PacELF_414 WPRO PMM 2011 report_2011 Oct 31\.pdf",
                        r"PacELF_414 WPRO PMM 2011 report_2011 Oct 31 PDF version.pdf",
                        real_file_path,
                    )
                )
                fn_to_try.append(
                    re.sub(
                        r"Multicountry Pacific/PacELF_585",
                        r"French Polynesia/PacELF_585",
                        real_file_path,
                    )
                )
                fn_to_try.append(
                    re.sub(
                        r"Manson-Bahr 1912 FIlariasis and elephantiasis in Fiji LSHTM b21356658",
                        r"Manson-Bahr 1912  FIlariasis and elephantiasis in Fiji  LSHTM b21356658",
                        real_file_path,
                    )
                )

                # find the first that is a file
                for pth in fn_to_try:
                    if os.path.isfile(pth):
                        break

                # try copying that
                if os.path.isfile(pth):
                    try:
                        shutil.copyfile(pth, real_dest_file)
                        # print(' COPIED: ' + doc_title)
                    except shutil.Error as e:
                        counts["copy_err"] += 1
                        print("Could not copy doc: " + pth)
                        print(e)
                else:
                    print(
                        "Could not find doc file for title: '"
                        + doc_title
                        + "', file: "
                        + pth
                    )
                    counts["doc_missing"] += 1

            #
            # Now we've got content there, make the xml sidecar file
            #

            xml_dest_file = flat_file_name + ".xml"
            xml_dest_path = args.dest_folder + "/" + xml_dest_file

            try:
                file = open(xml_dest_path, "w")
                file.write(xml_content)
                file.close()
                counts["sidecars"] += 1
            except ValueError as e:
                counts["sidecar_err"] += 1
                print("Oops, this one is dodgy: " + xml_dest_path)
                print("ValueError: ", e)


print("\nSummary:")
print(
    "".join(
        [
            "    ",
            str(counts["rows"]),
            " rows read: ",
            str(counts["docs"]),
            " documents processed, ",
            str(counts["sidecars"]),
            " metadata sidecars produced;",
            "\n    ",
            str(counts["hc"]),
            " hard copies, ",
            str(counts["restrict"]),
            " restricted docs, ",
            str(counts["restrict_hc"]),
            " restricted hard copies;",
            "\n    ",
            str(counts["copy_err"]),
            " copy errors, ",
            str(counts["write_err"]),
            " write errors, ",
            str(counts["sidecar_err"]),
            " sidecar errors, ",
            str(counts["doc_missing"]),
            " docs not locatable, ",
            str(counts["no_doc"]),
            " docs not listed.",
            "\n",
        ]
    )
)

