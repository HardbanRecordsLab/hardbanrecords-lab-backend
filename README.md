# hardbanrecords-lab-backend
Backend services for the HardbanRecords Lab platform (FastAPI)
# **Kompleksowy Raport i Dokumentacja Projektu: HardbanRecords Lab**

Wersja: 1.0  
Data: 14 sierpnia 2025  
Autor: Ekspert ds. Audytu i Dokumentacji IT

# **1\. Audyt i Raport Stanu Projektu**

## **1.1. Ocena Ogólna**

Projekt HardbanRecords Lab znajduje się w **początkowej fazie rozwoju (MVP)**, która została zrealizowana z sukcesem. Położono solidne fundamenty pod dalszą rozbudowę, weryfikując kluczowe założenia technologiczne i architektoniczne. Aplikacja backendowa (auth-service) została pomyślnie wdrożona w środowisku chmurowym i jest w stanie zarządzać podstawowymi operacjami na użytkownikach, co stanowi krytyczny kamień milowy.

## **1.2. Analiza Szczegółowa**

| Kategoria | Ocena i Stan Aktualny |
| :---- | :---- |
| **Architektura** | **Bardzo Dobry.** Wybrano nowoczesną, odseparowaną architekturę (decoupled) z frontendem na WordPress i backendem w formie mikroserwisów FastAPI. Takie podejście zapewnia doskonałą skalowalność i elastyczność w przyszłości. |
| **Technologia** | **Bardzo Dobry.** Stos technologiczny oparty na Pythonie/FastAPI, PostgreSQL i WordPressie jest nowoczesny, wydajny i wspierany przez silne społeczności open-source. Wykorzystanie darmowych planów (Free Tier) na Render.com jest strategicznie poprawne dla fazy MVP. |
| **Bezpieczeństwo** | **Dobry.** Podstawy są solidne: uwierzytelnianie oparte na tokenach JWT, hashowanie haseł (bcrypt), zarządzanie sekretami przez zmienne środowiskowe. Wymaga dalszego rozwoju w zakresie ochrony przed atakami XSS i implementacji ról. |
| **UX/UI** | **W Trakcie Definiowania.** Frontend istnieje jako działająca instancja WordPress z zaawansowanymi wtyczkami (Elementor, Tutor LMS), ale docelowe panele użytkownika, komunikujące się z backendem, nie zostały jeszcze zaimplementowane. |
| **Wydajność** | **Wystarczający (dla MVP).** Darmowe plany hostingowe (iFastNet, Render) są adekwatne dla fazy deweloperskiej i początkowego ruchu. Wymagane będzie monitorowanie i planowanie skalowania wraz ze wzrostem liczby użytkowników. |
| **Jakość Kodu** | **Dobry.** Kod backendu jest podzielony na logiczne moduły (auth\_app, common) i pliki (crud, schemas, models), co jest zgodne z najlepszymi praktykami. Wymaga dalszej standaryzacji (np. docstringi, typowanie). |
| **Integracje** | **W Trakcie Planowania.** Zdefiniowano kluczowe integracje (Too Lost, KDP, MailerLite, AI), ale żadna nie została jeszcze zaimplementowana. |
| **Zgodność** | **W Trakcie Planowania.** Projekt zakłada zgodność z RODO/GDPR, ale mechanizmy (np. zgody, eksport danych) nie zostały jeszcze wdrożone. |

## **1.3. Analiza SWOT**

### **Mocne Strony (Strengths)**

* **Spójna i ambitna wizja** poparta szczegółową dokumentacją.  
* **Nowoczesna, skalowalna architektura** oparta na sprawdzonych technologiach open-source.  
* **Niski próg wejścia i minimalne koszty początkowe** dzięki wykorzystaniu darmowych usług.  
* **Ukończony i działający moduł uwierzytelniania**, co jest najtrudniejszą częścią fundamentów.

### **Słabe Strony (Weaknesses)**

