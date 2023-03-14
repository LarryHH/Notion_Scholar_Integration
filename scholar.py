from scholarly import scholarly

class Source:
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
        self.__init__()

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
            self.year = int(search_query['bib'].get('pub_year', None))
            self.venue = str(search_query['bib'].get('venue', None))
            self.link = str(search_query.get('eprint_url', None))
            self.citations = int(search_query.get('num_citations', None))
    

if __name__ == "__main__":
    source = Source()
    source.get_pub_by_title('V. Giovannetti, S. Lloyd, and L. Maccone, “Quantum random access memory,” Physical Review Letters, April 2008.')
    print(source)

