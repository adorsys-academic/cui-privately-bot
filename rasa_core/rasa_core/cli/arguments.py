import pkg_resources


def add_config_arg(parser, nargs="*", **kwargs):
    """Add an argument to the parser to request a policy configuration."""

    parser.add_argument(
        '-c', '--config',
        type=str,
        nargs=nargs,
        default=[pkg_resources.resource_filename(__name__,
                                                 "../default_config.yml")],
        help="Policy specification yaml file.",
        **kwargs)


def add_core_model_arg(parser, **kwargs):
    """Add an argument to the parser to request a policy configuration."""

    parser.add_argument(
        '--core',
        type=str,
        help="Path to a pre-trained core model directory",
        **kwargs)


def add_domain_arg(parser, required=True, **kwargs):
    """Add an argument to the parser to request a the domain file."""

    parser.add_argument(
        '-d', '--domain',
        type=str,
        required=required,
        help="Domain specification (yml file)",
        **kwargs)


def add_output_arg(parser,
                   help_text,
                   required=True,
                   **kwargs):
    parser.add_argument(
        '-o', '--out',
        type=str,
        required=required,
        help=help_text,
        **kwargs)


def add_model_and_story_group(parser, allow_pretrained_model=True):
    """Add an argument to the parser to request a story source."""

    # either the user can pass in a story file, or the data will get
    # downloaded from a url
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-s', '--stories',
        type=str,
        help="File or folder containing stories")
    group.add_argument(
        '--url',
        type=str,
        help="If supplied, downloads a story file from a URL and "
             "trains on it. Fetches the data by sending a GET request "
             "to the supplied URL.")

    if allow_pretrained_model:
        add_core_model_arg(group)
