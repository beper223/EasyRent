# EasyRent - Платформа аренды жилья

## Содержание
- [О проекте](#о-проекте)
- [Функциональность](#функциональность)
- [Технические требования](#технические-требования)
- [Роли пользователей](#роли-пользователей)
- [Установка](#установка)
- [Использование](#использование)
- [Документация API](#документация-api)
- [Лицензия](#лицензия)

## О проекте
EasyRent - это современная веб-платформа для аренды жилья, которая соединяет арендодателей и арендаторов. Проект разработан с использованием Django REST Framework и предоставляет удобный API для управления объявлениями, бронированиями и пользователями.

## Функциональность

### 1. Управление объявлениями
- Создание, редактирование и удаление объявлений
- Управление статусом объявления (активно/неактивно)
- Детальная информация о недвижимости:
  - Заголовок и описание
  - Местоположение
  - Цена
  - Количество комнат
  - Тип жилья

### 2. Поиск и фильтрация
- Полнотекстовый поиск по заголовкам и описаниям
- Фильтрация по:
  - Ценовому диапазону
  - Местоположению (город/район)
  - Количеству комнат
  - Типу жилья
- Сортировка по цене и дате добавления

### 3. Система бронирования
- Создание и отмена бронирований
- Календарь доступности
- Подтверждение/отклонение бронирований
- История бронирований

### 4. Рейтинги и отзывы
- Оставление отзывов и оценок
- Просмотр отзывов по объявлениям
- Рейтинг арендодателей

## Технические требования

### Backend
- **Язык программирования**: Python 3.12+
- **Веб-фреймворк**: Django 5.2.5
- **API**: Django REST Framework 3.16.0
- **База данных**: MySQL (mysqlclient 2.2.7)
- **Аутентификация**: JWT (djangorestframework-simplejwt 5.5.1)
- **Документация API**: drf-spectacular (OpenAPI 3.0)
- **Фильтрация**: django-filter 25.1
- **Управление настройками**: django-environ 0.12.0
- **Кэширование**: Встроенное кэширование Django

### API
- **Архитектура**: RESTful
- **Документирование**: Автоматическая генерация через drf-spectacular
- **Пагинация**: Встроенная в DRF
- **Фильтрация**: Поддержка сложных фильтров через django-filter
- **Аутентификация**: JWT с поддержкой обновления токенов
- **Версионирование**: Встроенное в URL (v1/)
- **Формат данных**: JSON

## Роли пользователей

### Арендатор
- Просмотр и поиск объявлений
- Бронирование жилья
- Оставление отзывов
- Управление своими бронированиями

### Арендодатель
- Всё, что может арендатор
- Создание и управление объявлениями
- Подтверждение бронирований
- Просмотр статистики по объявлениям

### Администратор
- Полный доступ к системе
- Управление пользователями
- Модерация контента
- Аналитика и отчеты

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/EasyRent.git
cd EasyRent
```

2. Убедитесь, что у вас установлен [uv](https://github.com/astral-sh/uv) - современный и быстрый менеджер зависимостей Python

3. Установите зависимости:
```bash
uv sync
```

4. Настройте переменные окружения в файле `.env`:
```
# Базовые настройки Django
SECRET_KEY=ваш_секретный_ключ_здесь
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# Выбор базы данных (True - удалённая, False - локальная)
USE_REMOTE_DB=False

# Настройки удалённой базы данных
DB_ENGINE=django.db.backends.mysql
DB_NAME=имя_удаленной_бд
DB_HOST=хост_удаленной_бд
DB_PORT=3306
DB_USER=пользователь_бд
DB_PASSWORD=пароль_бд

# Настройки локальной базы данных
LOCAL_DB_ENGINE=django.db.backends.mysql
LOCAL_DB_NAME=имя_локальной_бд
LOCAL_DB_HOST=localhost
LOCAL_DB_PORT=3306
LOCAL_DB_USER=пользователь_бд
LOCAL_DB_PASSWORD=пароль_бд

# API ключ Google (опционально)
GOOGLE_API_KEY=ваш_google_api_ключ
```

5. Примените миграции:
```bash
python manage.py migrate
```

6. Создайте суперпользователя (опционально):
```bash
python manage.py createsuperuser
```

7. Запустите сервер:
```bash
python manage.py runserver
```

## Использование

### Примеры запросов

#### Поиск жилья
```bash
# Поиск по ключевым словам
GET /api/v1/listings/?search=балкон

# Фильтрация по цене и количеству комнат
GET /api/v1/listings/?min_price=1000&max_price=2000&min_rooms=1&max_rooms=3

# Фильтрация по местоположению и типу жилья
GET /api/v1/listings/?location=Берлин&housing_type=apartment

# Сортировка результатов
GET /api/v1/listings/?ordering=price          # по цене (возрастание)
GET /api/v1/listings/?ordering=-created_at    # по дате (сначала новые)
```

## Документация API

Полная документация по API доступна после запуска сервера по адресу:
- `/api/schema/swagger/` - Swagger UI
- `/api/schema/redoc/` - ReDoc

Также доступна документация на следующих языках:
- [English API Documentation](API_DOCUMENTATION.md)
- [Deutsche API-Dokumentation](API_DOKUMENTATION_DE.md)
- [Документация API на русском](API_DOCUMENTATION_RU.md)

## Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для получения дополнительной информации.

---

# EasyRent - Apartment Rental Platform

## Table of Contents
- [About the Project](#about-the-project)
- [Features](#features)
- [Technical Requirements](#technical-requirements)
- [User Roles](#user-roles)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [License](#license)

## About the Project
EasyRent is a modern web platform for apartment rentals that connects landlords and tenants. The project is built with Django REST Framework and provides a convenient API for managing listings, bookings, and users.

## Features

### 1. Listing Management
- Create, edit, and delete property listings
- Toggle listing status (active/inactive)
- Detailed property information:
  - Title and description
  - Location
  - Price
  - Number of rooms
  - Property type

### 2. Search and Filtering
- Full-text search in titles and descriptions
- Filter by:
  - Price range
  - Location (city/district)
  - Number of rooms
  - Property type
- Sort by price and listing date

### 3. Booking System
- Create and cancel bookings
- Availability calendar
- Booking confirmation/rejection
- Booking history

### 4. Ratings and Reviews
- Leave reviews and ratings
- View listing reviews
- Landlord ratings

## Technical Requirements

### Backend
- **Programming Language**: Python 3.12+
- **Web Framework**: Django 5.2.5
- **API**: Django REST Framework 3.16.0
- **Database**: MySQL (mysqlclient 2.2.7)
- **Authentication**: JWT (djangorestframework-simplejwt 5.5.1)
- **API Documentation**: drf-spectacular (OpenAPI 3.0)
- **Filtering**: django-filter 25.1
- **Settings Management**: django-environ 0.12.0
- **Caching**: Built-in Django caching

### API
- **Architecture**: RESTful
- **Documentation**: Auto-generated via drf-spectacular
- **Pagination**: Built-in DRF pagination
- **Filtering**: Advanced filtering via django-filter
- **Authentication**: JWT with token refresh
- **Versioning**: URL-based (v1/)
- **Data Format**: JSON

## User Roles

### Tenant
- Browse and search listings
- Book properties
- Leave reviews
- Manage own bookings

### Landlord
- All tenant capabilities
- Create and manage listings
- Confirm/reject bookings
- View listing statistics

### Administrator
- Full system access
- User management
- Content moderation
- Analytics and reporting

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/EasyRent.git
cd EasyRent
```

2. Make sure you have [uv](https://github.com/astral-sh/uv) installed - a modern and fast Python package manager

3. Install dependencies:
```bash
uv sync
```

4. Configure environment variables in `.env` file:
```
# Django basic settings
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# Database selection (True - remote, False - local)
USE_REMOTE_DB=False

# Remote database settings
DB_ENGINE=django.db.backends.mysql
DB_NAME=remote_db_name
DB_HOST=remote_db_host
DB_PORT=3306
DB_USER=db_user
DB_PASSWORD=db_password

# Local database settings
LOCAL_DB_ENGINE=django.db.backends.mysql
LOCAL_DB_NAME=local_db_name
LOCAL_DB_HOST=localhost
LOCAL_DB_PORT=3306
LOCAL_DB_USER=db_user
LOCAL_DB_PASSWORD=db_password

# Google API key (optional)
GOOGLE_API_KEY=your_google_api_key
```

5. Apply migrations:
```bash
python manage.py migrate
```

6. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

7. Run the server:
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

# Filter by location and property type
GET /api/v1/listings/?location=Berlin&housing_type=apartment

# Sort results
GET /api/v1/listings/?ordering=price          # by price (ascending)
GET /api/v1/listings/?ordering=-created_at    # by date (newest first)
```

## API Documentation

Full API documentation is available after starting the server at:
- `/api/schema/swagger/` - Swagger UI
- `/api/schema/redoc/` - ReDoc

Documentation is also available in the following languages:
- [English API Documentation](API_DOCUMENTATION.md)
- [Deutsche API-Dokumentation](API_DOKUMENTATION_DE.md)
- [Документация API на русском](API_DOCUMENTATION_RU.md)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

# EasyRent - Wohnungsvermietungsplattform

## Inhaltsverzeichnis
- [Über das Projekt](#über-das-projekt)
- [Funktionen](#funktionen)
- [Technische Anforderungen](#technische-anforderungen)
- [Benutzerrollen](#benutzerrollen)
- [Installation](#installation-1)
- [Verwendung](#verwendung)
- [API-Dokumentation](#api-dokumentation)
- [Lizenz](#lizenz)

## Über das Projekt
EasyRent ist eine moderne Webplattform zur Wohnungsvermittlung, die Vermieter und Mieter verbindet. Das Projekt wurde mit Django REST Framework entwickelt und bietet eine praktische API zur Verwaltung von Anzeigen, Buchungen und Benutzern.

## Funktionen

### 1. Anzeigenverwaltung
- Erstellen, Bearbeiten und Löschen von Immobilienanzeigen
- Anzeigenstatus umschalten (aktiv/inaktiv)
- Detaillierte Immobilieninformationen:
  - Titel und Beschreibung
  - Standort
  - Preis
  - Anzahl der Zimmer
  - Immobilientyp

### 2. Suche und Filterung
- Volltextsuche in Titeln und Beschreibungen
- Filtern nach:
  - Preisbereich
  - Standort (Stadt/Bezirk)
  - Anzahl der Zimmer
  - Immobilientyp
- Sortieren nach Preis und Anzeigedatum

### 3. Buchungssystem
- Buchungen erstellen und stornieren
- Verfügbarkeitskalender
- Buchungsbestätigung/-ablehnung
- Buchungsverlauf

### 4. Bewertungen und Rezensionen
- Bewertungen und Sterne vergeben
- Anzeigenbewertungen anzeigen
- Vermieterbewertungen

## Technische Anforderungen

### Backend
- **Programmiersprache**: Python 3.12+
- **Web-Framework**: Django 5.2.5
- **API**: Django REST Framework 3.16.0
- **Datenbank**: MySQL (mysqlclient 2.2.7)
- **Authentifizierung**: JWT (djangorestframework-simplejwt 5.5.1)
- **API-Dokumentation**: drf-spectacular (OpenAPI 3.0)
- **Filterung**: django-filter 25.1
- **Einstellungsverwaltung**: django-environ 0.12.0
- **Caching**: Integriertes Django-Caching

### API
- **Architektur**: RESTful
- **Dokumentation**: Automatisch generiert mit drf-spectacular
- **Paginierung**: Integrierte DRF-Paginierung
- **Filterung**: Erweiterte Filterung mit django-filter
- **Authentifizierung**: JWT mit Token-Aktualisierung
- **Versionierung**: URL-basiert (v1/)
- **Datenformat**: JSON

## Benutzerrollen

### Mieter
- Anzeigen durchsuchen und suchen
- Unterkünfte buchen
- Bewertungen hinterlassen
- Eigene Buchungen verwalten

### Vermieter
- Alle Funktionen eines Mieters
- Anzeigen erstellen und verwalten
- Buchungen bestätigen/ablehnen
- Anzeigenstatistiken einsehen

### Administrator
- Vollständiger Systemzugriff
- Benutzerverwaltung
- Inhaltsmoderation
- Analyse und Berichte

## Installation

1. Repository klonen:
```bash
git clone https://github.com/yourusername/EasyRent.git
cd EasyRent
```

2. Stellen Sie sicher, dass [uv](https://github.com/astral-sh/uv) installiert ist - ein moderner und schneller Python-Paketmanager

3. Abhängigkeiten installieren:
```bash
uv sync
```

4. Umgebungsvariablen in der `.env`-Datei konfigurieren:
```
# Django-Grundeinstellungen
SECRET_KEY=Ihr_geheimer_Schluessel_hier
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# Datenbankauswahl (True - entfernt, False - lokal)
USE_REMOTE_DB=False

# Einstellungen für entfernte Datenbank
DB_ENGINE=django.db.backends.mysql
DB_NAME=entfernte_datenbank_name
DB_HOST=entfernter_datenbank_host
DB_PORT=3306
DB_USER=datenbank_benutzer
DB_PASSWORD=datenbank_passwort

# Einstellungen für lokale Datenbank
LOCAL_DB_ENGINE=django.db.backends.mysql
LOCAL_DB_NAME=lokale_datenbank_name
LOCAL_DB_HOST=localhost
LOCAL_DB_PORT=3306
LOCAL_DB_USER=datenbank_benutzer
LOCAL_DB_PASSWORD=datenbank_passwort

# Google API-Schlüssel (optional)
GOOGLE_API_KEY=Ihr_Google_API_Schluessel
```

5. Migrationen anwenden:
```bash
python manage.py migrate
```

6. Superuser erstellen (optional):
```bash
python manage.py createsuperuser
```

7. Server starten:
```bash
python manage.py runserver
```

## Verwendung

### Beispielanfragen

#### Nach Anzeigen suchen
```bash
# Nach Stichwörtern suchen
GET /api/v1/listings/?search=Balkon

# Nach Preis und Zimmeranzahl filtern
GET /api/v1/listings/?min_price=1000&max_price=2000&min_rooms=1&max_rooms=3

# Nach Standort und Immobilientyp filtern
GET /api/v1/listings/?location=Berlin&housing_type=apartment

# Ergebnisse sortieren
GET /api/v1/listings/?ordering=price          # nach Preis (aufsteigend)
GET /api/v1/listings/?ordering=-created_at    # nach Datum (neueste zuerst)
```

## API-Dokumentation

Die vollständige API-Dokumentation ist nach dem Start des Servers verfügbar unter:
- `/api/schema/swagger/` - Swagger UI
- `/api/schema/redoc/` - ReDoc

Die Dokumentation ist auch in folgenden Sprachen verfügbar:
- [English API Documentation](API_DOCUMENTATION.md)
- [Deutsche API-Dokumentation](API_DOKUMENTATION_DE.md)
- [Документация API на русском](API_DOCUMENTATION_RU.md)

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Weitere Informationen finden Sie in der [LICENSE](LICENSE)-Datei.
