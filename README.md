# Практическая работа к 8 уроку
## Приложение для сбора вакансий с сайта hh.ru, загрузки списка вакансий в БД mongodb и поиска вакансий в БД.

### Сбор вакансий
Для сбора вакансий требуется запустить файл download.py, указав в качестве аргумента ключевое слово для поиска. например:
```
python3 download.py Архитектор
```

download.py подключается к hh.ru и получает вакансии с первых 10 страниц поиска по ключевому слову, после чего сохраняет их в БД MongoDB. MongoDB должна быть запущена на локальной машине и быть доступна для подключения.
![Попытка поиска с пустой БД](https://github.com/adellinacat/Methods-for-collecting-and-processing-data-from-the-Internet/blob/lesson_8/Screenshots/First_search.png?raw=true)



### Поиск по базе вакансий
Для поиска вакансий с интересующим уровнем заработной платы необходимо запустить файл search.py, указав в качестве аргумента желаемую зарплату:
```
python3 search.py 200000
```

Вывод программы будет содержать список вакансий, в которых уровень зарплаты выше или равен заданному

Поиск по бустой БД:
![Попытка поиска с пустой БД](https://github.com/adellinacat/Methods-for-collecting-and-processing-data-from-the-Internet/blob/lesson_8/Screenshots/First_search.png?raw=true)
Загрузка вакансий:
![Начало загрузки вакансий](https://github.com/adellinacat/Methods-for-collecting-and-processing-data-from-the-Internet/blob/lesson_8/Screenshots/Download_1.png?raw=true)
Вакансии загружены:
![Загрузка завершена](https://github.com/adellinacat/Methods-for-collecting-and-processing-data-from-the-Internet/blob/lesson_8/Screenshots/Download_2.png?raw=true)
Поиск вакансий по БД:
![Поиск вакансий по БД](https://github.com/adellinacat/Methods-for-collecting-and-processing-data-from-the-Internet/blob/lesson_8/Screenshots/second_search.png?raw=true)
Содержимое MondoDB (Просмотр через compass):
![Содержимое MongoDB](https://github.com/adellinacat/Methods-for-collecting-and-processing-data-from-the-Internet/blob/lesson_8/Screenshots/DB.png?raw=true)
