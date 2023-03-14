from scholarly import scholarly

def get_single_pub_by_title(title):
    """get single Scholar result from title search"""
    search_query = None
    try:
        search_query = scholarly.search_single_pub(title, filled = False)
    except IndexError as err:
        print(err)
    if search_query:
        name = search_query['bib'].get('title', None)
        authors = search_query['bib'].get('author', None)
        year = search_query['bib'].get('pub_year', None)
        venue = search_query['bib'].get('venue', None)
        link = search_query.get('eprint_url', None)
        citations = search_query.get('num_citations', None)

        print(name)
        print(authors)
        print(year)
        print(venue)
        print(link)
        print(citations)

if __name__ == "__main__":
    get_single_pub_by_title('Perception of physical stability and center of mass of 3D objects')

