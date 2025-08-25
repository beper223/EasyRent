# EasyRent API-Dokumentation

## Inhaltsverzeichnis
1. [Authentifizierung und Benutzer](#1-authentifizierung-und-benutzer-apiv1users)
2. [Wohnungsangebote](#2-wohnungsangebote-apiv1listings)
3. [Buchungen](#3-buchungen-apiv1bookings)
4. [API-Dokumentation](#4-api-dokumentation)

## 1. Authentifizierung und Benutzer (`/api/v1/users/`)

### Benutzerverwaltung
- **`POST /api/v1/users/`** - Neuen Benutzer registrieren
  - **Zugriff:** Anonyme Benutzer
  - **Anfragekörper:** Neue Benutzerdaten
  - **Antwort:** Registrierte Benutzerdaten

- **`GET /api/v1/users/`** - Alle Benutzer auflisten
  - **Zugriff:** Nur Administratoren
  - **Antwort:** Liste der Benutzer

- **`GET /api/v1/users/{id}/`** - Benutzerdetails abrufen
  - **Zugriff:** Authentifizierte Benutzer (eigene Daten) oder Administratoren
  - **Antwort:** Benutzerdetails

- **`PUT/PATCH /api/v1/users/{id}/`** - Benutzerdaten aktualisieren
  - **Zugriff:** Kontoinhaber oder Administrator
  - **Anfragekörper:** Aktualisierte Daten
  - **Antwort:** Aktualisierte Benutzerdaten

- **`DELETE /api/v1/users/{id}/`** - Benutzer löschen
  - **Zugriff:** Kontoinhaber oder Administrator

### Authentifizierung
- **`POST /api/v1/users/login/`** - Anmelden
  - **Zugriff:** Alle Benutzer
  - **Anfragekörper:** Benutzername und Passwort
  - **Antwort:** JWT Zugriffs- und Aktualisierungstoken

- **`POST /api/v1/users/logout/`** - Abmelden
  - **Zugriff:** Authentifizierte Benutzer
  - **Aktion:** Macht das Token ungültig

### Profil
- **`GET /api/v1/users/my`** - Aktuelle Benutzerinformationen
  - **Zugriff:** Authentifizierte Benutzer
  - **Antwort:** Aktuelle Benutzerdaten

- **`POST /api/v1/users/change-password/`** - Passwort ändern
  - **Zugriff:** Authentifizierte Benutzer
  - **Anfragekörper:** Aktuelles und neues Passwort

## 2. Wohnungsangebote (`/api/v1/listings/`)

### Grundlegende Operationen
- **`GET /api/v1/listings/`** - Alle Angebote anzeigen
  - **Zugriff:** Alle Benutzer
  - **Filter:**
    - `min_price`, `max_price` - Preisbereich
    - `min_rooms`, `max_rooms` - Anzahl der Zimmer
    - `location` - Standortsuche
    - `housing_type` - Wohnungstyp
  - **Sortierung:** Nach Preis (`price`) und Erstellungsdatum (`created_at`)
  - **Antwort:** Liste aktiver Angebote

- **`POST /api/v1/listings/`** - Neues Angebot erstellen
  - **Zugriff:** Authentifizierte Vermieter
  - **Anfragekörper:** Angebotsdaten
  - **Antwort:** Erstelltes Angebot

- **`GET /api/v1/listings/{id}/`** - Angebotsdetails anzeigen
  - **Zugriff:** Alle Benutzer
  - **Antwort:** Angebotsdetails mit Bewertungen

- **`PUT/PATCH /api/v1/listings/{id}/`** - Angebot aktualisieren
  - **Zugriff:** Angebotsersteller oder Administrator
  - **Anfragekörper:** Aktualisierte Daten
  - **Antwort:** Aktualisiertes Angebot

- **`DELETE /api/v1/listings/{id}/`** - Angebot löschen
  - **Zugriff:** Angebotsersteller oder Administrator

### Zusätzliche Aktionen
- **`GET /api/v1/listings/my_listings/`** - Meine Angebote
  - **Zugriff:** Authentifizierte Vermieter
  - **Antwort:** Angebote des aktuellen Benutzers

- **`POST /api/v1/listings/{id}/add_review/`** - Bewertung hinzufügen
  - **Zugriff:** Authentifizierte Mieter
  - **Anfragekörper:** Bewertungstext und Bewertung
  - **Antwort:** Erstellte Bewertung

## 3. Buchungen (`/api/v1/bookings/`)

- **`GET /api/v1/bookings/`** - Buchungen anzeigen
  - **Zugriff:** Authentifizierte Benutzer
  - **Antwort:**
    - Mieter: ihre eigenen Buchungen
    - Vermieter: Buchungen für ihre Angebote
    - Administratoren: alle Buchungen

- **`POST /api/v1/bookings/`** - Buchung erstellen
  - **Zugriff:** Authentifizierte Mieter
  - **Anfragekörper:** Angebots-ID, Buchungsdaten
  - **Antwort:** Erstellte Buchung

- **`GET /api/v1/bookings/{id}/`** - Buchungsdetails anzeigen
  - **Zugriff:**
    - Mieter (eigene Buchung)
    - Vermieter (Buchung für ihr Angebot)
    - Administrator

- **`PUT/PATCH /api/v1/bookings/{id}/`** - Buchung aktualisieren
  - **Zugriff:**
    - Mieter (eigene Buchung)
    - Administrator
  - **Einschränkungen:** Kann nur innerhalb bestimmter Fristen aktualisiert werden

- **`DELETE /api/v1/bookings/{id}/`** - Buchung stornieren
  - **Zugriff:**
    - Mieter (eigene Buchung)
    - Administrator
  - **Einschränkungen:** Kann nur bis zu einem bestimmten Datum storniert werden

## 4. API-Dokumentation

- **`GET /api/schema/`** - OpenAPI-Schema abrufen
- **`GET /api/schema/swagger/`** - Swagger-UI-Dokumentation

## Allgemeine Hinweise

1. **Authentifizierung:** Erforderlich für alle Endpunkte außer:
   - Benutzerregistrierung
   - Anmeldung
   - Anzeige von Angeboten
   - Anzeige von Angebotsdetails

2. **Benutzerrollen:**
   - **Mieter** - können Wohnungen buchen und Bewertungen abgeben
   - **Vermieter** - können Angebote erstellen und verwalten
   - **Administratoren** - haben vollen Zugriff auf alle Funktionen

3. **Einschränkungen:**
   - Buchungen können nur bis zu einem bestimmten Datum storniert werden
   - Nur Vermieter können Angebote erstellen
   - Nur Mieter, die eine Wohnung gebucht haben, können diese bewerten
