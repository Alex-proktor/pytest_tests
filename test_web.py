from selenium.webdriver import Keys

from GooglePages import SearchHelper


def test_google_search_alarislabs(browser):
    """
    1. Переход в поисковик Google
    2. Ввод текста "Alaris labs" в строку поиска
    3. Наличие ссылки "https://www.alarislabs.com" в результатах поиска.
    """
    print(f'')
    google_main_page = SearchHelper(browser)
    google_main_page.go_to_site()
    google_main_page.enter_word("Alaris labs").send_keys(Keys.RETURN)
    urls = google_main_page.get_urls()

    assert "https://www.alarislabs.com" in urls
