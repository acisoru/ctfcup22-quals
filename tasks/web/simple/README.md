# Web | easy | simple_login

## Информация
> Мы начали делать сервис, начали с реализации аутентификации. Проверьте, нет ли здесь ошибок 
> https://<somedomain>:5767

## Деплой
1. Получить TLS сертификат
2. Положить файлы cert.pem, privkey.pem в папку /keys
3. docker-compose up -d --build

## Выдать участникам
Адрес до сервиса
https://<somedomain>:5767

## Описание
Таск на подмену алгоритма подписи для JWT токена с RS256 на HS256.

## Решение
1. Войти под любым логином и паролем
2. Забрать JWT токен на странице /profile
3. В шапке токена поменять алгоритм шифрования на HS256
4. В качестве ключа шифрования взять открытый ключ для шифрования HTTPS траффика
5. Подписать новый токен
6. Закинуть обратно в cookie
7. Перезагрузить /profile

## Флаг

`CUP{easy_breezy_jwt}`
