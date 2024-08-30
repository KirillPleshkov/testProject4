# Тестовое задание

## Формулировка задания

Задача
- Реализовать Django + Stripe API бэкенд со следующим функционалом и условиями:
- Django Модель Item с полями (name, description, price)
- API с двумя методами:
- GET /buy/{id}, c помощью которого можно получить Stripe Session Id для оплаты выбранного Item. При выполнении этого метода c бэкенда с помощью python библиотеки stripe должен выполняться запрос stripe.checkout.Session.create(...) и полученный session.id выдаваться в результате запроса
- GET /item/{id}, c помощью которого можно получить простейшую HTML страницу, на которой будет информация о выбранном Item и кнопка Buy. По нажатию на кнопку Buy должен происходить запрос на /buy/{id}, получение session_id и далее с помощью JS библиотеки Stripe происходить редирект на Checkout форму stripe.redirectToCheckout(sessionId=session_id)

Доп. Задания: 
- Запуск используя Docker
- Использование environment variables
- Просмотр Django Моделей в Django Admin панели
- Запуск приложения на удаленном сервере, доступном для тестирования
- Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей стоимостью всех Items
- Модели Discount, Tax, которые можно прикрепить к модели Order и связать с соответствующими атрибутами при создании платежа в Stripe - в таком случае они корректно отображаются в Stripe Checkout форме.
- Добавить поле Item.currency, создать 2 Stripe Keypair на две разные валюты и в зависимости от валюты выбранного товара предлагать оплату в соответствующей валюте
- Реализовать не Stripe Session, а Stripe Payment Intent.

Критерии оценки
- Работоспособность
- Чистота и структура куда
- Гибкость и масштабируемость
- Безопасность и обработка ошибок

Доп плюсы:
- использование улучшающих архитектуру проекта, его читаемость, расширяемость и тестируемость паттернов и шаблонов проектирования
- использование более удобных библиотек и технологий, позволяющих ускорить разработку и сделать проект лучше
- скрипт или некий функционал для наполнения БД тестовыми данными
- типизация кода, докстринги
- написание readme по всем нюансам и способам запуска

