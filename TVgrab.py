__author__ = 'Keiran'
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

user_login = "rafiq@list.ru"
user_password = "ump.87uv"
base_url = 'https://topvisor.ru/projects/'


def init_session(debug=False):
    global wd
    if debug:
        wd = webdriver.Firefox()
        wd.maximize_window()
    else:
        # основной PhantomJS
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0"
        dcap["phantomjs.page.settings.userAgent"] = list(user_agent)
        wd = webdriver.PhantomJS(desired_capabilities=dcap)


def send_keys(locator, text):
    global wd
    wd.find_element_by_name(locator).click()
    wd.find_element_by_name(locator).clear()
    wd.find_element_by_name(locator).send_keys(text)


def login(user_login, user_password):
    global wd
    wd.get(base_url)
    #   wd.save_screenshot('t.png')
    wd.find_element_by_link_text("Вход").click()
    send_keys("authorisation_login", user_login)
    send_keys("authorisation_pass", user_password)
    wd.find_element_by_link_text("Войти").click()
    wait_until_element_present('.spoiler-head')
    #   wd.save_screenshot('1.png')


def get_projects_data():
    """
    получение исходных данных о проекте: ид, ссылка, количество ключей
    :return: list of Project()
    """
    #   wd.save_screenshot('2_get_project_data_start.png')
    sleep(5)
    result = dict()
    project_list = wd.find_elements_by_css_selector('.project.tag1')
    for row in project_list:
        title = row.find_element_by_css_selector('span.site').get_attribute('title')
        # project.keywords_count = row.find_element_by_css_selector('.count_keywords').text
        tv_url = row.find_element_by_css_selector('a.dynamics').get_attribute('href')
        result[tv_url] = title
    #   wd.save_screenshot('3_get_project_data_finish.png')
    return result


def get_info_list(css_selector):
    global wd
    sleep(1)
    keywords = wd.find_elements_by_css_selector(css_selector)
    k_list = list()
    for keyword in keywords:
        k_list.append(keyword.text)
        print(keyword.text)
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


def get_group_statistic(d_list):
    global wd
    # Получение списка ключей
    k_list = get_info_list('div.tag0.middle')
    print('Список ключей: %s' % k_list)
    if len(k_list) > 10:
        # установка кол-ва ключей на страницу
        Select(wd.find_element_by_name("limit")).select_by_index(6)
        sleep(5)
        if len(k_list) > 1000:
            page_count = len(get_combobox_options('page'))
        else:
            page_count = 1
    # получение дат
    table = wd.find_element_by_id('dynamics_table')
    row = table.find_elements_by_css_selector('div.cols>table>tbody>tr')
    keyword_statistic = {}
    for k_index in range(len(k_list)):
        date_pos = {}
        for d_index in range(len(d_list)):
            try:
                pos = row[k_index+1].find_elements_by_css_selector('td')[d_index].\
                    find_element_by_css_selector('div>a').text
            except:
                pos = '-'
            date_pos[d_list[d_index]] = pos
        keyword_statistic[k_list[k_index]] = date_pos
    return keyword_statistic


def wait_until_element_present(css_locator, wait_time=10):
    global wd
    time = 0
    def skip(time):
        sleep(1)
        time += 1
    try:
        while (not wd.find_element_by_css_selector(css_locator).is_displayed()) and (time < wait_time):
            skip(time)
    except NoSuchElementException:
            skip(time)


def get_region_statistic():
    g_list = get_combobox_options('group_id')[1:]
    groups = {}
    print('Найдено групп %d' % len(g_list))
    d_list = get_info_list('td>span.date')
    print('Список дат %s' % d_list)
    for g_num in range(len(g_list)):
        print('Выбор группы %s' % g_list[g_num])
        Select(wd.find_element_by_name("group_id")).select_by_index(g_num+1)
        wait_until_element_present('.up_position.min_width')
        print('Получение статистики группы')
        k_w = get_group_statistic(d_list)
        print('Гет регион статистик: %s' % k_w)
        groups[g_list[g_num]] = k_w
    return groups


def get_region_ids():
    global wd
    result = list()
    cb = wd.find_element_by_name('region_key')
    options = cb.find_elements_by_css_selector('option')
    for option in options:
        try:
            value = option.get_attribute("value")
            column_position = value.find(':')
            if column_position > 0 and value.find('-') == -1:
                result.append(value[:column_position])
        except:
            pass
    return result


def get_se_statistic(region=None):
    r_list = list()
    if region is None:
        r_list = get_region_ids()
    else:
        r_list.append(region)
    regions = {}
    for r_num in range(len(r_list)):
        Select(wd.find_element_by_name("region_key")).select_by_index(r_num)
        wait_until_element_present('.up_position.min_width')
        kw = get_region_statistic()
        regions[r_list[r_num]] = kw
    return regions


def set_dates():
    global wd
    wd.find_element_by_css_selector(".dates_text").click()
    wd.find_element_by_name('date1').click()
    wd.find_element_by_name('date1').send_keys(Keys.HOME)
    wd.find_element_by_name('date1').send_keys('09.10.2009' + Keys.END + 10 * Keys.BACKSPACE)
    sleep(1)
    wd.find_elements_by_css_selector(".btn.go")[2].click()
    sleep(1)


def save_project(project, export_file_name):
    import json
    with open('%s.json' % export_file_name, 'w') as out_file:
        out_file.write(json.dumps(project, lambda x: x.__dict__, indent=2))


def get_project_statistic(project_url, site_url, project_list):
    wd.get(project_url)
#    wd.save_screenshot('project_page.png')

    project_statistics = {}
    se_stat = {}
    se_list = get_combobox_options("searcher")[:-2]
    print('se_list %s' % se_list)
    set_dates()
    se_full = ('Yandex', 'Google', 'go.Mail')
    se_short = ('Google.com', 'Yandex.com')
    reg_num = 0
    for index in range(len(se_list)):
        if (se_list[index] in se_full) or (se_list[index] in se_short):
            if se_list[index] in se_full:
                Select(wd.find_element_by_name("searcher")).select_by_index(index)
                se_stat[se_list[index]] = get_se_statistic()
            elif se_list[index] == 'Yandex.com':
                se_stat[se_list[index]] = get_se_statistic('87')
            elif se_list[index] == 'Google.com':
                se_stat[se_list[index]] = get_se_statistic('87')
            project_statistics[se_list[index]] = se_stat[se_list[index]]
            reg_num += 1
    project_statistics_with_url = dict()
    project_statistics_with_url[site_url] = project_statistics
    project_list[project_url] = project_statistics_with_url


def save_project_list(project_list, export_file_name):
    import json
    with open('%s.json' % export_file_name, 'w') as out_file:
        out_file.write(json.dumps(project_list, indent=2))

init_session(debug=True)
login(user_login, user_password)
try:
    full_info = dict()
    full_info['login'] = user_login
    full_info['password'] = user_password
    full_info['projects'] = get_projects_data()

    file_name = 'project_list_%s' % user_login

    save_project_list(full_info, file_name)

    # project_statistic = dict()
    # for num in projects:
    #     get_project_statistic(project_url=num, site_url=projects[num], project_list=project_statistic)
    # file_name = user_login
    # save_project(project=project_statistic, export_file_name=file_name)
except NoSuchElementException:
    print('Element not found')
    wd.save_screenshot('Error.png')
finally:
    wd.close()
