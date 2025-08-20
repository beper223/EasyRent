Примеры использования в запросах
Поиск по ключевым словам:

bash
Копировать код
GET /api/v1/listings/?search=balcony
Фильтрация по цене и комнатам:

bash
Копировать код
GET /api/v1/listings/?min_price=1000&max_price=2000&min_rooms=1&max_rooms=3
Фильтрация по локации и типу жилья:

bash
Копировать код
GET /api/v1/listings/?location=Berlin&housing_type=apartment
Сортировка по цене по возрастанию:

bash
Копировать код
GET /api/v1/listings/?ordering=price
Сортировка по дате добавления (сначала новые):

bash
Копировать код
GET /api/v1/listings/?ordering=-created_at