* **Zależność od zewnętrznych API** (szczególnie Too Lost), których dostępność i warunki mogą się zmieniać.  
* **Potencjalna złożoność integracji** frontendu (WordPress/JS) z backendem (FastAPI).  
* **Brak zaimplementowanych kluczowych funkcji biznesowych** (dystrybucja muzyki, książek).

### **Ryzyka (Risks)**

* **Ryzyko Dostępności API Partnerów:** Brak uzyskania dostępu do API kluczowych partnerów (np. Too Lost) może zablokować rozwój głównych modułów.  
* **Ryzyko Wydajnościowe:** Darmowe plany hostingowe mogą okazać się niewystarczające przy wzroście ruchu, co wymusi nieplanowane koszty.  
* **Ryzyko Bezpieczeństwa:** Przechowywanie tokenów JWT w localStorage na froncie WordPressa wymaga dodatkowych zabezpieczeń przed atakami XSS.

### **Rekomendacje**

1. **Natychmiastowe Działania:** Dokończyć moduł auth-service poprzez implementację ochrony endpointów. To odblokuje dalsze prace.  
2. **Priorytet Krótkoterminowy:** Rozpocząć proces uzyskiwania dostępu do API Too Lost. Równolegle, rozpocząć budowę szkieletu serwisu music\_app (modele, schematy, podstawowe CRUD).  
3. **Priorytet Średnioterminowy:** Zbudować pierwszy w pełni działający przepływ (end-to-end flow) dla jednego modułu (np. artysta rejestruje się, loguje, tworzy wydanie muzyczne w panelu, a dane są zapisywane w bazie).

# **2\. Lista Zadań Projektu (To-Do List)**

## **Backend**

* \[x\] Zdefiniowanie architektury mikroserwisów (FastAPI).  
* \[x\] Utworzenie struktury monorepozytorium na GitHubie.  
* \[x\] Implementacja serwisu uwierzytelniania (auth-service).  
  * \[x\] Endpoint rejestracji (/register).  
  * \[x\] Endpoint logowania (/login) i generowanie tokenów JWT.  
  * \[x\] Ochrona endpointów i weryfikacja tokenów (/users/me).  
* \[ \] Implementacja serwisu muzycznego (music\_app).  
  * \[x\] Stworzenie modelu danych (MusicRelease).  
  * \[x\] Stworzenie schematów Pydantic.  
  * \[x\] Stworzenie logiki CRUD.  
  * \[x\] Implementacja endpointów API (tworzenie, listowanie).  
  * \[ \] Implementacja logiki przesyłania plików (audio, okładki) na S3/Cloud.  
  * \[ \] Integracja z API Too Lost.  
* \[ \] Implementacja serwisu książkowego (books\_app).  
  * \[ \] Stworzenie modelu danych (Book).  
  * \[ \] Stworzenie schematów Pydantic.  
  * \[ \] Implementacja logiki CRUD.  
  * \[ \] Implementacja konwersji plików (DOCX \-\> EPUB/MOBI).  
  * \[ \] Integracja z API partnerów (KDP, Draft2Digital).  
* \[ \] Implementacja serwisu AI (prometheus\_app).  
  * \[ \] Stworzenie endpointów do generowania tekstu.  
  * \[ \] Stworzenie endpointów do generowania obrazów.

## **Frontend (WordPress)**

* \[x\] Konfiguracja hostingu, domeny i instalacja WordPressa.  
* \[x\] Instalacja kluczowych wtyczek (Elementor, WooCommerce, Tutor LMS).  
* \[ \] Stworzenie strony logowania i rejestracji.  
  * \[ \] Napisanie skryptu JS do komunikacji z endpointami /register i /login.  
  * \[ \] Implementacja logiki zapisu i odczytu tokena JWT z localStorage.  
