import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

PATH = 'unsplash/'
PHOTO_SIZE_LIMIT = 400

def main():
    url = 'https://unsplash.com/s/photos/portrait-photo%2C-NoAI'
    driver = webdriver.Chrome()
    options = Options()
    options.add_argument('--disable-notifications')

    driver.get(url)
    driver.implicitly_wait(5)

    switch = True
    check_list = None
    start = 2000
    for i in range(1, 120, 1):
        position = 'window/scrollTo(0, ' + str(start*i) + ')'
        driver.execute_script(position)
        print('Move to', position)
        if i == 2:
            button = driver.find_element(By.CLASS_NAME, 'CwMIr.DQBsa.p1cWU.KHq0c.jpBZ0.AYOsT.Olora.I0aPD')
            if button:
                button.click()
                print(button)
                print('button check!')
                time.sleep(3)
            else:
                print('No find the button.')
        time.sleep(10)

        if switch:
            check_list = size_check(driver.page_source)
            if check_list:
                print('Save the check list --> SIZE:', len(check_list))
                switch = False
    if check_list:
        get_image(driver.page_source, check_list)
    else:
        print('NOT GET THE CHECK LIST!!')


def size_check(url):
    check_list = []
    soup = BeautifulSoup(url, features='html.parser')
    tags = soup.find_all('div', {'class': 'MorZF'})
    if len(tags) < PHOTO_SIZE_LIMIT:
        return None
    else:
        for tag in tags:
            link = tag.img
            name = link.get('srcset')
            photo_link = str(name).split(',')
            if len(photo_link) > 1:
                check_list.append(photo_link[9].split()[0])
        return check_list


def get_image(url, check_list):
    # response = requests.get(url)
    # html = response.text
    # soup = BeautifulSoup(html, features='html.parser')
    soup = BeautifulSoup(url, features='html.parser')
    tags = soup.find_all('div', {'class': 'MorZF'})

    index = 1
    print(len(tags), 'will be download..')
    for tag in tags:
        link = tag.img
        name = link.get('srcset')
        photo_link = str(name).split(',')
        if len(photo_link) > 1:
            if link_check(photo_link, check_list):
                download_img(photo_link[9].split()[0], PATH + 'img_0309_add_data' + str(index) + '.jpg')
                index += 1


def link_check(photo_link, check_list):
    link = photo_link[9].split()[0]
    if link in check_list:
        print('Already download...', link)
        return False
    return True


def download_img(url, save_path):
    response = requests.get(url)
    print(f'Download...{url}')
    with open(save_path, 'wb') as f:
        f.write(response.content)
    print('Finish!')


if __name__ == '__main__':
    main()
