import os
import pathlib
import click
import datetime
import logging

import requests
import pandas as pd
from tqdm import tqdm


# datetime formats reverse engineered from the Radio 24 website
date_format = "%y%m%d"
year_format = "%Y"

try:
    # find the latest existing file
    latest_file = sorted(list(pathlib.Path(".").glob("*-lazanzara.mp3")))[-1]
    # add one day to the latest existing file
    default_start_date = (
        datetime.datetime.strptime(str(latest_file).split("-")[0], date_format)
        + datetime.timedelta(days=1)
    ).strftime(date_format)
    print(default_start_date)
except IndexError:
    # if no files match, start from today
    default_start_date = datetime.datetime.today().strftime(date_format)


@click.command()
@click.option("--start_date", default=default_start_date, help="start date (yymmdd)")
@click.option(
    "--end_date",
    default=datetime.datetime.today().strftime(date_format),
    help="end date (yymmdd)",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
)
def main(start_date, end_date, verbose):
    """
    Download audio files of 'La Zanzara' radio program.

    This script downloads audio files of the 'La Zanzara' radio program from Radio24's
    website. You can specify a date range to download the audio files between the
    'start_date' and 'end_date'. The files are saved as MP3 files.

    Args:
        start_date (str): The start date in the format 'yymmdd'.
        end_date (str): The end date in the format 'yymmdd'.
        verbose (int): Verbosity level (0 for warnings, 1 for debug messages).

    Returns:
        None: Downloads and saves MP3 files.

    Example:
        To download audio files from January 1, 2022, to January 5, 2022, you can
        run the following command:

        $ python download_zanzara.py --start_date 220101 --end_date 220105

    """
    # set up logging
    levels = [
        logging.WARNING,
        logging.DEBUG,
    ]
    log_format = "%(asctime)s - %(name)s: %(message)s"
    logger = logging.getLogger(__name__)
    verbose = min(len(levels) - 1, verbose)
    logging.basicConfig(level=levels[verbose], format=log_format)

    # Parse the start_date and end_date as datetime objects
    start_date = datetime.datetime.strptime(start_date, date_format)
    end_date = datetime.datetime.strptime(end_date, date_format)
    daterange = pd.date_range(start_date, end_date)
    for day in tqdm(daterange):
        # Construct the URL for the audio file based on the date, by interpolating year and date
        url = "http://audio.radio24.ilsole24ore.com/radio24_audio/{}/{}-lazanzara.mp3".format(
            day.strftime(year_format), day.strftime(date_format)
        )
        response = requests.get(url, stream=True)
        logger.debug("requested url %s", url)
        logger.debug("got %s", response)
        if response.ok:
            # Extract the output filename from the URL and save the file
            output_path = os.path.basename(url)
            with open(os.path.basename(url), "wb") as output_file:
                for chunk in response.iter_content(4096):
                    output_file.write(chunk)
            logger.debug("written %s", output_path)


if __name__ == "__main__":
    main()
