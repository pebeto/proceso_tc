import os
from src.tasks.datos_abiertos_task import create_region_data_by_initial_csv
from src.tasks.datos_abiertos_task import run_web_scraping


URL = 'https://www.datosabiertos.gob.pe/'
DOWNLOAD_FILE_NAME = 'data.zip'
DOWNLOAD_OUTPUT_DIRECTORY = './tests/temp'
REGION_OUTPUT_DIRECTORY = './tests/temp/region'


def test_run_web_scraping():
    run_web_scraping(
        url=URL,
        download_file_name=DOWNLOAD_FILE_NAME,
        download_output_directory=DOWNLOAD_OUTPUT_DIRECTORY)

    assert os.path.exists(f'{DOWNLOAD_OUTPUT_DIRECTORY}/{DOWNLOAD_FILE_NAME}')


def test_create_region_data_by_initial_csv():
    create_region_data_by_initial_csv(
        f'{DOWNLOAD_OUTPUT_DIRECTORY}/{DOWNLOAD_FILE_NAME}',
        REGION_OUTPUT_DIRECTORY)

    assert len(os.listdir(REGION_OUTPUT_DIRECTORY))
