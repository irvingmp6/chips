def get_help_menu() -> dict:
    menu = {}
    menu['debug'] = """Shows errors as standard out"""
    menu['desc'] = """A command-line tool that returns results from mainstream search engines."""
    menu['levels'] = """Controlls the depth of the search. Defaults to 0, the initial search engine pages"""
    menu['exclude-urls-with'] = """Specifies text the search should exclude"""
    menu['exclude-urls-with-from-file'] = """Specifies text the search should exclude from text file"""
    menu['only-urls-with'] = """Specifies the text the URLs should focus on"""
    menu['only-urls-with-from-file'] = """Specifies the text the URLs should focus on from text file"""
    menu['url-regex'] = """Regex pattern that controls the URLs searched"""
    menu['timeout'] = """Specifies the timeout threshold per search request"""
    menu['verbose'] = """Shows activity as standard out"""
    menu['save-results'] = """Writes the text from each visited page to file called chips.txt"""
    menu['save-urls'] = """Writes the urls from each visited page to a file called all_urls.txt"""
    menu['search-engines'] = """list of specific search engines to be queried"""
    menu['search_phrase'] = """Phrases you would normally enter in the search bar."""
    return menu
