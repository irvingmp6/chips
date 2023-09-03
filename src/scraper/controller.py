import argparse
from collections import namedtuple

from bs4 import BeautifulSoup

from src.config.user_settings import UserSettings
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

    def search(self):
        """Controller main entry - Prepares and searches initial urls, creating more urls from
        the initial pages. Searches those and returns relevant results.
        """
        timeout = self.user_settings.timeout
        verbose = self.user_settings.verbose
        for page in self.initial_pages:
            if self.user_settings.verbose:
                print(f"parent URL::: {page.url}")
            page.soup = Scraper.scrape_website(page.url, timeout=timeout, verbose=verbose)
        potential_pages = self._get_potential_pages(self.initial_pages)
        pages_of_interest = self._get_pages_of_interest(potential_pages)
        for page in pages_of_interest:
            page.soup = Scraper.scrape_website(page.url, timeout=timeout, verbose=verbose)
            if page.soup:
                try:
                    print(page.soup.get_text())
                except UnicodeEncodeError as e:
                    if verbose:
                        print(f"parent URL::: {page.url} | Error::: {e}")
                    continue

    def _get_potential_pages(self, parent_pages) -> list:
        """ Returns list of child Pages, where each child Page 
        is a link found in its parent Page
        """
        child_pages = []
        for parent_page in parent_pages:
            search_engine = parent_page.search_engine
            try:
                for a in parent_page.soup.find_all('a', href=True):
                    url = a['href']
                    url_start = url.find("https")
                    if url_start != -1:
                        url = url[url_start:]
                        extra = url.find("&sa=U")
                        if extra != -1:
                            url = url[:extra]
                        child_pages.append(Page(search_engine, url, None))            
            except TypeError:
                continue
        return child_pages

    def _get_pages_of_interest(self, candidates):
        pages_of_interest = self._remove_excluded_domains(candidates)
        pages_of_interest = self._only_include_domains_of_interest(pages_of_interest)
        return pages_of_interest

    def _remove_excluded_domains(self, pages_of_interest):
        pages = []
        excluded_domains = self.user_settings.excluded_domains
        if len(excluded_domains):
            for page in pages_of_interest:
                for exlucded_domain in excluded_domains:
                    if exlucded_domain not in page.url:
                        pages.append(page)
        else:
            pages = pages_of_interest
        return pages

    def _only_include_domains_of_interest(self, pages_of_interest):
        pages = []
        domains_of_interest = self.user_settings.domains_of_interest
        if len(domains_of_interest):
            for page in pages_of_interest:
                for domain_of_interest in domains_of_interest:
                    if domain_of_interest in page.url:
                        pages.append(page)
        else:
            pages = pages_of_interest
        return pages