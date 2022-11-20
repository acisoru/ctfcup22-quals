# RE | Easy | Simple Encoder

## Информация
> Мы тут написали программу для целостной передачи данных между ПЛК
на дальних северах. Что самое смешное - модифицированное сообщение передалось нормально, а вот декодер где-то потерялся...

## Выдать участникам
- Бинарь encoder
- Бинарный файлик plc_data.bin

## Описание идеи таска
simple encode algo, c++, arm

## Решение
1) Открываем иду/гидру/hiew (последнее для дедов)
2) Офигиваем от кода
3) Фиксим сигнатуры плюсовых функций для аллокации.
4) Радуемся наличию hexrays и реверсим плюсы (переодически плачем)
5) Программа состоит из пары вспомогательных классов и одной функции-кодировщика по алгоритму Голомба 0 степени.
6) Пишем декодер.

Честно говоря таск сделан чтобы был простой реверс)