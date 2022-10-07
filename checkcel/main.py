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

    subparsers = parser.add_subparsers(help='sub-command help', dest="subcommand")

    parser_validate = subparsers.add_parser('validate', help='Validate a file')

    parser_validate.add_argument(
        dest="template",
        help="Template to use for validation",
    )

    parser_validate.add_argument(
        dest="source",
        help="File to validate",
    )

    parser_validate.add_argument(
        "-f",
        "--format",
        dest="format",
        choices=['spreadsheet', 'tabular'],
        help="Type of file to validate : spreadsheet of tabular",
        default="spreadsheet"
    )

    parser_validate.add_argument(
        "-s",
        "--sheet",
        dest="sheet",
        default=0,
        help="Sheet to validate. Default to 0 for first sheet",
    )

    parser_validate.add_argument(
        "-d",
        "--delimiter",
        dest="delimiter",
        help="Delimiter for tabular files : Default to ','",
        default=","
    )

    parser_validate.add_argument(
        "-r",
        "--row",
        dest="row",
        default=0,
        help="Ignore the first n rows (default 0)",
    )

    parser_validate.add_argument(
        "-t",
        "--template",
        dest="template_type",
        choices=['python', 'json', 'yml', 'yaml'],
        help="Template type (python, json, or yml)",
        default="python"
    )

    parser_generate = subparsers.add_parser('generate', help='Generate an xlsx file')

    parser_generate.add_argument(
        dest="template",
        help="Template to use for validation",
    )

    parser_generate.add_argument(
        dest="output",
        help="Output file name",
    )

    parser_generate.add_argument(
        "-t",
        "--template",
        dest="template_type",
        choices=['python', 'json', 'yml', 'yaml'],
        help="Template type (python, json, or yml)",
        default="python"
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
        help="Sheet to extract. Default to 0 for first sheet",
    )

    parser_extract.add_argument(
        "-r",
        "--row",
        dest="row",
        default=0,
        help="Ignore the first n rows (default 0)",
    )

    parser_extract.add_argument(
        "-t",
        "--template",
        dest="template_type",
        choices=['python', 'json', 'yml', 'yaml'],
        help="Template type (python, json, or yml)",
        default="python"
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
        Checkxtractor(source=arguments.source, output=arguments.output, sheet=arguments.sheet, row=arguments.row, template_type=arguments.template_type).extract()
        return exits.OK

    if arguments.subcommand == "validate":
        all_passed = True

        passed = Checkcel(
            source=arguments.source,
            format=arguments.format,
            delimiter=arguments.delimiter,
            sheet=arguments.sheet,
            row=arguments.row
        )

        if arguments.template_type == "python":
            passed.load_from_python_file(arguments.template)
        elif arguments.template_type == "json":
            passed.load_from_json_file(arguments.template)
        elif arguments.template_type in ["yml", "yaml"]:
            passed.load_from_yaml_file(arguments.template)

        if not isinstance(passed, Checkplate):
            return passed
        passed.validate()
        all_passed = all_passed and passed
        return exits.OK if all_passed else exits.DATAERR

    else:
        passed = Checkerator(output=arguments.output)
        if arguments.template_type == "python":
            passed.load_from_python_file(arguments.template)
        elif arguments.template_type == "json":
            passed.load_from_json_file(arguments.template)
        elif arguments.template_type in ["yml", "yaml"]:
            passed.load_from_yaml_file(arguments.template)

        if not isinstance(passed, Checkplate):
            return passed
        passed.generate()
        return exits.OK


def run(name):
    if name == "__main__":
        exit(main())


run(__name__)
