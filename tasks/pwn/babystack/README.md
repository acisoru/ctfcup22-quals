# PWN | easy | babystack

## Информация

>  Говорят нет ничего проще сделать ROP на стеке, когда есть все утечки, так ли это?
> 
> nc <ip> 13773
>

## Деплой

```sh
cd deploy
docker-compose up --build -d
```

## Выдать участинкам

Архив из директории [public/](public/) и IP:PORT сервера

## Описание
ROP в ядре, обойти все актуальные встроенные защиты ядра

## Решение

1. Ликам KASLR через чтение со стека
2. Формируем ROP для вызова commit_creds(prepare_kernel_cred(0))

[пример эксплоита](solve/main.c)

## Флаг

`CUP{b4by_st4ck_f0r_y0000o0o0oo0u_af39bc041}`