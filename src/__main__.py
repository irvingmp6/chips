import argparse
import textwrap

from _version import __version__

from src.interface.interface_text import get_help_menu
from src.scraper.controller import Controller

def get_args():
    help_menu = get_help_menu()
    cli = argparse.ArgumentParser(
        prog='chips',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(help_menu['desc'])
    )
    cli.add_argument(
        'search_phrases',
        metavar='<SEARCH PHRASE(S)>',
        nargs='+',
        help=textwrap.dedent(help_menu['search_phrase'])
    )
    mutually_exclusive_group = cli.add_mutually_exclusive_group()
    mutually_exclusive_group.add_argument(
        '--exclude-domains',
        nargs='+',
        default=[],
        help=textwrap.dedent(help_menu['exclude-domains'])
    )
    mutually_exclusive_group.add_argument(
        '--only-domains',
        nargs='+',
        default=[],
        help=textwrap.dedent(help_menu['only-domains'])
    )
    cli.add_argument(
        '--debug', 
        action='store_true',
        help=textwrap.dedent(help_menu['debug'])
        )
    cli.add_argument(
        '--save-results', 
        action='store_true',
        help=textwrap.dedent(help_menu['save-results'])
        )
    cli.add_argument(
        '--save-urls', 
        action='store_true',
        help=textwrap.dedent(help_menu['save-urls'])
        )
    cli.add_argument(
        '--search-engines',
        nargs='+',
        choices=["ask", "bing", "google"],
        default=[],
        help=textwrap.dedent(help_menu['search-engines'])
    )
    cli.add_argument(
        '--timeout', '-t',
        type=int,
        default=5,
        help=textwrap.dedent(help_menu['timeout'])
    )
    cli.add_argument(
        '--verbose', '-v', 
        action='store_true',
        )
    cli.add_argument(
        '--version', '-V', action='version',
        version='%(prog)s {version}'.format(version=__version__)
    )
    return cli.parse_args()

def main():
    args = get_args()
    controller = Controller(args)
    controller.start_process()

if __name__ == "__main__":
    main()