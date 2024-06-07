# Create ArgumentParser object
import argparse
import glob
import logging
import os
import sys

from nicebook.configs import Configs
from nicebook.generator import Generator


def main():

    parser = argparse.ArgumentParser(description="Generate customizable PDF's from markdown files")

    # Add arguments
    parser.add_argument("-i","--input", help="Can be folders or markdown files, multiple allowed", nargs="+")
    parser.add_argument("-o","--output", help="Path to output file", default="output.pdf")
    parser.add_argument("-c","--config", help="Config file. Will search for nicebook.yml in current folder if non is specified.", default=Configs.DEFAULT_FILE_NAME)
    parser.add_argument("-v","--verbose", help="Verbose mode",  action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("-g","--generate-config", help=f"Generate a {Configs.DEFAULT_FILE_NAME} with the default configs so can be easily overriden",action=argparse.BooleanOptionalAction, default=False)
    args = parser.parse_args()


    if args.generate_config:
        # if os.path.exists(Configs.DEFAULT_FILE_NAME):
        #     print(f"{Configs.DEFAULT_FILE_NAME} already exists")
        #     sys.exit(1)

        current_file = os.path.dirname(os.path.abspath(__file__))

        Configs.generate_default_config_file(Configs.DEFAULT_FILE_NAME)

        sys.exit(0)


    input = args.input
    if not input:
        parser.print_help()
        sys.exit(1)

    # fix for when receiving a multi line string from piped input


    files = []

    for item in input:
        for i in item.split("\n"):
            if os.path.isdir(i):
                files.extend(glob.glob(i + '/**/*.md', recursive=True))
            else:
                files.append(i)


    output_file = args.output
    verbose = args.verbose
    config = args.config

    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    g = Generator(config)
    g.generate(files, output_file)

if __name__ == "__main__":
    main()
