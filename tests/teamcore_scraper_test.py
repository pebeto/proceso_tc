from src.scrapers.teamcore_scraper import TeamcoreScraper
from selenium.webdriver.common.by import By
from selenium import webdriver


URL = 'https://www.datosabiertos.gob.pe/'
GECKO_DRIVER = './utils/geckodriver'

SCRAPER = TeamcoreScraper(URL, './tests/temp', 'data.zip')
DRIVER = webdriver.Firefox(executable_path=GECKO_DRIVER)

SCRAPER.driver.get(URL)
DRIVER.get(URL)


def test_get_element_by_xpath():
    xpath_str = "//div[@class='view-header']"

    by_scraper_method_text = SCRAPER._get_element_by_xpath(xpath_str).text
    by_driver_text = DRIVER.find_element(By.XPATH, xpath_str).text

    assert by_scraper_method_text == by_driver_text


def test_get_elements_by_xpath():
    xpath_str = "//a[@class='facetapi-inactive']"

    by_scraper_method_len = len(SCRAPER._get_elements_by_xpath(xpath_str))
    by_driver_text = len(DRIVER.find_elements(By.XPATH, xpath_str))

    assert by_scraper_method_len == by_driver_text


def test_click_last_selectors():
    SCRAPER._click_last_selectors(last_n=2)

    n_panel_options = len(SCRAPER._get_elements_by_xpath(
        "//div[contains(@class, 'ctools-collapsed')]"))

    assert n_panel_options == 0


def test_get_actual_panel_links():
    xpath_str = "//a[@class='facetapi-inactive']"

    by_scraper_method_len = len(SCRAPER._get_actual_panel_links())
    by_driver_text = len(DRIVER.find_elements(By.XPATH, xpath_str))

    assert by_scraper_method_len == by_driver_text


def test_get_url_by_name():
    by_scraper_method_link = SCRAPER._get_url_by_name('entidades')

    assert by_scraper_method_link == f'{URL}search/type/group?sort_by=changed'


def test_select_option():
    by_scraper_method_link = SCRAPER._select_option('entidades')

    assert by_scraper_method_link == f'{URL}search/type/group?sort_by=changed'


def test_set_selection_criteria():
    SCRAPER._set_selection_criteria('dataset', 'desarrollo social', 'xls')
    by_scraper_method_link = SCRAPER.driver.current_url

    assert by_scraper_method_link == f'{URL}search/field_resources%253Afield_format/xls-16/field_topic/desarrollo-social-338/type/dataset?sort_by=changed'


def test_set_search_term():
    SCRAPER._set_search_term('sbn')
    by_scraper_method_view_header = SCRAPER._get_element_by_xpath(
        "//div[@class='view-header']").text

    assert by_scraper_method_view_header == '21 Distribución de Datos'
