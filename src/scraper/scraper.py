from bs4 import BeautifulSoup
import requests

class Scraper:
    @staticmethod
    def scrape_website(url, timeout, verbose=False):
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
                if verbose:
                    print(f"URL::: {url} | Response::: {response.status_code}")

        except requests.exceptions.ConnectTimeout as e:
            if verbose:
                print(f"URL::: {url} | Response::: {response.status_code}")

        return soup