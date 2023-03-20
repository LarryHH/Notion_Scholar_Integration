from scholarly import scholarly, ProxyGenerator

class Scholar:
    """single Google Soholar search result"""
    def __init__(self) -> None:
        self.name = None
        self.authors = None
        self.year = None
        self.venue = None
        self.link = None
        self.citations = None

    def __str__(self) -> str:
        return f'{self.name},{self.authors},{self.year},{self.citations},{self.venue},{self.link}'

    def reset(self):
        """reset object variables to None"""
        self.name = None
        self.authors = None
        self.year = None
        self.venue = None
        self.link = None
        self.citations = None

    def establish_proxy(self, scraper_api_key):
        """use ScraperAPI proxy"""
        pg = ProxyGenerator()
        success = pg.ScraperAPI(scraper_api_key)
        scholarly.use_proxy(pg)

    def get_pub_by_title(self, title):
        """get single Scholar result from title search"""
        search_query = None
        try:
            search_query = scholarly.search_single_pub(title, filled = False)
            print(search_query)
        except IndexError as err:
            print(err)
        if search_query:
            self.name = str(search_query['bib'].get('title', None))
            self.authors = list(search_query['bib'].get('author', None))
            self.venue = str(search_query['bib'].get('venue', None))
            self.link = str(search_query.get('eprint_url', None))
            try:
                self.year = int(search_query['bib'].get('pub_year', None))
            except:
                self.year = None
            try:
                self.citations = int(search_query.get('num_citations', None))
            except:
                self.citations = None
    

if __name__ == "__main__":
    scholar = Scholar("scraper_api_key")
    scholar.get_pub_by_title('V. Giovannetti, S. Lloyd, and L. Maccone, “Quantum random access memory,” Physical Review Letters, April 2008.')
    print(scholar)

