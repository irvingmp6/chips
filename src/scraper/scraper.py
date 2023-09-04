from bs4 import BeautifulSoup
from requests import ReadTimeout
import requests

class Scraper:
    @staticmethod
    def scrape_website(url, timeout, verbose=False, verbose_urls=False, debug=False):
        soup = ""
        try:
            response = requests.get(url, timeout=timeout)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')

            else:
                headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36'}
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'lxml')
                if verbose or verbose_urls:
                    print(f"URL::: {url} | Response::: {response.status_code}")

        except (requests.exceptions.ConnectTimeout, ReadTimeout) as e:
            if debug:
                print(f"URL::: {url} | Response::: {response.status_code}")

        return soup