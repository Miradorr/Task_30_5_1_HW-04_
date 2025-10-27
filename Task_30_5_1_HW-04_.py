

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def driver():
    """Фикстура для инициализации веб-драйвера"""

    # Создаем экземпляр браузера Google Chrome
    driver = webdriver.Chrome()

    # Устанавливаем неявное ожидание в 10 секунд
    driver.implicitly_wait(10)

    # Переходим на страницу авторизации PetFriends
    driver.get('https://petfriends.skillfactory.ru/login')

    # Передаем управление тесту
    yield driver

    # Закрываем браузер после выполнения теста
    driver.quit()


def test_show_all_pets(driver):
    """Тест проверки карточек питомцев с использованием неявных ожиданий"""

    # Вводим email и пароль, нажимаем на кнопку входа
    driver.find_element(By.ID, 'email').send_keys('dsploit2@gmail.com')
    driver.find_element(By.ID, 'pass').send_keys('820663')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Проверяем, что открылась главная страница с питомцами
    assert driver.find_element(By.TAG_NAME, 'h1').text == 'PetFriends'

    # Находим все элементы карточек питомцев
    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    # Проверяем, что на странице одинаковое количество карточек, и что элементов больше нуля
    assert len(images) == len(names) == len(descriptions) > 0, 'Количество карточек, имен и описаний не совпадает'


def test_my_pets_table(driver):
    """Тест проверки таблицы питомцев с явными ожиданиями"""

    # Создаем экземпляр явного ожидания с таймаутом 10 секунд
    wait = WebDriverWait(driver, 10)

    # Явное ожидание и ввод email
    email = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    email.send_keys('dsploit2@gmail.com')

    # Явное ожидание и ввод пароля
    password = wait.until(EC.presence_of_element_located((By.ID, 'pass')))
    password.send_keys('820663')

    # Явное ожидание и нажатие на кнопку входа
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
    button.click()

    # Явное ожидание заголовка главной страницы
    header = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'h1')))
    assert header.text == 'PetFriends'

    # Явное ожидание и переход на страницу 'Мои питомцы'
    my_pets = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Мои питомцы')))
    my_pets.click()

    # Явное ожидание, ждем когда сама таблица питомцев появится в DOM
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table')))

    # Явное ожидание всех строк tbody таблицы (данные питомцев) и проверка, что они есть
    rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table.table tbody tr')))
    assert len(rows) > 0, 'Нет питомцев в таблице'



