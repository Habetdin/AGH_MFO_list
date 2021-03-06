# Чёрный список сайтов микрофинансовых организаций (МФО) для AdGuard Home

Информация о действующих МФО по состоянию на 12.02.2022

## Информация о списке

Данный [список для AdGuard Home](blocklist.txt) включает в себя адреса веб-сайтов:

- Действующих микрофинансовых компаний (МФК)
- Действующих микрокредитных компаний (МКК)
- Исключенных из реестра, но доступных в сети МФО

Данные по действующим МФО обновляются из [государственного реестра МФО][registry-file],
размещённого [в соответствующем разделе][registry-page] сайта Банка России. [Данные по исключенным организациям](mirrors.txt) сохраняются вручную при их исчезновении из актуальной версии реестра.

## Обновление списка

Для самостоятельного обновления чёрного списка, скопируйте колонку N («Адреса официальных сайтов в информационно-телекоммуникационной сети "Интернет"») из [Excel-файла реестра][registry-file] в файл `source.txt`, исправьте пути к используемым файлам в скрипте [`generate.py`](generate.py) и запустите его.

Для запуска скрипта Вам понадобится Python 3+ с установленным модулем [IDNA](https://pypi.org/project/idna/).

[registry-file]: <https://cbr.ru/vfs/finmarkets/files/supervision/list_MFO.xlsx> "Государственный реестр микрофинансовых организаций"
[registry-page]: <https://cbr.ru/microfinance/registry/> "Реестры субъектов рынка микрофинансирования"
