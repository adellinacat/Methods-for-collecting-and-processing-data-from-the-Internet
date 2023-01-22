from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

s = Service('./chromedriver')

chromeOptions = Options()
chromeOptions.add_argument('start-maximized')

new_goods_dict = {}
trend_goods_dict = {}
price_xpath = "//mvid-shelf-group/mvid-carousel/div[@class='mvid-carousel-outer mv-hide-scrollbar']/div[@class='mvid-carousel-inner']/mvid-product-cards-group/div[@class='product-mini-card__price ng-star-inserted']"
title_xpath = "//mvid-shelf-group/mvid-carousel/div[@class='mvid-carousel-outer mv-hide-scrollbar']/div[@class='mvid-carousel-inner']/mvid-product-cards-group/div[@class='product-mini-card__name ng-star-inserted']"
tab_button_xpath = "//mvid-shelf-group/mvid-switch-shelf-tab-selector/mvid-carousel/div[@class='mvid-carousel-outer mv-hide-scrollbar']/div[@class='mvid-carousel-inner']/button[@class='tab-button ng-star-inserted']"

driver = webdriver.Chrome(service=s, options=chromeOptions)
driver.implicitly_wait(1)
driver.get('https://www.mvideo.ru/')
#Скроллим вниз и ждём загрузку. После догрузки очередного блока скроллим ещё чуть ниже и дожидаемся загрузки нужной карусели:
driver.execute_script("window.scrollBy(0,400)")
time.sleep(0.5)
driver.execute_script("window.scrollBy(0,600)")

#Ожидаем загрузки нужной карусели, переключаемся из "Новинок" в "Тренды" и обратно (Чтобы убедиться что блок стал доступен)
wait = WebDriverWait(driver, 10)
tab_button = wait.until(EC.element_to_be_clickable((By.XPATH, tab_button_xpath)))
tab_button.click()
#После нажатия, xpath кнопки меняется на .....SELECTED, поэтому ищем нужную (Ненажатую) кнопку по-новой
tab_button = wait.until(EC.element_to_be_clickable((By.XPATH, tab_button_xpath)))
tab_button.click()


for i in range(2):
    goods_new = driver.find_elements(By.XPATH, title_xpath)
    prices_new = driver.find_elements(By.XPATH, price_xpath)
    actions = ActionChains(driver)
    actions.move_to_element(goods_new[-1])
    actions.perform()

x = 0
while x <= len(goods_new)-1:
    name_new = goods_new[x].find_element(By.XPATH, ".//div").text
    price_new = prices_new[x].find_element(By.XPATH, ".//mvid-price/div/span[@class='price__main-value']").text
    new_goods_dict[x] = {'title' : name_new, 'price' : price_new}
    x += 1

actions.move_to_element(goods_new[0])
actions.perform()

tab_button = wait.until(EC.element_to_be_clickable((By.XPATH, tab_button_xpath)))
tab_button.click()

for i in range(2):
    goods_trend = driver.find_elements(By.XPATH, title_xpath)
    prices_trend = driver.find_elements(By.XPATH, price_xpath)
    actions = ActionChains(driver)
    actions.move_to_element(goods_trend[-1])
    actions.perform()

x = 0
while x <= len(goods_trend)-1:
    name_trend = goods_trend[x].find_element(By.XPATH, ".//div").text
    price_trend = prices_trend[x].find_element(By.XPATH, ".//mvid-price/div/span[@class='price__main-value']").text
    trend_goods_dict[x] = {'title' : name_trend, 'price' : price_trend}
    x += 1

print("Трендовые товары в МВидео:")
for id, content in trend_goods_dict.items():
    print("Наименование: ", content['title'], "Цена: ", content['price'])

print('\n\n')

print("Новинки в МВидео:")
for id, content in new_goods_dict.items():
    print("Наименование: ", content['title'], "Цена: ", content['price'])