import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

# добавим исключения, чтобы тест не падал на них потом
ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)

# подтянем драйвер селениума для хрома и перейдем по ссылке
url = r'http://zpp.rospotrebnadzor.ru/Forum/Appeals'
driver = webdriver.Chrome(executable_path='C:/Users/Kuruma/Desktop/chromedriver.exe')
driver.get(url)

# теперь для каждой записи (первой, второй...) на странице пройдем по всем страницам
for number in range(1, 6):
    for page_number in range(1, 2034):
        # поставим неявное ожидание, чтобы тест подождал, пока поле с вводом страницы появится
        WebDriverWait(driver, 20, ignored_exceptions = ignored_exceptions).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pagerCustomPage"]')))
        # очистим поле, введем номер страницы и кликнем рядом с полем кнопку перейти на страницу
        driver.find_element_by_xpath('//*[@id="pagerCustomPage"]').clear()
        driver.find_element_by_xpath('//*[@id="pagerCustomPage"]').send_keys(page_number)
        driver.find_element_by_xpath('//*[@id="pagerCustomPageAddon"]').click()
        # поспим пока откроется страница
        time.sleep(7)
        title = driver.find_element_by_xpath('//*[@id="appeals-list"]/div[2]/div[2]/div[{}]/div/div[2]/div/a/span'.format(number))
        title.click()
        # подождем пока появится текст и запишем его
        WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#mainbody > div.row.vm-20 > div > div > div:nth-child(2) > div:nth-child(1) > p')))
        new_text = driver.find_element_by_css_selector(
            '#mainbody > div.row.vm-20 > div > div > div:nth-child(2) > div:nth-child(1) > p').text
        # для подстраховки читаем уже записанное и добавляем к нему новый текст, @$% - чтобы не потерять начало нового текста
        with open("complaints300.txt", "r", encoding='utf-8') as f:
             data = f.read()
        with open("complaints300.txt", "w", encoding='utf-8') as text_file:
                try: text_file.write(data + "@$%" + new_text)
                except Exception: text_file.write(data + "@$%" + page_number)
        # вернемся на предыдущую (на этом умном сайте - на первую) страницу
        driver.back()
# закроем браузер и освободим память
driver.quit()
