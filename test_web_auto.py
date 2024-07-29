# import page
import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture()
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, slow_mo=500)
        yield browser
        browser.close()


@pytest.fixture()
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


def test_prihlaseni_zakaznika(page):
    """Testování přihlášení zákazníka do uživatelského menu přes zkušební email"""

    # vyhledání webové stránky
    page.goto("https://www.brainmarket.cz", timeout=50000)

    # čekání na vyskočení slevového okna
    discount = page.get_by_text("×").click()
    accept_button = page.get_by_test_id("buttonCookiesAccept").click()

    # nalezení přihlášení a klinutí na něj
    login = page.get_by_role("link", name="").click()

    # vyplnění přihlašovacího emailu
    input_email = page.get_by_test_id("inputEmail")
    input_email.fill("kikec6712@seznam.cz")

    # vyplnění hesla
    input_password = page.get_by_test_id("inputPassword")
    input_password.fill("123456789")

    # kliknutí na potvrzující tlačítko a čekání na načtení zákaznického menu
    button_submit = page.get_by_test_id("buttonSubmit").click()

    page.wait_for_load_state("networkidle")

    # ověření, že se skutečně zákazník nachází v zákaznickém menu, podle tlačítka odhlásit
    button_signout = page.locator('a[data-testid="buttonSignout"]')

    assert button_signout.is_visible(), "Logout button is not visible on the page."
