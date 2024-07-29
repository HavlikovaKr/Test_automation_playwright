# Engeto Testing Project 2
Tento projekt se zaměřuje na automatizované testování webové stránky pomocí frameworku Playwright.

## Dependencies
- [pytest](https://docs.pytest.org/en/7.1.x/contents.html)
- [pytest-playwright](https://playwright.dev/python/docs/intro)

## Launch
To launch all tests:

```bash
pytest
```

To launch each test:

```bash
pytest test_web_auto.py::test_prihlaseni_zakaznika
pytest test_web_auto.py::test_vyhledani_zbozi_vlozeni_do_kosiku
pytest test_web_auto.py::test_pridano_do_oblibenych
```
 
## Tests 
- test_prihlaseni_zakaznika: Ověření správného příhlášení registrovaného zákazníka. 
- test_vyhledani_zbozi_vlozeni_do_kosiku: Nalezení zvoleného zboží ("NeuroHacker") a zkouška vložení do košíku. 
- test_pridano_do_oblibenych: Nalezení zvoleného zboží ("Matcha"), zda jde přidat do oblíbených položek. 
