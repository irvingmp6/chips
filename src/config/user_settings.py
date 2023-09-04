class UserSettings:
    def __init__(self, args):
        self.args = args
        self.excluded_domains = self._get_excluded_domains()
        self.domains_of_interest = args.only_domains
        self.timeout = args.timeout
        self.verbose = self.args.verbose
        self.search_phrases = self.args.search_phrases
        self.search_engines = self._get_search_engines()
        self.save_results = self.args.save_results
        self.save_urls = self.args.save_urls
        self.debug = self.args.debug

    def _get_excluded_domains(self):
        domains = ["google.com"]
        domains.extend(self.args.exclude_domains)
        return domains

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

