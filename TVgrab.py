__author__ = 'Keiran'
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep

user_login = "rafiq@list.ru "
user_password = "ump.87uv"

wd = webdriver.Firefox()
wd.get('https://topvisor.ru/projects/')
wd.maximize_window()


class Project():
    def __init__(self, url, keywords_count, id):
        self.url = url
        self.keywords_count = keywords_count
        self.id = id
        self.keywords = {}


def login(user_login, user_password):
    wd.get("https://topvisor.ru/")
    wd.find_element_by_link_text("Вход").click()
    wd.find_element_by_name("authorisation_login").click()
    wd.find_element_by_name("authorisation_login").clear()
    wd.find_element_by_name("authorisation_login").send_keys(user_login)
    wd.find_element_by_name("authorisation_pass").click()
    wd.find_element_by_name("authorisation_pass").click()
    wd.find_element_by_name("authorisation_pass").clear()
    wd.find_element_by_name("authorisation_pass").send_keys(user_password)
    wd.find_element_by_link_text("Войти").click()


def get_projects_id():
    sleep(3)
    project_list = wd.find_elements_by_css_selector('.project.tag1')
    for project in project_list:
        project_keywords = project.find_element_by_css_selector('.count_keywords').text
        project_id = project.find_element_by_css_selector('a.dynamics').get_attribute('href')
        project_url = project.find_element_by_css_selector('span.site').get_attribute('title')
        print(project_keywords, project_id, project_url)
    return ['281590']


def get_project_info(pid):
    count = 0
    wd.get('https://topvisor.ru/project/dynamics/%s/' %pid)
    Select(wd.find_element_by_name("limit")).select_by_index(5)
    table = wd.find_element_by_id('dynamics_table')
    rows = table.find_elements_by_css_selector('tr')
    for row in rows:
        count += 1
        cells = row.find_elements_by_css_selector('td')
        for c in cells:
            print(str(count), c.text)


login(user_login, user_password)
projects_id = get_projects_id()
for project in projects_id:
    pass
   # get_project_info(project)
wd.close()
