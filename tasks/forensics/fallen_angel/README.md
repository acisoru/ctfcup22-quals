# Forensic | Medium | Fallen Angel

## Информация
Нам удалось перехватить беспилотный летательный аппарат и получить данные из него, твоя задача - найти населенный пункт, откуда в последний раз происходил запуск этого дрона. Флаг - название населенного пункта латиницей с большой буквы.
URLS:
[MEGA](https://mega.nz/file/erpxRIIb#0YXut2ZN26ybLCn_LVutBXk_4yQSYHQ6vLe7JCBjqzY)
[Google Drive](https://drive.google.com/file/d/1guSb1xYhBJqHosvACePygdAy4e4QUFs-/view?usp=sharing)
[Yandex Disk](https://disk.yandex.ru/d/ATkt0XeUoIXjZA)
[Torrent](public/drone.E01.torrent)

## Деплой
-

## Выдать участникам
-

## Описание
-

## Решение
Гуглим, находим,что E01 это криминалистический образ диска, с которым можно работать с помощью различных утилит для форензики, к примеру FTK Imager или ewf-tools

Начальный этап доступа к файловой системе можно произвести несколькими способами:

Создаем точку монтирования 
``` bash
(kali@kali)-[~/Downloads]
└─$ mkdir ext_sd                                                                
```

Монтируем образ
```bash
┌──(kali@kali)-[~/Downloads]
└─$ ewfmount drone.E01 ext_sd 
ewfmount 20140807
                                                                                                                           
┌──(kali@kali)-[~/Downloads]
└─$ ls ext_sd 
ewf1
``` 

Просматриваем структуру каталогов внутри образа

```bash                                                                                                                               
┌──(kali@kali)-[~/Downloads]
└─$ fls -r ext_sd/ewf1
d/d 3:  LOST.DIR
d/d 4:  DCIM
+ d/d 3077:     100MEDIA
++ r/r 1357829: DJI_0001.MP4
++ r/r 1357830: DJI_0002.MP4
++ r/r 1357831: DJI_0003.MP4
++ r/r 1357833: DJI_0006.MP4
++ r/r * 1357836:       .DJI_0005.MP4.trinf
++ r/r * 1357839:       .DJI_0005.MP4.avc1
d/d 5:  MISC
+ d/d 4101:     THM
++ d/d 5125:    100
+++ r/r 1358853:        DJI_0001.THM
+++ r/r 1358854:        DJI_0002.THM
+++ r/r 1358855:        DJI_0003.THM
+++ r/r 1358856:        DJI_0004.THM
+++ r/r 1358857:        DJI_0005.THM
+ d/d 4102:     GIS
++ r/r 6150:    dji.gis
+ d/d 4103:     IDX
++ r/r * 1356807:       .VR_dji_A2UMXs
++ r/r * 1356810:       .VR_dji_kzIxFO
d/d 8:  System Volume Information
+ r/r 208425991:        IndexerVolumeGuid
+ r/r 208425994:        WPSettings.dat
v/v 268368899:  $MBR
v/v 268368900:  $FAT1
v/v 268368901:  $FAT2
V/V 268368902:  $OrphanFiles                                                                                                                          
```

 Извлекаем файл из  образа
```bash
┌──(kali@kali)-[~/Downloads]
└─$ icat ext_sd/ewf1 1357829 > DJI_0006.MP4  
```

Альтернативный вариант

Создаем точку монтирования
```bash
(kali㉿kali)-[~/Downloads]
└─$ sudo mkdir /mnt/drone                                                                                                  
```

Конвертируем образ в формат vdi и монтируем его к системе
```bash
┌──(kali㉿kali)-[~/Downloads]
└─$ sudo xmount --in ewf drone.E01 --cache /tmp/disk.cache --out vdi /mnt/drone
                                                                                                                               
┌──(kali㉿kali)-[~/Downloads]
└─$ ls /mnt/drone 
drone.info  drone.vdi
```
Для более простого доступа  конвертируем в формат img
```bash
(kali㉿kali)-[/mnt/drone]
└─$ sudo VBoxManage clonehd --format raw drone.vdi /home/kali/Downloads/mavic.img              
0%...10%...20%...30%...40%...50%...60%...70%...80%...90%...100%
Clone medium created in format 'raw'. UUID: f1842ab8-011f-4ec8-9526-263892d257bf
```

Получаем иформацию о файловой системе образа
```bash
sudo fdisk -l /home/kali/Downloads/mavic.img                                                                           
Disk /home/kali/Downloads/mavic.img: 8 GiB, 8589934592 bytes, 16777216 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x00000000
```

Монтируем получившийся ранее img образ
```bash
kali㉿kali)-[/mnt/drone]
└─$ sudo mount -t msdos -o loop,rw /home/kali/Downloads/mavic.img /mnt  
```

Финальный этап

Получаем метаинформацию из видеофайлов
```bash
exiftool DJI_0006.MP4 

ExifTool Version Number         : 12.50
File Name                       : DJI_0260.MP4
Directory                       : .
File Size                       : 671 MB
File Modification Date/Time     : 2022:11:14 17:11:11+03:00
File Access Date/Time           : 2022:11:14 17:20:23+03:00
File Inode Change Date/Time     : 2022:11:14 17:16:09+03:00
File Permissions                : -rw-r--r--
File Type                       : MP4
File Type Extension             : mp4
MIME Type                       : video/mp4
Major Brand                     : MP4 Base w/ AVC ext [ISO 14496-12:2005]
Minor Version                   : 2014.2.0
Compatible Brands               : avc1, isom
Media Data Size                 : 670965710
Media Data Offset               : 44
Movie Header Version            : 0
Create Date                     : 2022:09:10 10:36:23
Modify Date                     : 2022:09:10 10:36:23
Time Scale                      : 30000
Duration                        : 0:02:32
Preferred Rate                  : 1
Preferred Volume                : 100.00%
Preview Time                    : 0 s
Preview Duration                : 0 s
Poster Time                     : 0 s
Selection Time                  : 0 s
Selection Duration              : 0 s
Current Time                    : 0 s
Next Track ID                   : 4
GPS Coordinates (err)           : 56 deg 42' 24.48" N, 37 deg 22' 2.28" E
Speed X (err)                   : +0.00
Speed Y (err)                   : +0.00
Speed Z (err)                   : +0.00
Pitch (err)                     : -4.90
Yaw (err)                       : -110.60
Roll (err)                      : +1.50
Camera Pitch (err)              : -24.50
Camera Yaw (err)                : +0.80
Camera Roll (err)               : +0.00
Comment                         : DE=None,SN=1SFOK170AB0A4H, Type=Normal, HQ=Normal, Mode=P
Category                        : v00.00.0637, 0.0.1, v1.0.0
Model                           : FC7203
User Data mux (fr)              : 
Track Header Version            : 0
Track Create Date               : 2022:09:10 10:36:23
Track Modify Date               : 2022:09:10 10:36:23
Track ID                        : 1
Track Duration                  : 0:02:32
Track Layer                     : 0
Track Volume                    : 0.00%
Image Width                     : 1920
Image Height                    : 1080
Graphics Mode                   : srcCopy
Op Color                        : 0 0 0
Compressor ID                   : avc1
Source Image Width              : 1920
Source Image Height             : 1080
X Resolution                    : 72
Y Resolution                    : 72
Compressor Name                 : AVC encoder
Bit Depth                       : 24
Video Frame Rate                : 29.97
Meta Format                     : priv
Warning                         : [minor] The ExtractEmbedded option may find more tags in the media data
Matrix Structure                : 1 0 0 0 1 0 0 0 1
Media Header Version            : 0
Media Create Date               : 2022:09:10 10:36:23
Media Modify Date               : 2022:09:10 10:36:23
Media Time Scale                : 30000
Media Duration                  : 0:02:32
Handler Class                   : Media Handler
Handler Type                    : Text
Handler Description             : .DJI.Subtitle
Gen Media Version               : 0
Gen Flags                       : 0 0 0
Gen Graphics Mode               : ditherCopy
Gen Op Color                    : 32768 32768 32768
Gen Balance                     : 0
Other Format                    : text
GPS Coordinates                 : 56 deg 42' 24.48" N, 37 deg 22' 2.28" E
Speed X                         : +0.00
Speed Y                         : +0.00
Speed Z                         : +0.00
Pitch                           : -4.90
Yaw                             : -110.60
Roll                            : +1.50
Camera Pitch                    : -24.50
Camera Yaw                      : +0.80
Camera Roll                     : +0.00
User Data mux                   : 
Image Size                      : 1920x1080
Megapixels                      : 2.1
Avg Bitrate                     : 35.3 Mbps
GPS Latitude                    : 56 deg 42' 24.48" N
GPS Longitude                   : 37 deg 22' 2.28" E
Rotation                        : 0
GPS Position                    : 56 deg 42' 24.48" N, 37 deg 22' 2.28" E
```

Используя найденные координаты получаем название населенного пункта


## Флаг

`CUP{Krivets}`
