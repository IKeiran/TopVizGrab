__author__ = 'Keiran'
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep
from topvizproject import Project

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
    sleep(1)
    keywords = wd.find_elements_by_css_selector(css_selector)
    k_list = list()
    for keyword in keywords:
        k_list.append(keyword.text)
        print(keyword.text)
#    print('GIL end')
    return k_list


def get_combobox_options(cb_name):
    global wd
    result = list()
    cb = wd.find_element_by_name(cb_name)
    options = cb.find_elements_by_css_selector('option')
    for option in options:
        try:
            result.append(option.text)
        except:
            pass
    return result


def save_project(project):
    import json
    with open('test.json', 'w') as out_file:
        out_file.write(json.dumps(project, lambda x: x.__dict__, indent=2))


def get_group_statistic(d_list):
    global wd
    # Получение списка ключей
    k_list = get_info_list('div.tag0.middle')
    print('Список ключей: %s' % k_list)
    if len(k_list)>10:
        Select(wd.find_element_by_name("limit")).select_by_index(6) # установка кол-ва ключей на страницу
        sleep(5)
        if len(k_list)>1000:
            page_count = len(get_combobox_options('page'))
        else:
            page_count = 1
    # получение дат
    table = wd.find_element_by_id('dynamics_table')
    row = table.find_elements_by_css_selector('div.cols>table>tbody>tr')
    keyword_statisic = {}
    for k_index in range(len(k_list)):
        date_pos = {}
        for d_index in range(len(d_list)):
            try:
                pos = row[k_index+1].find_elements_by_css_selector('td')[d_index].find_element_by_css_selector('div>a').text
            except:
                pos = '-'
            date_pos[d_list[d_index]] = pos
        keyword_statisic[k_list[k_index]] = date_pos
    return keyword_statisic


def get_region_statistic():
    g_list = get_combobox_options('group_id')[1:]
    groups = {}
    print('Найдено групп %d' % len(g_list))
    d_list = get_info_list('td>span.date')
    print('Список дат %s' % d_list)
    for g_num in range(len(g_list)):
        print('Выбор группы %s' % g_list[g_num])
        Select(wd.find_element_by_name("group_id")).select_by_index(g_num+1)
        sleep(5)
        print('Получение статистики группы')
        k_w = get_group_statistic(d_list)
        print('Гет регион статистик: %s' % k_w)
        groups[g_list[g_num]]=k_w
    return groups


def get_region_ids():
    global wd
    result = list()
    cb = wd.find_element_by_name('region_key')
    options = cb.find_elements_by_css_selector('option')
    for option in options:
        try:
            punkt = option.get_attribute("value")
            colpos = punkt.find(':')
            if colpos > 0 and punkt.find('-') == -1:
                result.append(punkt[:colpos])
        except:
            pass
    return result


def get_se_statistic(region = None):
    r_list = list()
    if region is None:
        r_list = get_region_ids()
    else:
        r_list.append(region)
    regions = {}
    for r_num in range(len(r_list)):
        Select(wd.find_element_by_name("region_key")).select_by_index(r_num)
        sleep(5)
        kw = get_region_statistic()
        regions[r_list[r_num]]=kw
    return regions


def set_dates():
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver import ActionChains
    global wd
    w = wd
    wd.find_element_by_css_selector(".dates_text").click()
    wd.find_element_by_name('date1').click()
    wd.find_element_by_name('date1').clear()
    send_keys('date1', '01.01.2013')
    wd.find_element_by_css_selector(".btn.go").click()


def get_project_statistic(project):
    wd.get(project.tv_url)
    all = {}
    se_stat = {}
    se_list = get_combobox_options("searcher")[:-2]
    set_dates()
    SE_FULL = ('Yandex', 'Google', 'go.Mail')
    SE_SHORT = ('Google.com', 'Yandex.com')
    reg_num = 0
    for index in range(len(se_list)):
        if (se_list[index] in SE_FULL) or (se_list[index] in SE_SHORT):
            if se_list[index] in SE_FULL:
                Select(wd.find_element_by_name("searcher")).select_by_index(index)
                se_stat[se_list[index]] = get_se_statistic()
            elif se_list[index] == 'Yandex.com':
                se_stat[se_list[index]] = get_se_statistic('87')
            elif se_list[index] == 'Google.com':
                se_stat[se_list[index]] = get_se_statistic('87')
            all[se_list[index]] = se_stat[se_list[index]]
            reg_num+=1
    save_project(all)

    # получение позиций

#    save_project(project)


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
