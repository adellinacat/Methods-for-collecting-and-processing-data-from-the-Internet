from pprint import pprint
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
import requests
import time
import re
import sys

if len(sys.argv) < 2:
    print("Укажите название вакансии для загрузки в БД")
    sys.exit()
elif len(sys.argv) == 2:
    print("Наименование принято. Будет произведён поиск вакансий по запросу \"", sys.argv[1], "\"")
elif len(sys.argv) > 2:
    print("Указано слишком много аргументов. Укажите только один аргумент - наименование искомой вакансии для загрузки в БД")
    sys.exit()

#Объявляем функцию, которая будет преобразовывать списки, получаемые от lxml|xpath в строки
def group(rows):
    concat = ""
    for row in rows:
        concat = concat + str(row)
        rows = concat
    return rows

# функция для передачи собранной информации в коллекцию mongo
def insert_document(collection, data):
    return collection.insert_one(data).inserted_id

#Задаём имя искомой вакансии
name = sys.argv[1]

#Задаём теоретическое максимально возможное количество страниц
max_pages = 10

#Задаём таймаут для запросов к серверу в секундах
wait = 1

#Формируем строку с запросом. Начинаем с первой (Нулевой) страницы
page = 0
url = 'https://hh.ru/search/vacancy?text=' + name + '&page=' + str(page) + '&from=suggest_post&salary=&area=1&ored_clusters=true&enable_snippets=true'

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

#Формируем запрос, получаем данные
responce = requests.get(url, headers=headers)
dom = bs(responce.text, 'lxml')

page = 0
#проверка на символы
regex = re.compile('[a-zA-Zа-яА-ЯёЁ.\s]')

#Создаём словарь, в котором ключом будет являться порядковый номер вакансии
jobdict = {}
jobnum = 1

#Проходим по всем страницам
while page < max_pages:
    url = 'https://hh.ru/search/vacancy?text=' + name + '&page=' + str(page) + '&from=suggest_post&salary=&area=1&ored_clusters=true&enable_snippets=true'
    time.sleep(wait)
    #Читаем страницу
    responce = requests.get(url, headers=headers)
    dom = bs(responce.text, 'lxml')
    
    #Кладём в переменную список вакансий со страницы
    joblist = dom.find_all('div', class_='vacancy-serp-item-body__main-info')
    
    #Для каждой вакансии на странице получаем информацию. N - переменная которая передаётся в качестве аргумента xpath (Поэтому с 1, а не с 0)
    
    for text in joblist:
        jobsalary = text.find('span', class_='bloko-header-section-3')
        #jobsalary = dom.find("(//div[@class='vacancy-serp-item-body__main-info'])[" + str(n) + "]//span[@class='bloko-header-section-3']/text()")
        #Проверяем записи в списке jobsalary   
        if not jobsalary:
            curency = None
            sal_min = None
            sal_max = None
        else:
            jobsalary = group(jobsalary)
            if "руб" in jobsalary.lower():
                curency = "рубль РФ"
            elif "usd" in jobsalary.lower():
                curency = "доллар США"
            elif "eur" in jobsalary.lower():
                curency = "Евро"
            elif "kzt" in jobsalary.lower():
                curency = "казахстанский тенге"
            else:
                curency = "other"
            
            if "от" in jobsalary.lower():
                sal_min = int(regex.sub('', jobsalary))
                sal_max = None
            elif "до" in jobsalary.lower():
                sal_max = int(regex.sub('', jobsalary))
                sal_mix = None
            elif "–" in jobsalary.lower():
                clean = regex.sub('', jobsalary)
                sal_min=int(clean[:clean.find("–")])
                sal_max=int(clean[clean.find("–")+1:])
                     
        company = group(text.find('div', class_='vacancy-serp-item__meta-info-company').find('a').contents)
        jobname = group(text.find('h3', class_='bloko-header-section-3').find('span').find('a').contents)
        link = group(text.find('a', class_='serp-item__title', href=True)['href'])
        
        jobdict[jobnum] = {'comp' : company, 'jobname': jobname, 'link' : link, 'sal_min' : sal_min, 'sal_max' : sal_max, 'currency' : curency}
        
        jobnum += 1
       
    
    page += 1
    
    #Прогрессбар:
    print ("Обработано страниц:", page, "из", max_pages)
print("Сбор данных завершён")

#Выводим собранный список вакансий
print("Собранные вакансии:")
for num in jobdict:
    print (num, "\nКомпания:", jobdict[num]['comp'], "\nВакансия:", jobdict[num]['jobname'],
           "\nСсылка:", jobdict[num]['link'], "\nЗарплата min:", jobdict[num]['sal_min'], 
           "\nЗарплата max:", jobdict[num]['sal_max'], "\nВалюта:", jobdict[num]['currency'],"\n")


#Подключаемся к MongoDB
client = MongoClient('localhost', 27017)
db = client['vacancy_hh']
collection = db['hh.ru_db']

#просматриваем базу и добавляем новые вакансии
i = 0
for n in jobdict:
    if collection.count_documents({ 'link': jobdict[n]['link'] }, limit=1 ) == 0:
        collection.insert_one(jobdict[n])
        i += 1
print("Добавлено ", i, " новых вакансий")
