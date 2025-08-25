# EasyRent - Платформа аренды жилья

## Содержание
- [Описание проекта](#описание-проекта)
- [Возможности](#возможности)
- [Установка](#установка)
- [Использование](#использование)
- [Документация API](#документация-api)
- [Лицензия](#лицензия)

## Описание проекта
EasyRent - это современная веб-платформа для аренды жилья, которая соединяет арендодателей и арендаторов. Проект разработан с использованием Django REST Framework и предоставляет удобный API для управления объявлениями, бронированиями и пользователями.

## Возможности
- 📝 Создание и управление объявлениями об аренде
- 📅 Бронирование жилья на выбранные даты
- 🔐 Аутентификация и авторизация пользователей
- 🔍 Расширенный поиск с фильтрацией
- ⭐ Система отзывов и рейтингов
- 📱 Адаптивный интерфейс

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/EasyRent.git
cd EasyRent
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
.\venv\Scripts\activate  # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте переменные окружения в файле `.env`:
```
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. Примените миграции:
```bash
python manage.py migrate
```

6. Запустите сервер:
```bash
python manage.py runserver
```

## Использование

### Примеры запросов

#### Поиск жилья
```bash
# Поиск по ключевым словам
GET /api/v1/listings/?search=balcony

# Фильтрация по цене и количеству комнат
GET /api/v1/listings/?min_price=1000&max_price=2000&min_rooms=1&max_rooms=3

# Фильтрация по местоположению и типу жилья
GET /api/v1/listings/?location=Berlin&housing_type=apartment

# Сортировка результатов
GET /api/v1/listings/?ordering=price          # по цене (возрастание)
GET /api/v1/listings/?ordering=-created_at    # по дате (сначала новые)
```

## Документация API

Полная документация по API доступна на следующих языках:

- [English API Documentation](API_DOCUMENTATION.md)
- [Deutsche API-Dokumentation](API_DOKUMENTATION_DE.md)
- [Документация API на русском](API_DOCUMENTATION_RU.md)

## Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для получения дополнительной информации.

---

# EasyRent - Apartment Rental Platform

## Table of Contents
- [Project Description](#project-description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [License](#license)

## Project Description
EasyRent is a modern web platform for apartment rentals that connects landlords and tenants. The project is built with Django REST Framework and provides a convenient API for managing listings, bookings, and users.

## Features
- 📝 Create and manage rental listings
- 📅 Book accommodations for selected dates
- 🔐 User authentication and authorization
- 🔍 Advanced search with filtering
- ⭐ Review and rating system
- 📱 Responsive interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/EasyRent.git
cd EasyRent
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables in `.env` file:
```
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. Apply migrations:
```bash
python manage.py migrate
```

6. Run the server:
```bash
python manage.py runserver
```

## Usage

### Example Requests

#### Search for Listings
```bash
# Search by keywords
GET /api/v1/listings/?search=balcony

# Filter by price and number of rooms
GET /api/v1/listings/?min_price=1000&max_price=2000&min_rooms=1&max_rooms=3

# Filter by location and housing type
GET /api/v1/listings/?location=Berlin&housing_type=apartment

# Sort results
GET /api/v1/listings/?ordering=price          # by price (ascending)
GET /api/v1/listings/?ordering=-created_at    # by date (newest first)
```

## API Documentation

Full API documentation is available in the following languages:

- [English API Documentation](API_DOCUMENTATION.md)
- [Deutsche API-Dokumentation](API_DOKUMENTATION_DE.md)
- [Документация API на русском](API_DOCUMENTATION_RU.md)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

---

# EasyRent - Wohnungsvermietungsplattform

## Inhaltsverzeichnis
- [Projektbeschreibung](#projektbeschreibung)
- [Funktionen](#funktionen)
- [Installation](#installation-1)
- [Verwendung](#verwendung)
- [API-Dokumentation](#api-dokumentation-1)
- [Lizenz](#lizenz)

## Projektbeschreibung
EasyRent ist eine moderne Webplattform zur Wohnungsvermietung, die Vermieter und Mieter verbindet. Das Projekt wurde mit Django REST Framework entwickelt und bietet eine benutzerfreundliche API zur Verwaltung von Anzeigen, Buchungen und Benutzern.

## Funktionen
- 📝 Erstellung und Verwaltung von Mietangeboten
- 📅 Buchung von Unterkünften für ausgewählte Zeiträume
- 🔐 Benutzerauthentifizierung und -autorisierung
- 🔍 Erweiterte Suche mit Filtern
- ⭐ Bewertungs- und Rezensionssystem
- 📱 Reaktionsfähige Benutzeroberfläche

## Installation

1. Repository klonen:
```bash
git clone https://github.com/yourusername/EasyRent.git
cd EasyRent
```

2. Virtuelle Umgebung erstellen und aktivieren:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
.\venv\Scripts\activate  # Windows
```

3. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

4. Umgebungsvariablen in der `.env`-Datei konfigurieren:
```
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. Migrationen anwenden:
```bash
python manage.py migrate
```

6. Server starten:
```bash
python manage.py runserver
```

## Verwendung

### Beispielanfragen

#### Nach Wohnungen suchen
```bash
# Nach Stichwörtern suchen
GET /api/v1/listings/?search=Balkon

# Nach Preis und Zimmerzahl filtern
GET /api/v1/listings/?min_price=1000&max_price=2000&min_rooms=1&max_rooms=3

# Nach Standort und Wohnungstyp filtern
GET /api/v1/listings/?location=Berlin&housing_type=apartment

# Ergebnisse sortieren
GET /api/v1/listings/?ordering=price          # nach Preis (aufsteigend)
GET /api/v1/listings/?ordering=-created_at    # nach Datum (neueste zuerst)
```

## API-Dokumentation

Vollständige API-Dokumentation in folgenden Sprachen:

- [English API Documentation](API_DOCUMENTATION.md)
- [Deutsche API-Dokumentation](API_DOKUMENTATION_DE.md)
- [Документация API на русском](API_DOCUMENTATION_RU.md)

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Weitere Informationen finden Sie in der [LICENSE](LICENSE)-Datei.