* \[ \] Zbudowanie głównego panelu użytkownika (Dashboard).  
* \[ \] Zbudowanie panelu do zarządzania muzyką.  
  * \[ \] Formularz dodawania nowego wydania.  
  * \[ \] Widok listy istniejących wydań.  
* \[ \] Zbudowanie panelu do zarządzania książkami.  
* \[ \] Integracja z WooCommerce (automatyczne tworzenie produktów).  
* \[ \] Integracja z Tutor LMS.

## **Baza Danych (PostgreSQL)**

* \[x\] Utworzenie instancji bazy danych na Render.com.  
* \[x\] Zdefiniowanie schematu tabeli users.  
* \[x\] Zdefiniowanie schematu tabeli music\_releases.  
* \[ \] Zdefiniowanie schematu tabeli books.  
* \[ \] Opracowanie strategii backupu i odzyskiwania danych.

## **UX/UI**

* \[ \] Zaprojektowanie makiet (wireframes) dla paneli użytkownika.  
* \[ \] Opracowanie spójnego systemu designu (kolory, typografia, komponenty).  
* \[ \] Przeprowadzenie testów użyteczności z potencjalnymi użytkownikami.

## **Testy**

* \[x\] Przygotowanie pliku test.http do testowania API auth-service.  
* \[ \] Rozbudowa test.http o testy dla music\_app i books\_app.  
* \[ \] Opracowanie planu testów manualnych dla frontendu.  
* \[ \] Wdrożenie testów jednostkowych dla logiki backendu (rekomendowane).

## **Dokumentacja**

* \[x\] Stworzenie wstępnej dokumentacji projektowej (niniejszy dokument).  
* \[ \] Stworzenie dokumentacji API (np. przy użyciu Swagger UI w FastAPI).  
* \[ \] Przygotowanie dokumentacji dla użytkownika końcowego (FAQ, tutoriale).

## **Integracje**

* \[ \] Uzyskanie kluczy i dokumentacji do API Too Lost.  
* \[ \] Zbadanie możliwości integracji API z Amazon KDP i Draft2Digital.  
* \[ \] Skonfigurowanie integracji z MailerLite.  
* \[ \] Skonfigurowanie n8n do automatyzacji procesów.

## **Marketing**

* \[ \] Przygotowanie strategii marketingowej dla MVP.  
* \[ \] Stworzenie landing page'a dla aplikacji.  
* \[ \] Rozpoczęcie budowania społeczności (np. media społecznościowe, Discord).

## **Wdrożenie (DevOps)**

* \[x\] Skonfigurowanie repozytorium Git na GitHubie.  
* \[x\] Skonfigurowanie automatycznych wdrożeń (Auto-Deploy) na Render.com.  
* \[ \] Wdrożenie drugiego serwisu (music-service) na Render.com.  
* \[ \] Wdrożenie n8n jako serwisu w tle na Render.com.  
* \[ \] Skonfigurowanie monitoringu dostępności usług (np. UptimeRobot).

# **3\. Dokumentacja Techniczno-Funkcjonalno-Użytkowa**

## **3.1. Cel i Zakres Aplikacji**

**HardbanRecords Lab** to zintegrowana platforma cyfrowa (SaaS) dla niezależnych twórców (muzyków i autorów), której celem jest uproszczenie i zautomatyzowanie całego cyklu życia produktu cyfrowego – od przygotowania, przez globalną dystrybucję, aż po monetyzację i analizę wyników. Aplikacja eliminuje bariery techniczne i finansowe, dając twórcom pełną kontrolę nad ich własnością intelektualną.

**Zakres MVP** obejmuje dwa główne moduły: **Wydawnictwo Muzyczne** i **Wydawnictwo Cyfrowe (Książki)**, wraz z centralnym systemem zarządzania użytkownikami.

## **3.2. Architektura Systemu**

Platforma wykorzystuje nowoczesną, **odseparowaną architekturę (decoupled)**, składającą się z dwóch głównych komponentów:

