import argparse
import os
import utils

default_input_dir = "../data"

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default=None, type=bool, required=True, help="create csv files from articles")
    parser.add_argument("--all", default=None, type=bool, required=True, help="convert all files")
    parser.add_argument("--infile", default=default_input_dir, type=str, required=True,
                        help="Directory for xml input files")
    parser.add_argument("--out", type=str, required=True, help="Output (csv) file")
    args = parser.parse_args()

    source_files = []
    truth_files = []

    for root, dirs, files in os.walk(args.infile):
        for file in files:
            if file.endswith('xml') and 'validation' not in file:
                truth_files.append(str(os.path.join(root, file))) if 'ground-truth' in file else source_files.append(
                    str(os.path.join(root, file)))
    utils.parse_xml_files(source_files, truth_files, args.csv, args.out + "\\processed.csv")
