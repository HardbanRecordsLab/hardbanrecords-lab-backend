# integrations/toolost.py - Półautomatyczna integracja z Toolost przez Selenium

import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Przechowuj swoje dane logowania jako zmienne środowiskowe dla bezpieczeństwa
# W panelu Render.com, w sekcji "Environment", dodaj te zmienne.
TOOLOST_EMAIL = os.getenv("TOOLOST_EMAIL")
TOOLOST_PASSWORD = os.getenv("TOOLOST_PASSWORD")

class ToolostAutomator:
    """
    Automatyzuje proces dodawania wydań na platformie Toolost.com.
    """
    def __init__(self):
        options = webdriver.ChromeOptions()
        # Odkomentuj poniższą linię, aby skrypt działał w tle (bez widocznego okna przeglądarki)
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print("Przeglądarka do automatyzacji została uruchomiona.")

    def login(self):
        """
        Loguje się na konto Toolost.com.
        """
        if not TOOLOST_EMAIL or not TOOLOST_PASSWORD:
            print("BŁĄD: Zmienne środowiskowe TOOLOST_EMAIL i TOOLOST_PASSWORD nie są ustawione.")
            return False
            
        print("Przechodzę na stronę logowania Toolost...")
        self.driver.get("https://toolost.com/login")
        sleep(3) # Czekamy na załadowanie wszystkich elementów strony

        try:
            # Znajdujemy pola na email i hasło oraz przycisk logowania
            email_input = self.driver.find_element(By.NAME, "email")
            password_input = self.driver.find_element(By.NAME, "password")
            login_button = self.driver.find_element(By.TAG_NAME, "button")

            print("Wprowadzam dane logowania...")
            email_input.send_keys(TOOLOST_EMAIL)
            password_input.send_keys(TOOLOST_PASSWORD)
            login_button.click()
            sleep(5) # Czekamy na przetworzenie logowania

            # Sprawdzamy, czy logowanie się udało (np. przez sprawdzenie adresu URL)
            if "dashboard" in self.driver.current_url:
                print("Logowanie do Toolost zakończone sukcesem!")
                return True
            else:
                print("Logowanie nie powiodło się. Sprawdź dane logowania i selektory.")
                return False
        except Exception as e:
            print(f"Wystąpił błąd podczas logowania: {e}")
            return False

    def create_release(self, release_data: dict):
        """
        Wypełnia formularz dodawania nowego wydania muzycznego.
        'release_data' to słownik zawierający np. 'title', 'artist', 'audio_path', 'cover_path'.
        """
        print(f"Rozpoczynam proces tworzenia wydania dla '{release_data['title']}'...")
        
        # KROK 1: Przejdź do strony tworzenia nowego wydania (musisz znaleźć właściwy URL)
        # self.driver.get("https://toolost.com/release/new") # <-- ZMIEŃ NA POPRAWNY ADRES URL
        # sleep(3)

        # KROK 2: Znajdź i wypełnij pola formularza
        # To jest najważniejsza część, którą musisz uzupełnić samodzielnie.
        # Użyj narzędzi deweloperskich w przeglądarce (F12 -> "Zbadaj element"),
        # aby znaleźć 'name', 'id', lub 'xpath' każdego pola.
        
        # Przykład:
        # title_input = self.driver.find_element(By.NAME, "release_title")
        # title_input.send_keys(release_data['title'])
        #
        # artist_input = self.driver.find_element(By.NAME, "artist_name")
        # artist_input.send_keys(release_data['artist'])
        #
        # audio_upload_input = self.driver.find_element(By.ID, "audio-upload-input")
        # audio_upload_input.send_keys(release_data['audio_path']) # Musi to być pełna ścieżka do pliku na serwerze
        
        print("UWAGA: Funkcja 'create_release' jest szablonem i wymaga implementacji.")
        print("Proces zakończony (symulacja).")
        return True

    def close(self):
        """
        Zamyka przeglądarkę i kończy sesję.
        """
        if self.driver:
            self.driver.quit()
            print("Przeglądarka została zamknięta.")
