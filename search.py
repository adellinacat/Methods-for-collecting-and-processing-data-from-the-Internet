import sys
from pymongo import MongoClient

#Подключение к MongoDB
client = MongoClient('localhost', 27017)
db = client['vacancy_hh']
collection = db['hh.ru_db']

if len(sys.argv) < 2:
    print("Недостаточно аргументов. Укажите желаемую сумму зарплаты, для поиска в БД")
    sys.exit()
elif len(sys.argv) == 2:
    print("Принято. Будет произведён поиск вакансий с желаемой зарплатой, не менее", sys.argv[1]," рублей")
elif len(sys.argv) > 2:
    print("Указано слишком много аргументов. Укажите только один аргумент - желаемую зарплату")
    sys.exit()

# функция для поиска по величине ЗП
def find_job(zp):
    res=collection.find({"$or":[{ 'sal_min': { "$gte": zp } },{'sal_max': {"$gte": zp} }]})
    for x in res:
        print ("\nКомпания:", x['comp'], "\nВакансия:", x['jobname'], "\nСсылка:", x['link'],
               "\nЗарплата min:", x['sal_min'], "\nЗарплата max:", x['sal_max'], "\nВалюта:", x['currency'],"\n")

# Задаем параметр поиска, выводим результат
zarplata = int(sys.argv[1])
find_job(zarplata)
