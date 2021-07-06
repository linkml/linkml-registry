import click
import logging
from linkml_registry.registry import SchemaMetadata, SchemaRegistry
from linkml_registry.evaluate import evaluate
from linkml_registry.markdown_dumper import MarkdownTableDumper, MarkdownPageDumper
from linkml_runtime.dumpers import json_dumper, yaml_dumper
from linkml_runtime.loaders import yaml_loader


# Click input options common across commands
input_option = click.option('-i', '--input', required=True, type=click.Path(),
                            help='Input file, e.g. a SSSOM tsv file.')
output_directory_option = click.option('-d', '--output-directory', type=click.Path(), help='Output directory path.')
output_option = click.option('-o', '--output', help='Output file, e.g. a YAML file.')

@click.group()
@click.option('-v', '--verbose', count=True)
@click.option('-q', '--quiet')
def main(verbose: int, quiet: bool):
    """Main

    Args:

        verbose (int): Verbose.
        quiet (bool): Quiet.

    Returns:

        None.

    """
    if verbose >= 2:
        logging.basicConfig(level=logging.DEBUG)
    elif verbose == 1:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)
    if quiet:
        logging.basicConfig(level=logging.ERROR)


@main.command()
@input_option
@output_option
@click.option('--use-github-api/--no-use-github-api', default=False, help='Use the github API to enhance results')
@click.option('-m', '--markdown-output',
              default=None,
              help='path to markdown output')
@click.option('-w', '--workdir',
              default='tmp',
              help='working dir for checked out repos')
def eval(input: str, output: str, markdown_output: str = None, workdir: str = 'tmp', use_github_api: bool = False):
    """Evaluate

    Example:
        TODO

    Args:

        input (str): The path to the input models yaml file
        output (str): The path to the output file.

    Returns:

        None.

    """
    registry = yaml_loader.load(input, SchemaRegistry)
    evaluate(registry, use_github_api=use_github_api, workdir=workdir)
    if markdown_output:
        d = MarkdownPageDumper()
        d.dump(registry, to_file=markdown_output)
    if output:
        with open(output, "w") as stream:
            stream.write(yaml_dumper.dumps(registry))


if __name__ == "__main__":
    main()