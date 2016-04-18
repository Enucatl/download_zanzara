import datetime
import os
import click
import requests
import pandas as pd


@click.command()
@click.option(
    "--start_date",
    default="20160215",
    help="start date (yyyymmdd)")
@click.option(
    "--end_date",
    default="20160220",
    help="end date (yyyymmdd)")
def main(start_date, end_date):
    """download della zanzara da start date a end date
    (formato yyyymmdd)

    :start_date: string yyyymmdd
    :end_date: string yyyymmdd
    :returns:

    """
    start_date = datetime.datetime.strptime(start_date, "%Y%m%d")
    end_date = datetime.datetime.strptime(end_date, "%Y%m%d")
    daterange = pd.date_range(start_date, end_date)
    for day in daterange:
        url = "http://audio.radio24.ilsole24ore.com/radio24_audio/{}/{}-lazanzara.mp3".format(
            day.strftime("%Y"), day.strftime("%y%m%d"))
        response = requests.get(url, stream=True)
        print(url, response)
        if response.ok:
            with open(os.path.basename(url), "wb") as output_file:
                for chunk in response.iter_content(1024):
                    output_file.write(chunk)


if __name__ == "__main__":
    main()
import datetime
import os
import click
import requests
import pandas as pd


@click.command()
@click.option(
    "--start_date",
    default="20160215",
    help="start date (yyyymmdd)")
@click.option(
    "--end_date",
    default="20160220",
    help="end date (yyyymmdd)")
def main(start_date, end_date):
    """download della zanzara da start date a end date
    (formato yyyymmdd)

    :start_date: string yyyymmdd
    :end_date: string yyyymmdd
    :returns:

    """
    start_date = datetime.datetime.strptime(start_date, "%Y%m%d")
    end_date = datetime.datetime.strptime(end_date, "%Y%m%d")
    daterange = pd.date_range(start_date, end_date)
    for day in daterange:
        url = "http://audio.radio24.ilsole24ore.com/radio24_audio/{}/{}-lazanzara.mp3".format(
            day.strftime("%Y"), day.strftime("%y%m%d"))
        response = requests.get(url, stream=True)
        print(url, response)
        if response.ok:
            with open(os.path.basename(url), "wb") as output_file:
                for chunk in response.iter_content(1024):
                    output_file.write(chunk)


if __name__ == "__main__":
    main()