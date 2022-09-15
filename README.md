# shop_test_task_rishat

## Настройка и запуск
 
1. Настроить settings.ALLOWED_HOSTS (пример ["127.0.0.1"])
2. Настроить settings.CSRF_TRUSTED_ORIGINS (пример ["http://127.0.0.1:8000"])
3. Задать переменную окружения STRIPE_API_KEY (ключ API STRIPE)
4. Задать переменную окружения SECRET_KEY (секретный ключ django приложения)
5. Произвести миграции `venv/bin/python manage.py migrate`
6. Запустить сервер `venv/bin/python manage.py runserver`

