# Система аутентификации и авторизации

Backend-приложение с собственной системой аутентификации и авторизации на Django REST Framework.

## Архитектура

### Модули приложения
- **app_auth** - JWT аутентификация (вход/выход)
- **users** - управление пользователями
- **business_entities** - демонстрационные бизнес-сущности

### База данных

#### Пользователи
- **ProjectUser** - пользователи системы
  - email, имя, фамилия
  - роль (user/admin/superuser)
  - мягкое удаление (is_active)

#### Бизнес-сущности
- **Task** - задачи (создатель, исполнитель, статус)
- **News** - новости (создатель, заголовок, содержание)

### Система прав доступа

#### Роли пользователей
- **user** - обычный пользователь
- **admin** - администратор  
- **superuser** - суперпользователь

#### Правила доступа
- Все аутентифицированные пользователи могут просматривать и создавать объекты
- Изменять и удалять можно только собственные объекты или объекты на которые ты назначен исполнителем (кроме администраторов)
- Администраторы имеют полный доступ ко всем операциям

## API Endpoints

### Аутентификация

**Вход в систему**
```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Выход из системы**
```http
POST /api/auth/logout/
Authorization: Bearer <jwt_token>
```

### Пользователи

**Регистрация**
```http
POST /api/users/register/
Content-Type: application/json

{
  "email": "newuser@example.com",
  "password": "password123",
  "password_confirm": "password123",
  "first_name": "Иван",
  "last_name": "Иванов"
}
```

**Профиль пользователя**
```http
GET /api/users/profile/
Authorization: Bearer <jwt_token>
```

**Обновление профиля**
```http
PUT /api/users/profile/
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "first_name": "Новое имя",
  "last_name": "Новая фамилия"
}
```

**Удаление аккаунта**
```http
DELETE /api/users/delete-account/
Authorization: Bearer <jwt_token>
```

### Бизнес-сущности

**Задачи**

Получить список задач:
```http
GET /api/business/tasks/
Authorization: Bearer <jwt_token>
```

Создать задачу:
```http
POST /api/business/tasks/
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "Новая задача",
  "description": "Описание задачи",
  "assigned_to": 2 (id пользователя на котором закреалена задача)
}
```

Управление задачей:
```http
GET/PUT/DELETE /api/tasks/1/
Authorization: Bearer <jwt_token>
```

**Новости**

Получить список новостей:
```http
GET /api/news/
Authorization: Bearer <jwt_token>
```

Создать новость:
```http
POST /api/news/
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "Заголовок новости",
  "content": "Текст новости"
}
```

Управление новостью:
```http
GET/PUT/DELETE /api/business/news/1/
Authorization: Bearer <jwt_token>
```

## Технологии
- Django + Django REST Framework
- PostgreSQL
- JWT токены
- Кастомная система permissions
- Docker

## Запуск проекта

```bash
# Сборка и запуск
docker-compose up --build

# Приложение будет доступно по http://localhost:8000
```