* **Frontend:** Aplikacja kliencka zbudowana na **WordPress**, odpowiedzialna za renderowanie interfejsu użytkownika (strona publiczna, panele artystów).  
* **Backend:** Zestaw niezależnych **mikroserwisów** napisanych w **Pythonie (FastAPI)**, które udostępniają logikę biznesową poprzez API REST.

### **Diagram Architektury (Tekstowy)**

  Użytkownik (Przeglądarka)  
       |  
       v  
\+-----------------------------+      \+---------------------------------+  
| Frontend (WordPress)        |      | Backend (Render.com)            |  
| \- Strona publiczna          |      |                                 |  
| \- Panele (Elementor \+ JS)   |-----\>| API Gateway (Routing)           |  
\+-----------------------------+      |      |        |        |        |  
                                     |      v        v        v        v  
                                     | \[auth\]   \[music\]  \[books\]  \[prometheus\]  
                                     |      |        |        |        |  
                                     |      \+--------+--------+--------+  
                                     |               |  
                                     |               v  
                                     |      \+----------------+  
                                     |      | Baza Danych    |  
                                     |      | (PostgreSQL)   |  
                                     |      \+----------------+  
                                     \+---------------------------------+

## **3.3. Wykorzystane Technologie i Biblioteki**

| Warstwa | Technologia/Biblioteka | Cel |
| :---- | :---- | :---- |
| **Backend** | Python 3.11+ | Główny język programowania. |
|  | FastAPI | Nowoczesny framework do budowy API. |
|  | Uvicorn | Serwer ASGI do uruchamiania aplikacji FastAPI. |
|  | SQLAlchemy | ORM do komunikacji z bazą danych. |
|  | Pydantic | Walidacja danych i zarządzanie ustawieniami. |
|  | Passlib, python-jose | Hashowanie haseł i obsługa tokenów JWT. |
| **Frontend** | WordPress | System zarządzania treścią (CMS). |
|  | Elementor | Page builder do tworzenia interfejsów. |
|  | JavaScript (Fetch API) | Komunikacja z backendem. |
| **Baza Danych** | PostgreSQL | Relacyjna baza danych. |
| **Infrastruktura** | Render.com | Platforma chmurowa (PaaS) do hostingu backendu i bazy. |
|  | iFastNet | Hosting współdzielony dla WordPressa. |
|  | Git / GitHub | System kontroli wersji. |

## **3.4. Struktura Bazy Danych**

Baza danych wykorzystuje model relacyjny. Główne tabele w fazie MVP:

* **users**: Przechowuje informacje o użytkownikach (ID, email, hashowane hasło, rola).  
* **music\_releases**: Przechowuje informacje o wydaniach muzycznych (ID, tytuł, artysta, metadane w JSON, status, klucze do plików w chmurze).  
  * **Relacja:** music\_releases.owner\_id \-\> users.id (jeden do wielu).

## **3.5. Główne Funkcje i Moduły**

* **Moduł Uwierzytelniania (auth-service):**  
  * **Rejestracja:** Tworzenie nowego konta użytkownika z hashowaniem hasła.  
  * **Logowanie:** Weryfikacja danych i generowanie tokena dostępowego JWT.  
  * **Autoryzacja:** Mechanizm weryfikacji tokenów JWT w celu ochrony dostępu do zasobów.  
* **Moduł Muzyczny (music-service):**  
  * **Zarządzanie Wydaniami:** Operacje CRUD (Create, Read, Update, Delete) na wydaniach muzycznych.  
  * **Automatyzacja Dystrybucji:** Przygotowanie pakietów dla partnerów (np. Too Lost).

## **3.6. Role Użytkowników i Uprawnienia**

| Rola | Opis | Główne Uprawnienia |
| :---- | :---- | :---- |
| music\_creator | Niezależny muzyk, producent. | Tworzenie i zarządzanie własnymi wydaniami muzycznymi. |
| book\_author | Niezależny autor. | Tworzenie i zarządzanie własnymi projektami książkowymi. |
| admin | Administrator platformy. | Pełen dostęp do zarządzania użytkownikami i treściami. |

