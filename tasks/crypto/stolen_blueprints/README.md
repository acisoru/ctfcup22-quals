# Crypto | easy | Stolen blueprints

## Информация
Появилась информация, что сотрудники нашего завода передают секретные чертежи третьим лицам.
У одного из сотрудников при осмотре на проходной нашли зашифрованную картинку, но он отказался её расшифровывать, за что он был наказан (его поставили в угол).
Поможете нам узнать, что за картинку он выносил с завода?

## Деплой
-

## Выдать участникам
Файлы из папки public

## Описание
-

## Решение
Нам дан зашифрованный файл и сказано, что это картинка формата jpeg. 

Предположим, что это шифр гаммирования. Применим метод протяжки по известному открытому тексту. У jpeg-файлов есть заголовок, который зафиксирован (первые байты у него {ff d8 ff e0} и через 2 байта идет нуль-терменированная строка 'JFIF' ({4a 46 49 46 00})) - вычисляем гамму, которая была наложена на эти кусочки: для первых 4-х байт это {fc ff d8 ff}, а для строки 'JFIF' гамма {10 4a 46 49 46}. То есть мы видим, что каждый байт ксорится с предыдущим байтом открытого текста. Данный шифр называется шифром Тритемиуса или самошифром. 

Расшифровываем картинку [скриптом](solve/brek.py).
## Флаг

`CUP{TRitHEm1U$_on5_l0Ve}`




