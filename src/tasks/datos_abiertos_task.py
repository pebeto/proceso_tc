import pandas as pd
from src.scrapers.teamcore_scraper import TeamcoreScraper


def run_web_scraping(url, download_output_directory, download_file_name):
    """
    Runs web scraping by defined logic in selected class
    """
    scraper = TeamcoreScraper(
        url,
        download_output_directory,
        download_file_name)
    scraper.scrap_data('dataset', 'economia y finanzas', 'csv', 'donaciones')


def create_region_data_by_initial_csv(path_to_file, region_output_directory):
    """
    Creates new .csv files for each region by an initial csv file. It accepts compressed files.
    """
    df = pd.read_csv(path_to_file, encoding='latin-1')
    regions = df['REGION'].unique()
    for region in regions:
        region_df = df[df['REGION'] == region]
        region_df.to_csv(
            f'{region_output_directory}/{region.lower()}.csv',
            index=False)
        print(
            f'A csv file for {region} was generated in {region_output_directory}...')


def run_datos_abiertos_task():
    url = 'https://www.datosabiertos.gob.pe/'
    download_file_name = 'data.zip'
    download_output_directory = './data'
    region_output_directory = './region_data'

    run_web_scraping(
        url=url,
        download_file_name=download_file_name,
        download_output_directory=download_output_directory)
    create_region_data_by_initial_csv(
        download_output_directory +
        '/' +
        download_file_name,
        region_output_directory)