## **3.7. Scenariusze Użycia (Use Cases)**

* **Use Case 1: Rejestracja nowego artysty**  
  1. Artysta wchodzi na stronę hardbanrecords-lab.eu.  
  2. Klika "Zarejestruj się".  
  3. Wypełnia formularz (email, hasło).  
  4. Frontend wysyła zapytanie POST /register do backendu.  
  5. Backend weryfikuje dane, tworzy nowego użytkownika w bazie i odsyła potwierdzenie.  
  6. Frontend informuje o sukcesie i przekierowuje do strony logowania.  
* **Use Case 2: Artysta dodaje nowy utwór**  
  1. Artysta loguje się do platformy (otrzymuje token JWT).  
  2. Przechodzi do panelu muzycznego i klika "Dodaj nowy utwór".  
  3. Wypełnia formularz (tytuł, artysta) i wgrywa plik audio.  
  4. Frontend wysyła zapytanie POST /music/ do backendu, dołączając token JWT w nagłówku Authorization.  
  5. Backend weryfikuje token, potwierdza uprawnienia, zapisuje dane w tabeli music\_releases i odsyła dane nowo utworzonego wydania.  
  6. Frontend odświeża listę wydań w panelu.

## **3.8. Interfejsy API**

API jest oparte na REST. Główne endpointy:

* POST /register: Tworzy nowego użytkownika.  
  * Request Body: {"email": "user@example.com", "password": "secret"}  
  * Response (200 OK): {"id": 1, "email": "user@example.com", "role": "book\_author"}  
* POST /login: Loguje użytkownika.  
  * Request Body: username=user@example.com\&password=secret  
  * Response (200 OK): {"access\_token": "...", "token\_type": "bearer"}  
* GET /users/me (Chroniony): Zwraca dane zalogowanego użytkownika.  
  * Headers: Authorization: Bearer \<token\>  
  * Response (200 OK): {"id": 1, "email": "user@example.com", "role": "book\_author"}

## **3.9. Wymagania Niefunkcjonalne**

* **Wydajność:** Czas odpowiedzi API \< 500ms.  
* **Bezpieczeństwo:** Szyfrowanie HTTPS, hashowanie haseł, ochrona przed podstawowymi atakami webowymi.  
* **Skalowalność:** Architektura musi umożliwiać łatwe dodawanie nowych mikroserwisów i skalowanie istniejących.  
* **Niezawodność:** Dostępność na poziomie 99.9%.

## **3.10. Wymagania Sprzętowe i Środowiskowe**

* **Backend:** Środowisko uruchomieniowe Python 3.11+ na platformie PaaS (Render.com). Baza danych PostgreSQL.  
* **Frontend:** Standardowy serwer hostingowy PHP/MySQL (iFastNet).  
* **Użytkownik:** Nowoczesna przeglądarka internetowa.

# **4\. PDR (Preliminary Design Review)**

## **4.1. Wstępna Koncepcja i Architektura**

Koncepcja opiera się na stworzeniu odseparowanej architektury, gdzie frontend (WordPress) jest całkowicie niezależny od backendu (mikroserwisy FastAPI). Pozwala to na maksymalne wykorzystanie darmowych i niskokosztowych usług: istniejący, tani hosting dla WordPressa oraz darmowe plany PaaS (Render.com) dla backendu, który jest bardziej wymagający technologicznie. Taka architektura jest elastyczna i gotowa na przyszłe skalowanie.

## **4.2. Harmonogram Projektu (Kamienie Milowe)**

