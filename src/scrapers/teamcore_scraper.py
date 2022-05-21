import requests

from selenium import webdriver
from selenium.webdriver.common.by import By

from unidecode import unidecode

GECKO_DRIVER = './utils/geckodriver'


class TeamcoreScraper:
    def __init__(self, url, download_output_directory, download_file_name):
        self.url = url
        self.download_output_directory = download_output_directory
        self.download_file_name = download_file_name
        self.driver = webdriver.Firefox(executable_path=GECKO_DRIVER)

    def _get_element_by_xpath(self, xpath_string):
        """
        General abstraction to get elements by xpath. Avoiding method redefinition.
        """
        return self.driver.find_element(By.XPATH, xpath_string)

    def _get_elements_by_xpath(self, xpath_string):
        """
        General abstraction to get elements by xpath. Avoiding method redefinition.
        """
        return self.driver.find_elements(By.XPATH, xpath_string)

    def _click_last_selectors(self, last_n):
        """
        Click the last selectors, defined from last to first by last_n.
        """
        selectors_elements = self._get_elements_by_xpath(
            "//h2[@class='pane-title ctools-collapsible-handle']")
        for selector_element in selectors_elements[last_n:]:
            selector_element.click()

    def _get_actual_panel_links(self):
        """
        General abstraction to get actual panel links. Avoiding string redefinition.
        """
        return self._get_elements_by_xpath("//a[@class='facetapi-inactive']")

    def _get_url_by_name(self, name):
        """
        Retrieves each panel link. It will change after picking an option, so running this again is necessary.
        """
        panel_links = self._get_actual_panel_links()
        for panel_link in panel_links:
            link_name = unidecode(panel_link.text.split('\n')[0].split(
                '(')[0].lower().strip())  # Removing unnecesary text and lowercasing
            if link_name == name:
                url = panel_link.get_attribute('href')
                return url

    def _select_option(self, name, click_last_selectors=0):
        """
        General abstraction for option picking.
        """
        if click_last_selectors:
            # To enable the last hidden panel entries
            self._click_last_selectors(click_last_selectors)
        return self._get_url_by_name(name)

    def _set_selection_criteria(self, content_type, category, data_format):
        """
        Set the three steps in the selection criteria.
        """
        content_type_url = self._select_option(content_type)
        self.driver.get(content_type_url)
        print(f'Added {content_type} as Content Type')

        category_url = self._select_option(category)
        self.driver.get(category_url)
        print(f'Added {category} as Category')

        # In this case we just need one hidden panel entry
        data_format_url = self._select_option(
            data_format, click_last_selectors=1)
        self.driver.get(data_format_url)
        print(f'Added {data_format} as Data Format')

    def _set_search_term(self, report_name):
        """
        Write the report_name into the search input.
        """
        search_input_element = self._get_element_by_xpath(
            "//input[@class='form-control form-text']")
        search_input_element.send_keys(report_name)
        print(f'Set {report_name} in the search input')
        search_input_element.submit()

    def _execute_custom_behavior(self):
        """
        Click on the single link and downloading the file related to it.
        """
        self.driver.implicitly_wait(
            1)  # Webpage loads slower, so our scraper needs to wait.
        wanted_link_element = self._get_element_by_xpath(
            "//a[@title='Donaciones COVID-19 - [Ministerio de Economía y Finanzas - MEF]']")
        wanted_link_element.click()
        print(f'Clicking on wanted link (defined by end-user)')

        download_button_element = self._get_element_by_xpath(
            "//a[@title='Data - Donaciones Covid-19']/following-sibling::span/a")
        download_button_link = download_button_element.get_attribute('href')
        res = requests.get(download_button_link)
        print(
            f'Downloading data and saving into {self.download_output_directory}')
        # We save the file with this method to use the project internal folder
        # structure
        open(
            f'{self.download_output_directory}/{self.download_file_name}',
            'wb').write(
            res.content)

    def scrap_data(self, content_type, category, data_format, report_name):
        """
        Extracts data from the url defined in the class.

        This method is divided in three processes:
        - Set the selection criteria by using the content type, the category and data format
        - Set the search term by the report name
        - Execute custom behavior (defined by the end-user)

        Parameters
        ----------
        content_type : str
            A string representating the content type
        category : str
            A string representating the category
        data_format : str
            A string representating the data format
        report_name : str
            A string representating the report name
        """
        print(f'Navigating into {self.url}')
        self.driver.get(self.url)
        self._set_selection_criteria(content_type, category, data_format)
        self._set_search_term(report_name)
        self._execute_custom_behavior()
        self.driver.close()
        print(f'Finishing scraping process')
