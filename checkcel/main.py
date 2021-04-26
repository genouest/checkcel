from Checkcel import Checkcel
from Checkcel import Checkxtractor
from Checkcel import Checknerator
from Checkcel import Checkplate
from Checkcel import logs
from Checkcel import exits

import os
import tempfile
import shutil
import sys
import inspect
from argparse import ArgumentParser


def parse_args():
    """
    Handle command-line arguments with argparse.ArgumentParser
    Return list of arguments, largely for use in `parse_arguments`.
    """

    # Initialize
    parser = ArgumentParser(description="Test description")
    # Specify the vladfile to be something other than vladfile.py

    subparsers = parser.add_subparsers(help='sub-command help', dest="subcommand")

    parser_validate = subparsers.add_parser('validate', help='Validate a file')

    parser_validate.add_argument(
        dest="template",
        help="Python template to use for validation",
    )

    parser_validate.add_argument(
        dest="source",
        help="File to validate",
    )

    parser_validate.add_argument(
        "-t",
        "--type",
        dest="type",
        choices=['spreadsheet', 'tabular'],
        help="Type of file to validate : spreadsheet of tabular",
        default="spreadsheet"
    )

    parser_validate.add_argument(
        "-s",
        "--sheet",
        dest="sheet",
        default=0,
        help="Sheet to validate",
    )

    parser_validate.add_argument(
        "-d",
        "--delimiter",
        dest="delimiter",
        help="Delimiter for tabular files : Default to ','",
        default=","
    )

    parser_generate = subparsers.add_parser('generate', help='Generate an xlsx file')

    parser_generate.add_argument(
        dest="template",
        help="Python template to use for validation",
    )

    parser_generate.add_argument(
        dest="output",
        help="Output file name",
    )

    parser_extract = subparsers.add_parser('extract', help='Extract a template file')

    parser_extract.add_argument(
        dest="source",
        help="File to validate",
    )

    parser_extract.add_argument(
        dest="output",
        help="Output file name",
    )

    parser_extract.add_argument(
        "-s",
        "--sheet",
        dest="sheet",
        default=0,
        help="Sheet to extract",
    )

    return parser.parse_args()


def is_valid_template(tup):
    """
    Takes (name, object) tuple, returns True if it's a public Checkplate subclass.
    """
    name, item = tup
    return bool(
        inspect.isclass(item) and issubclass(item, Checkplate) and hasattr(item, "validators") and not name.startswith("_")
    )


def load_template_file(path):
    """
    Load template file and get the custom class (subclass of Checkplate)
    """
    # Limit conflicts in file name
    with tempfile.TemporaryDirectory() as dirpath:
        shutil.copy2(path, dirpath)
        directory, template = os.path.split(path)
        sys.path.append(dirpath)

        file = template.split(".")[0]
        mod = __import__(file)
        custom_class = None

        filtered_classes = dict(filter(is_valid_template, vars(mod).items()))
        # Get the first one
        if filtered_classes:
            custom_class = list(filtered_classes.values())[0]

    return custom_class


def main():
    arguments = parse_args()
    logger = logs.logger
    if arguments.subcommand not in ["validate", "generate", "extract"]:
        logger.error(
            "Unknown command"
        )
        return exits.NOINPUT

    if arguments.subcommand == "extract":
        Checkxtractor(source=arguments.source, output=arguments.output, sheet=arguments.sheet).extract()
        return exits.OK

    custom_template_class = load_template_file(arguments.template)
    if not custom_template_class:
        logger.error(
            "Could not find a subclass of Checkplate in the provided file."
        )
        return exits.UNAVAILABLE

    if arguments.subcommand == "validate":
        all_passed = True

        passed = Checkcel(
            validators=custom_template_class.validators,
            source=arguments.source,
            type=arguments.type,
            delimiter=arguments.delimiter,
            sheet=arguments.sheet
        ).validate()
        all_passed = all_passed and passed
        return exits.OK if all_passed else exits.DATAERR

    else:
        Checknerator(
            validators=custom_template_class.validators,
            output=arguments.output,
        ).generate()
        return exits.OK


def run(name):
    if name == "__main__":
        exit(main())


run(__name__)