| Kamień Milowy | Faza | Planowany Termin |
| :---- | :---- | :---- |
| **Fundamenty** | Infrastruktura | ✅ **Zakończono** |
| **Serwis Auth** | Backend | ✅ **Zakończono** |
| **MVP Modułu Muzycznego** | Backend/Frontend | Q4 2025 |
| **MVP Modułu Książkowego** | Backend/Frontend | Q1 2026 |
| **Integracja AI (Prometheus)** | Backend | Q2 2026 |

## **4.3. Główne Ryzyka i Sposoby Ich Mitigacji**

| Ryzyko | Prawdopodobieństwo | Wpływ | Sposób Mitigacji |
| :---- | :---- | :---- | :---- |
| **Brak dostępu do API Too Lost** | Średnie | Wysoki | Równoległe badanie alternatywnych partnerów dystrybucyjnych z API (np. Revelator). |
| **Problemy z wydajnością na darmowych planach** | Wysokie | Średni | Regularne monitorowanie obciążenia. Przygotowanie budżetu na szybkie przejście na płatne, mocniejsze plany (\~$7/miesiąc za usługę na Render). |
| **Złożoność integracji WP-JS-FastAPI** | Średnie | Średni | Budowanie prostych, dobrze udokumentowanych endpointów API. Stworzenie biblioteki reużywalnych funkcji JS po stronie frontendu. |

## **4.4. Analiza Kosztów i Zasobów (Model Niskobudżetowy)**

Projekt w fazie MVP jest realizowany przy **minimalnych kosztach bieżących**.

* **Frontend (WordPress):** **\~150 PLN / rok** (istniejący hosting współdzielony na iFastNet).  
* **Backend (FastAPI):** **$0 / miesiąc**. Wykorzystanie darmowego planu "Web Service" na Render.com.  
* **Baza Danych (PostgreSQL):** **$0 / miesiąc**. Wykorzystanie darmowego planu "PostgreSQL" na Render.com.  
* **Kontrola Wersji (Git):** **$0 / miesiąc**. Prywatne repozytorium na GitHubie.  
* **Narzędzia Deweloperskie:** **$0**. VS Code, Ubuntu (WSL), Postman/REST Client są darmowe.

**Całkowity koszt utrzymania MVP: \~150 PLN rocznie.**

## **4.5. Wstępny Plan Testów**

Testowanie będzie się odbywać na trzech poziomach:

1. **Testy API:** Manualne testowanie każdego endpointu backendu za pomocą narzędzia test.http w VS Code.  
2. **Testy Manualne E2E:** Po zintegrowaniu frontendu, przeprowadzanie pełnych scenariuszy użytkownika (rejestracja \-\> logowanie \-\> dodanie utworu).  
3. **Testy Użyteczności:** Przekazanie wczesnej wersji aplikacji grupie zaufanych artystów w celu zebrania opinii zwrotnej.

## **4.6. Kryteria Akceptacji Produktu (MVP)**

Produkt w wersji MVP zostanie uznany za gotowy, gdy spełni następujące kryteria:

* Użytkownik może pomyślnie założyć konto i zalogować się.  
* Zalogowany użytkownik może uzyskać dostęp do swojego panelu.  
* Użytkownik z rolą music\_creator może dodać nowe wydanie muzyczne (tytuł, artysta), a dane zostaną poprawnie zapisane w bazie danych.  
* Użytkownik może wylogować się z systemu.  
* Całość działa stabilnie w środowisku produkcyjnym na Render.com.

## **4.7. Podsumowanie i Rekomendacje**

Projekt HardbanRecords Lab jest w doskonałej kondycji. Ukończono kluczową, najbardziej ryzykowną fazę budowy fundamentów. Architektura jest solidna, a stos technologiczny nowoczesny i niskokosztowy. Zidentyfikowane ryzyka są zarządzalne.

**Rekomenduje się natychmiastowe przejście do kolejnej fazy projektu**, której priorytetem powinno być ukończenie serwisu auth-service i rozpoczęcie prac nad modułem muzycznym. Projekt jest w pełni gotowy do dalszego rozwoju.