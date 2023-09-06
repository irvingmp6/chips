import argparse
import re
from collections import namedtuple

from bs4 import BeautifulSoup

from src.interface.user_settings import UserSettings
from .scraper import Scraper

url_encoding = {
    " ": "%20",
    "'": "%27"
}

def scrub_query_string(query_string):
    """ Replaces characters in query string with proper encoding"""
    for character, encoding in url_encoding.items():
        query_string = query_string.replace(character, encoding)
    return query_string


class Page:
    """ Object to store BeatifulSoup and its metadata"""
    def __init__(self, search_engine:str, url:str, soup:BeautifulSoup=None) -> None:
        self.search_engine = search_engine
        self.url = url
        self.soup = soup


class Controller:
    def __init__(self, args:argparse.Namespace) -> None:
        """ Handles the business logic """
        self.user_settings = UserSettings(args)
        self.initial_pages = self.initial_pages()
        self.results = []
        self.all_urls = []

    def initial_pages(self) -> list:
        """ Returns list of Pages, where each Page contains 
        a url representing the initial searches
        """
        pages = []
        for search_engine, website in self.user_settings.search_engines.items():
            url = website + "q=" + self._get_query_string()
            pages.append(Page(search_engine, url, None))
        return pages

    def _get_query_string(self):
        """ Appends the user's search phrases as query strings 
        to the search pages
        """
        query_string = "+".join([search_phrase for search_phrase in self.user_settings.search_phrases])
        query_string = scrub_query_string(query_string)
        return query_string

    def start_process(self):
        """Controller main entry - Prepares and searches initial urls, creating more urls from
        the initial pages. Searches those and returns relevant results.
        """
        timeout = self.user_settings.timeout
        verbose = self.user_settings.verbose
        debug = self.user_settings.debug
        levels = self.user_settings.levels

        if debug:
            print(f"Search {0} set of pages")
        for page in self.initial_pages:
            self.all_urls.append(page.url)
            page.soup = Scraper.scrape_website(page.url, timeout=timeout, verbose=verbose, debug=debug)
            self.results.append(page.soup)
        potential_pages = self._get_potential_pages(self.initial_pages)
        pages_of_interest = self._get_pages_of_interest(potential_pages)


        for level in range(0, levels):
            if debug:
                print(f"Search {level+1} set of pages")
            self.search_pages(pages_of_interest)
            potential_pages = self._get_potential_pages(pages_of_interest)
            pages_of_interest = self._get_pages_of_interest(potential_pages)

        if self.user_settings.save_results:
            self.save_results()

        if self.user_settings.save_urls:
            self.save_urls()

    def _get_potential_pages(self, parent_pages) -> list:
        """ Returns list of child Pages, where each child Page 
        is a link found in its Page
        """
        child_pages = []
        for parent_page in parent_pages:
            search_engine = parent_page.search_engine
            if parent_page.soup:
                try:
                    for a in parent_page.soup.find_all('a', href=True):
                        url = a['href']
                        url_start = url.find("https")
                        if url_start != -1:
                            url = url[url_start:]
                            extra = url.find("&sa=U")
                            if extra != -1:
                                url = url[:extra]
                            if url not in self.all_urls:
                                child_pages.append(Page(search_engine, url, None))            
                except TypeError:
                    continue
        return child_pages

    def search_pages(self, pages_of_interest):
        timeout = self.user_settings.timeout
        verbose = self.user_settings.verbose
        debug = self.user_settings.debug

        for page in pages_of_interest:
            self.all_urls.append(page.url)
            page.soup = Scraper.scrape_website(page.url, timeout=timeout, verbose=verbose, debug=debug)
            if page.soup:
                self.results.append(page.soup)
                try:
                    if verbose:
                        print(page.soup.get_text())
                except UnicodeEncodeError as e:
                    continue

    def _get_pages_of_interest(self, candidates):
        pages_of_interest = self._remove_excluded_urls(candidates)
        pages_of_interest = self._remove_previsisted_pages(pages_of_interest)
        pages_of_interest = self._filter_using_regex(pages_of_interest)
        pages_of_interest = self._only_include_urls_of_interest(pages_of_interest)
        return pages_of_interest

    def _remove_excluded_urls(self, pages_of_interest):
        pages = []
        excluded_urls = self.user_settings.excluded_urls
        if len(excluded_urls):
            for page in pages_of_interest:
                for exlucded_url in excluded_urls:
                    contains_domain = page.url.find(exlucded_url) > -1
                    if contains_domain:
                        break
                if contains_domain:
                    continue
                pages.append(page)
        else:
            pages = pages_of_interest
        return pages
    
    def _filter_using_regex(self, potential_pages):
        pages = []
        regex_pattern = fr"{self.user_settings.url_regex}"
        regex = re.compile(regex_pattern)
        for potential_page in potential_pages:
            if regex.match(potential_page.url):
                pages.append(potential_page)
        return pages

    def _remove_previsisted_pages(self, pages_of_interest):
        pages = []
        for page_of_interest in pages_of_interest:
            if page_of_interest.url not in self.all_urls:
                pages.append(page_of_interest)
        return pages

    def _only_include_urls_of_interest(self, pages_of_interest):
        pages = []
        urls_of_interest = self.user_settings.urls_of_interest
        if len(urls_of_interest):
            for page in pages_of_interest:
                for domain_of_interest in urls_of_interest:
                    if domain_of_interest in page.url:
                        pages.append(page)
        else:
            pages = pages_of_interest
        return pages

    def save_results(self):
        with open("chips.txt", "w") as f:
            for r in self.results:
                try:
                    f.write(r)
                    f.write("\n++++++++++++++++++++++++\n++++++++++++++++++++++++\n")
                except TypeError:
                    continue

    def save_urls(self):
        with open("all_urls.txt", "w") as f:
            for url in self.all_urls:
                try:
                    f.write(url+"\n")
                except TypeError as e:
                    print(e)
                    continue