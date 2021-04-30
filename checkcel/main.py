from checkcel import Checkplate
from checkcel import Checkcel
from checkcel import Checkxtractor
from checkcel import Checkerator
from checkcel import logs
from checkcel import exits

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

    parser_extract.add_argument(
        "-r",
        "--row",
        dest="row",
        default=0,
        help="Row to extract (default 0)",
    )

    return parser.parse_args()


def main():
    arguments = parse_args()
    logger = logs.logger
    if arguments.subcommand not in ["validate", "generate", "extract"]:
        logger.error(
            "Unknown command"
        )
        return exits.NOINPUT

    if arguments.subcommand == "extract":
        Checkxtractor(source=arguments.source, output=arguments.output, sheet=arguments.sheet, row=arguments.row).extract()
        return exits.OK

    if arguments.subcommand == "validate":
        all_passed = True

        passed = Checkcel(
            source=arguments.source,
            type=arguments.type,
            delimiter=arguments.delimiter,
            sheet=arguments.sheet
        ).load_from_file(arguments.template)
        if not isinstance(passed, Checkplate):
            return passed
        passed.validate()
        all_passed = all_passed and passed
        return exits.OK if all_passed else exits.DATAERR

    else:
        passed = Checkerator(
            output=arguments.output,
        ).load_from_file(arguments.template)
        if not isinstance(passed, Checkplate):
            return passed
        passed.generate()
        return exits.OK


def run(name):
    if name == "__main__":
        exit(main())


run(__name__)
