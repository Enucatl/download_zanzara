import datetime
import os
import click
import requests
import pandas as pd
import logging
from tqdm import tqdm


@click.command()
@click.option(
    "--start_date",
    default="20160215",
    help="start date (yyyymmdd)")
@click.option(
    "--end_date",
    default=datetime.datetime.today().strftime("%Y%m%d"),
    help="end date (yyyymmdd)")
@click.option(
    "-v",
    "--verbose",
    count=True,
    )
def main(start_date, end_date, verbose):
    """download de la zanzara, date in formato yyyymmdd

    :start_date: string yyyymmdd
    :end_date: string yyyymmdd
    :returns: nothing, saves mp3 files

    """
    levels = [
        logging.WARNING,
        logging.DEBUG,
    ]
    log_format = '%(asctime)s - %(name)s: %(message)s'
    logger = logging.getLogger(__name__)
    verbose = min(len(levels) - 1, verbose)
    logging.basicConfig(level=levels[verbose], format=log_format)
    start_date = datetime.datetime.strptime(start_date, "%Y%m%d")
    end_date = datetime.datetime.strptime(end_date, "%Y%m%d")
    daterange = pd.date_range(start_date, end_date)
    n = len(daterange)
    for day in tqdm(daterange):
        url = "http://audio.radio24.ilsole24ore.com/radio24_audio/{}/{}-lazanzara.mp3".format(
            day.strftime("%Y"), day.strftime("%y%m%d"))
        response = requests.get(url, stream=True)
        logger.debug("requested url %s", url)
        logger.debug("got %s", response)
        if response.ok:
            output_path = os.path.basename(url)
            with open(os.path.basename(url), "wb") as output_file:
                for chunk in response.iter_content(1024):
                    output_file.write(chunk)
            logger.debug("written %s", output_path)


if __name__ == "__main__":
    main()
