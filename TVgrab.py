__author__ = 'Keiran'
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep
from topvizproject import Project, Keyword

user_login = "rafiq@list.ru"
user_password = "ump.87uv"
base_url = 'https://topvisor.ru/projects/'


def init_session():
    global wd
    wd = webdriver.Firefox()
    wd.maximize_window()


def send_keys(locator, text):
    global wd
    wd.find_element_by_name(locator).click()
    wd.find_element_by_name(locator).clear()
    wd.find_element_by_name(locator).send_keys(text)


def login(user_login, user_password):
    global wd
    wd.get(base_url)
    wd.find_element_by_link_text("Вход").click()
    send_keys("authorisation_login", user_login)
    send_keys("authorisation_pass", user_password)
    wd.find_element_by_link_text("Войти").click()
    sleep(5)


def get_projects_data():
    """
    получение исходных данных о проекте: ид, ссылка, количество ключей
    :return: list of Project()
    """
    project = Project()
    result = list()
    project_list = wd.find_elements_by_css_selector('.project.tag1')
    for row in project_list:
        project.title = row.find_element_by_css_selector('span.site').get_attribute('title')
        project.keywords_count = row.find_element_by_css_selector('.count_keywords').text
        project.tv_url = row.find_element_by_css_selector('a.dynamics').get_attribute('href')
        result.append(Project(title=project.title,
                              keywords_count=project.keywords_count,
                              tv_url=project.tv_url))
    return result


def get_info_list(css_selector):
    global wd
    keywords = wd.find_elements_by_css_selector(css_selector)
    k_list = list ()
    for keyword in keywords:
        k_list.append(keyword.text)
    return  k_list


def get_project_statistic(project):
    count = 0
    wd.get(project.tv_url)
    Select(wd.find_element_by_name("limit")).select_by_index(5)
    sleep(5)
    # получение списка ключевых фраз
    k_list = get_info_list('div.tag0.middle')
    print(k_list)
    # получение дат
    d_list =get_info_list('td>span.date')
    print(d_list)
    project = Project()
    # получение позиций
    table = wd.find_element_by_id('dynamics_table')
 #   row = table.find_elements_by_css_selector('div.cols>table>tbody>tr>td>div')
    row = table.find_elements_by_css_selector('div.cols>table>tbody>tr')
    for k_index in range(len(k_list)):
        for d_index in range(len(d_list)):
            try:
                pos = row[k_index+1].find_elements_by_css_selector('td')[d_index].find_element_by_css_selector('div>a').text

            except:
                pos = '-'
            kwrd = Keyword(group='', date=d_list[d_index],position=pos)
            project.add_keyword(element=k_list[k_index], kwrd)
            print('Keywords: %s; Date: %s; position: %s' % (k_list[k_index], d_list[d_index], pos))
    print(project)





"""
    table = wd.find_element_by_id('dynamics_table')
    rows = table.find_elements_by_css_selector('tr')
    k_w = ()
    for row in rows:
        count += 1
        cells = row.find_elements_by_css_selector('td')

        print('')
        print(keyword.text)
  #      for c in cells:
   #         print(str(count), c.text)
"""

init_session()
login(user_login, user_password)
try:
    projects = get_projects_data()
    print(projects)

#    for num in range(len(projects)):
    num = 0
    get_project_statistic(projects[num])
#except:
#    print('Some error')
finally:
    wd.close()
