import requests
from socket import timeout as stimeout
from bs4 import BeautifulSoup
from requests.exceptions import ReadTimeout


class Scraper:
    @staticmethod
    def scrape_website(url, timeout, verbose=False, verbose_urls=False, debug=False):
        soup = ""
        status_code = "<NO STATUS CODE>"
        try:
            response = requests.get(url, timeout=timeout)
            status_code = response.status_code

            if status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')

            else:
                headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36'}
                response = requests.get(url, headers=headers)
                if status_code == 200:
                    soup = BeautifulSoup(response.text, 'lxml')
                if verbose or verbose_urls:
                    print(f"URL::: {url} | Response::: {status_code}")

        except (requests.exceptions.ConnectTimeout, ReadTimeout, stimeout) as e:
            if debug:
                print(f"URL::: {url} | Response::: {status_code}")

        return soup