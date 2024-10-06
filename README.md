# Web Scraper PDF-letöltéshez

Ez a projekt egy Python és Selenium alapú webes adatgyűjtőt tartalmaz, amely automatikusan navigál egy weboldalra, kiválasztja az aktív hatóanyagokat a legördülő menüből, letölti a kapcsolódó PDF-eket, és azokat helyileg tárolja. A projekt moduláris felépítésű, a különböző funkciók külön fájlokba vannak szervezve az átláthatóság és karbantarthatóság érdekében.

## Projekt Felépítése

/scraper_project/ │ ├── scraper/ │ ├── init.py # A scraper mappa csomaggá alakítása │ ├── browser_setup.py # A böngésző beállításainak és lezárásának kezelése │ ├── page_interactions.py # A weboldallal való interakciók kezelése (kiválasztás, kattintás stb.) │ ├── utils.py # Segédfunkciókat tartalmaz, pl. görgetés és letöltések figyelése │ └── scraper.py # A fő scraping logika (találatok kezelése, PDF letöltése) │ └── main.py # A scraper futtatásának belépési pontja

### Fájlok áttekintése

1. **`browser_setup.py`**  
   A böngésző indítását és lezárását kezeli egy headless Brave böngészővel, előre meghatározott letöltési beállításokkal. Funkciók:
   - `get_chrome_options()`: Böngésző beállítások konfigurálása (headless mód, letöltési könyvtár stb.)
   - `start_browser()`: Elindítja a Selenium WebDriver-t a megadott beállításokkal.
   - `stop_browser()`: Lezárja a WebDriver-t.

2. **`page_interactions.py`**  
   Meghatározza, hogyan lép kapcsolatba a scraper a weboldallal, mint például aktív hatóanyagok kiválasztása, szűrők törlése, és gombok kattintása. Funkciók:
   - `open_website()`: Megnyitja a célszerű weboldalt és megvárja a betöltést.
   - `select_active_ingredient()`: Kiválaszt egy konkrét hatóanyagot a legördülő menüből.
   - `click_search_button()`: Kattint a keresés gombra, hogy alkalmazza a szűrőket.
   - `clear_filters()`: Törli a szűrőket az egyes keresések után.

3. **`utils.py`**  
   Általános segédfunkciókat tartalmaz, amelyeket más modulokban újra lehet használni. Funkciók:
   - `scroll_to_element()`: Görget az adott elemhez a weboldalon.
   - `wait_for_downloads()`: Megvárja, amíg egy PDF letöltése befejeződik.

4. **`scraper.py`**  
   A fő scraping logikát valósítja meg, amely kezeli a keresési találatokat és a PDF fájlok letöltését. Funkciók:
   - `process_search_results()`: Végigmegy a keresési találatokon és kezeli a PDF letöltéseket.
   - `download_pdfs()`: Letölti a PDF fájlokat a megadott keresési eredményekhez.

5. **`main.py`**  
   A scraper belépési pontja. Ez a script hívja meg a szükséges funkciókat a weboldal betöltésére, hatóanyagok kiválasztására, PDF-ek letöltésére és a szűrők alaphelyzetbe állítására.

## Követelmények

Győződj meg róla, hogy a következők telepítve vannak a rendszereden:

- **Python 3.x**
- **Selenium**: Python csomag a webes böngészők automatizálásához.
- **Brave böngésző**: A web böngésző, amelyet a scrapinghez használunk (igény szerint helyettesíthető Chrommal).
- **ChromeDriver**: Az általad használt Brave vagy Chrome verziójával megfelelő verzió.

Selenium telepítése pip-pel:
```bash
pip install selenium
```
## Beállítás

1. **Klónozd a repót vagy töltsd le a projekt fájljait.**

2. **Győződj meg róla, hogy a Brave böngésző a következő útvonalon van telepítve:**

   
   C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe

3. **Töltsd le a megfelelő ChromeDriver verziót** [innen](https://sites.google.com/a/chromium.org/chromedriver/downloads) **és helyezd el egy általad választott mappába. Módosítsd az útvonalat a** `browser_setup.py` **fájlban:**

   ```python
   chrome_driver_path = "D:\\Prog\\Chromium\\chromedriver-win64\\chromedriver.exe"

4. **Állítsd be a PDF-ek letöltési könyvtárát a `browser_setup.py` fájlban:**
 ```python
   download_directory = "D:\\Prog\\Python\\Erik\\Hatóanyagok"```
