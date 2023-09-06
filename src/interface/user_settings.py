class UserSettings:
    def __init__(self, args):
        self.args = args
        self.excluded_urls = self._get_excluded_urls()
        self.urls_of_interest = self._get_urls_of_interest()
        self.timeout = args.timeout
        self.verbose = self.args.verbose
        self.search_phrases = self.args.search_phrases
        self.search_engines = self._get_search_engines()
        self.save_results = self.args.save_results
        self.save_urls = self.args.save_urls
        self.debug = self.args.debug
        self.levels = self.args.levels
        self.url_regex = self.args.url_regex

    def _get_excluded_urls(self):
        domains = ["google.com"]
        domains.extend(self.args.exclude_urls_with)
        file = self.args.exclude_urls_with_from_file
        domains.extend(self._get_domains_from_file(file))
        return domains

    def _get_urls_of_interest(self):
        urls = self.args.only_urls_with
        if len(urls):
            return urls
        file = self.args.only_urls_with_from_file
        return self._get_domains_from_file(file)
        
    def _get_domains_from_file(self, file):
        doi = []
        if file:
            with open(file) as f:
                for r in f:
                    domain = r.strip()
                    doi.append(domain)
        return doi

    def _get_search_engines(self):
        requested_search_engines = self.args.search_engines
        available_search_engines = {
            "ask": "https://ask.com/web?l=dir&",
            "bing": "https://bing.com/search?",
            "google": "https://google.com/search?",
        }
        use_search_engines = {}
        if len(requested_search_engines):
            for requested_search_engine in requested_search_engines:
                use_search_engines[requested_search_engine] = available_search_engines.get(requested_search_engine, "")
        else:
            use_search_engines = available_search_engines
        return use_search_engines

