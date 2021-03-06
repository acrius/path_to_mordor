#path_to_mordor

Package to organization scraping based on bs4.

Simple example.

<!-- language: lang-py -->
    """
    The module contains the rules of scraping.
    """
    from ptm import Frodo
    from ptm.path_actions import gpagins, gpages, gresults
    from ptm.result_actions import KeyRealtionships, gvalues, gtexts, gattrs
    from treasy import BookSearchDB
    from treasy.session import create_session
    from smithy.preparing import prepare

    RESORCE = 'http://www.labirint-bookstore.ru'
    START_PAGE = 'http://www.labirint-bookstore.ru/books'

    def result_proccessing(result_set):
        """
        This function proccess the results.
        """
        db = BookSearchDB(create_session())
        result = prepare(result_set, {'name': 'labirint-bookstore', 'url': 'http://www.labirint-bookstore.ru'})
        print(result)
        description = result['description'].split('||')
        if len(description) > 2:
            result['description'] = description[2].strip()
        db.update_book(result)

    KEY_RELATIONSHIPS = KeyRealtionships({
        'ISBN:': 'isbn_numbers',
        'Издательство:': 'publisher',
        'Автор:': 'authors',
        'Переводчик:': 'translators',
        'Иллюстратор': 'illustrators',
        'Серия:': 'series',
        'Жанр:': 'genres',
        'Год выпуска:': 'year',
        'Тип обложки:': 'cover_format',
        'Страниц:': 'page_number',
        'Масса:': 'weidth',
        'Размеры:': 'size',
        'Иллюстратор:': 'illustrators'})

    RESULTS = {
        KEY_RELATIONSHIPS: gvalues(gtexts('div', attrs={'class': 'book-info-left'}),
                                   gtexts('div', attrs={'class': 'book-info-right'})),
        'description': gtexts('div', attrs={'id': 'bigcard-description'}, separator="||"),
        'title': gattrs('img', attrs={'class': 'img-cover-book'}, target_attribute='alt')
    }

    PATH = {
        gpagins(pagin_template='?page=', start_page_number=1, finish_page_number=10): {
                gpages('div', attrs={'class': 'books-name'}):
                    gresults(result_proccessing, result_map=RESULTS)
        }
    }

    def run(rucksack):
        """
        Run travel. This function triggers scraping.
        """
        frodo = Frodo(RESORCE, START_PAGE, PATH, rucksack)
        frodo.run()
