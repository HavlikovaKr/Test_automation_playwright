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


def test_vyhledani_zbozi_vlozeni_do_kosiku(page):
    """Testovaní vyhledávání zboží a potvrzení o vložení do košíku"""

    # vyhledání webové stránky
    page.goto("https://www.brainmarket.cz")

    # čekání na vyskočení slevového okna
    discount = page.get_by_text("×").click()
    accept_button = page.get_by_test_id("buttonCookiesAccept").click()

    # nalezení search inputu a vyhledání slova "BrainMax NeuroHacker"
    search_input = page.get_by_test_id("searchInput")
    search_input.fill("BrainMax NeuroHacker")

    # klinutí na tlačítko vyhledat a čekání na načtení stránky
    search_button = page.get_by_test_id("searchBtn").click()
    page.wait_for_load_state("networkidle")

    # nalezení produktu a klinutí na něj
    product_locator = page.locator(
        "span[data-micro='name']:has-text('BrainMax NeuroHacker, Dopamine Upgrade! 60 rostlinných kapslí')")
    product_locator.wait_for(state='visible', timeout=5000)
    product_locator.click()

    # kliknutí na tlačítko "Přidat do košíku" a čekání na jeho viditelnost
    add_to_cart_button = page.get_by_role("button", name="Přidat do košíku")
    add_to_cart_button.wait_for(state='visible', timeout=5000)
    add_to_cart_button.click()

    # ověření, že se produkt přidal do košíku pomocí propsání textu "Přidáno do košíku"
    page.screenshot(path="screenshot.png")

    added_to_cart_locator = page.locator("div.h1:has-text('Přidáno do košíku')")
    added_to_cart_locator.wait_for(timeout=5000)

    expected_text = "Přidáno do košíku"
    assert added_to_cart_locator.inner_text() == expected_text