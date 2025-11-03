# Система аутентификации и авторизации

Backend-приложение с собственной системой аутентификации и авторизации на Django REST Framework.

Тестовое задание для отработки работы с JWT-токенами. Реализована кастомная система безопасности,с минимальным использованием встроенных решений Django "из коробки". База данных - PosttgrSQL. Все приложение упаковано в docker контейнеры.
Реализованы кастомные пермишены. Для тестирования пермишенов созданы бизнес-сущности.

## Что можно сделать далее
Чтобы было проще разобраться, я решил сделать только access токен. Можно добавить refresh токены для обновления access токенов без повторного логина.
На данном этапе не работает Django admin панель - можно ей заняться для удобства управления данными.
Также можно добавить восстановление пароля по email, ограничение количества запросов и автоматическую генерацию документации API.
Проект готов к использованию как основа для более сложных систем безопасности.
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

#### Permission классы
- **IsAuthenticated** - только аутентифицированные пользователи
- **IsOwnerOrAdmin** - владелец объекта или админ
- **IsAssignerOrAdmin** - исполнитель задачи или админ  
- **IsOwnerOrAssignerOrAdmin** - владелец, исполнитель или админ
- **IsOwnerOrAdminOrReadOnly** - чтение: все, изменение: владелец или админ
- **IsAdmin** - только администраторы

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
GET /api/tasks/
Authorization: Bearer <jwt_token>
```

Создать задачу:
```http
POST /api/tasks/
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "Новая задача",
  "description": "Описание задачи",
  "assigned_to": 2
}
```

Управление задачей:
```http
GET/PUT/DELETE /api/tasks/1/
Authorization: Bearer <jwt_token>
```

**Демонстрация permissions для задач:**
```http
GET /api/tasks/owner-or-admin/1/ - только владелец или админ
GET /apitasks/assigner-or-admin/1/ - только исполнитель или админ  
GET /api/tasks/admin-only/ - только администраторы
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
# Контейнеры с логами в терминале
или
docker-compose up --build -d 
# Контейнеры в фоновом режиме

# Приложение будет доступно по http://localhost:8000
```
# Создание суперпользователя (после запуска)
```bash
docker exec -it auth_system_project-backend-1 python manage.py createsuperuser
```

## Демонстрация системы прав

### Сценарии тестирования:

1. **Без аутентификации** - все запросы возвращают 401
2. **Обычный пользователь** - может создавать и просматривать, но редактировать только свои объекты
3. **Администратор** - имеет полный доступ ко всем операциям

### Примеры проверки permissions:
- Попробуйте изменить чужую задачу как обычный пользователь - получите 403
- Попробуйте доступ к `/tasks/admin-only/` как обычный пользователь - получите 403  
- Администратор имеет доступ ко всем endpoint'ам
