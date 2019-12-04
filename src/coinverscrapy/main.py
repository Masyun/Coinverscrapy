import argparse
import sys
import logging
import os
import camelot
import json

from src.coinverscrapy import __version__
from src.coinverscrapy.scraper.Scraper import Scraper
from src.coinverscrapy.scraper.ScraperProxy import ScraperProxy
from src.coinverscrapy.parser.Parser import Parser
from src.coinverscrapy.parser.ParserProxy import ParserProxy

__author__ = "MasYun"
__copyright__ = "MasYun"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


def scrape_website(url, local_output):
    """Main scrape function

    Args:
      URL : string

    Returns:
      int: 0
      :param local_output:
      :param url:
    """
    ScraperProxy(Scraper(url), local_output).start()


def parse_tojson(input_location, output_location):
    """Main parse function

    Args:
      URL : string

    Returns:
      int: 0
      :param output_location:
      :param input_location:
    """
    ParserProxy(Parser(input_location), output_location).start()


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Coinversable website scraper/PDF parser tool")
    parser.add_argument(
        "--version",
        action="version",
        version="coinverscrapy {ver}".format(ver=__version__))
    parser.add_argument(
        dest="url",
        help="url of the webpage to be scraped",
        type=str,
        metavar="INT")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO)
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG)
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        help="specify the output directory",
        type=str)
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)

    # scrape_website(args.url, "pdfs")
    if args.output:
        parse_tojson("pdfs", args.output)
    else:
        parse_tojson("pdfs", 'C:\\Json_vakken')  # C:\Users\yunus\Desktop

def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
