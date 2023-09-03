def get_help_menu() -> dict:
    menu = {}
    menu['desc'] = """A command-line tool that returns results from mainstream search engines."""
    menu['exclude-domains'] = """Specifies the domain(s) the search should exclude"""
    menu['only-domains'] = """Specifies the domain(s) the search should focus on"""
    menu['timeout'] = """Specifies the timeout threshold per search request"""
    menu['verbose'] = """Shows activity as standard out"""
    menu['search-engines'] = """list of specific search engines to be queried"""
    menu['search_phrase'] = """Phrases you would normally enter in the search bar."""
    return menu
