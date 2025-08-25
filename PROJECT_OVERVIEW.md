# Концепция проекта EasyRent

## Оглавление
- [Цель проекта](#цель-проекта)
- [Основной функционал](#основной-функционал)
- [Технические требования](#технические-требования)
- [Роли пользователей](#роли-пользователей)
- [Дополнительные функции](#дополнительные-функции)

## Цель проекта
Создать полнофункциональное back-end приложение для системы аренды жилья с возможностью управления объявлениями, бронированиями и отзывами.

## Основной функционал

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
  - Местоположению (город/район в Германии)
  - Количеству комнат
  - Типу жилья
- Сортировка по цене и дате добавления

### 3. Пользовательская система
- Регистрация и аутентификация
- Разделение прав доступа:
  - Арендаторы
  - Арендодатели
  - Администраторы
- Управление профилем

### 4. Система бронирования
- Создание и отмена бронирований
- Календарь доступности
- Подтверждение/отклонение бронирований арендодателем
- История бронирований

### 5. Рейтинги и отзывы
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

## Дополнительные функции

### Аналитика
- Популярные запросы поиска
- Статистика просмотров объявлений
- Рейтинги и отзывы


---

# EasyRent Project Concept

## Table of Contents
- [Project Goal](#project-goal)
- [Core Functionality](#core-functionality)
- [Technical Requirements](#technical-requirements)
- [User Roles](#user-roles)
- [Additional Features](#additional-features)

## Project Goal
To develop a full-featured back-end application for a property rental system with capabilities for managing listings, bookings, and reviews.

## Core Functionality

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
  - Location (city/district in Germany)
  - Number of rooms
  - Property type
- Sort by price and listing date

### 3. User System
- Registration and authentication
- Role-based access control:
  - Tenants
  - Landlords
  - Administrators
- Profile management

### 4. Booking System
- Create and cancel bookings
- Availability calendar
- Booking confirmation/rejection by landlords
- Booking history

### 5. Ratings and Reviews
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

## Additional Features

### Analytics
- Popular search queries
- Listing view statistics
- Ratings and reviews analysis


---

# EasyRent Projektkonzept

## Inhaltsverzeichnis
- [Projektziel](#projektziel)
- [Hauptfunktionen](#hauptfunktionen)
- [Technische Anforderungen](#technische-anforderungen)
- [Benutzerrollen](#benutzerrollen)
- [Zusätzliche Funktionen](#zusätzliche-funktionen)

## Projektziel
Entwicklung einer vollständigen Backend-Anwendung für ein Immobilienvermietungssystem mit Funktionen zur Verwaltung von Anzeigen, Buchungen und Bewertungen.

## Hauptfunktionen

### 1. Anzeigenverwaltung
- Erstellen, Bearbeiten und Löschen von Anzeigen
- Anzeigenstatus umschalten (aktiv/inaktiv)
- Detaillierte Immobilieninformationen:
  - Titel und Beschreibung
  - Standort
  - Preis
  - Anzahl der Zimmer
  - Immobilientyp

### 2. Suche und Filterung
- Volltextsuche in Titeln und Beschreibungen
- Filtermöglichkeiten nach:
  - Preisbereich
  - Standort (Stadt/Bezirk in Deutschland)
  - Zimmeranzahl
  - Immobilientyp
- Sortierung nach Preis und Erstellungsdatum

### 3. Benutzersystem
- Registrierung und Authentifizierung
- Rollenbasierte Zugriffssteuerung:
  - Mieter
  - Vermieter
  - Administratoren
- Profilverwaltung

### 4. Buchungssystem
- Erstellen und Stornieren von Buchungen
- Verfügbarkeitskalender
- Buchungsbestätigung/-ablehnung durch Vermieter
- Buchungsverlauf

### 5. Bewertungen und Rezensionen
- Bewertungen und Sterne vergeben
- Anzeigenbewertungen einsehen
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
- **Konfigurationsverwaltung**: django-environ 0.12.0
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
- Analysen und Berichte

## Zusätzliche Funktionen

### Analysen
- Beliebte Suchanfragen
- Anzeigenaufrufstatistiken
- Bewertungsanalysen

