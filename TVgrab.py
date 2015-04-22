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


def print_log(text):
    global debug
    if debug:
        print(text)

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
    project_list = list()
    # архивные проекты вырезаю
    active_block = wd.find_elements_by_css_selector('.spoiler-wrapper')[0:3]
    for i in range(2):
        try:
            projects = active_block[i].find_elements_by_css_selector('.project.tag1')
            if len(projects) > 0:
                for pr in projects:
                    project_list.append(pr)
        except NoSuchElementException:
            pass
    for row in project_list:
        title = row.find_element_by_css_selector('span.site').get_attribute('title')
        # project.keywords_count = row.find_element_by_css_selector('.count_keywords').text
        tv_url = row.find_element_by_css_selector('a.dynamics').get_attribute('href')
        result[tv_url] = title
    #   wd.save_screenshot('3_get_project_data_finish.png')
    print_log('Получены все данные о проектах')
    return result


def get_info_list(css_selector):
    global wd
    sleep(1)
    keywords = wd.find_elements_by_css_selector(css_selector)
    k_list = list()
    for keyword in keywords:
        k_list.append(keyword.text)
        print_log('get info list %s ' % keyword.text)
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


def get_group_statistic(date_list):
    global wd
    keys_on_page = 10
    # Получение списка ключей
    keywords_count = wd.find_element_by_css_selector('.total').text[1:-1]
    if int(keywords_count) > 10:
        print_log('установка кол-ва ключей на страницу')
        # установка кол-ва ключей на страницу
        Select(wd.find_element_by_name("limit")).select_by_index(0)
        sleep(5)
        page_count = int(keywords_count) // keys_on_page + 1
    else:
        page_count = 1
    print_log('количество страниц %d' % page_count)
    keyword_statistic = {}

    for i in range(page_count):
        print_log('Страница %d из %d' % (i+1, page_count))
        if i > 0:
            print_log('Установлена %d страница из %d' % (i, page_count))
            Select(wd.find_element_by_name("page")).select_by_index(i)
            sleep(2)

        k_list = get_info_list('div.tag0.middle')
        print_log('Список ключей: %s, количество: %d' % (k_list, len(k_list)))
        Select(wd.find_element_by_name("limit")).select_by_index(0)

        # получение дат
        table = wd.find_element_by_id('dynamics_table')
        row = table.find_elements_by_css_selector('div.cols>table>tbody>tr')

        for k_index in range(len(k_list)):
            date_pos = {}
            for d_index in range(len(date_list)):
                try:
                    pos = row[k_index + 1].find_elements_by_css_selector('td')[d_index].\
                        find_element_by_css_selector('div>a').text
                except NoSuchElementException:
                    pos = '-'
                date_pos[date_list[d_index]] = pos
            keyword_statistic[k_list[k_index]] = date_pos
            print_log('Keywords statistic %s;' % keyword_statistic)
    print_log('Пагинация завершена, итоговый результат: ' % keyword_statistic)
    return keyword_statistic


def wait_until_element_present(css_locator, wait_time=10):
    def skip(wating_time):
        sleep(1)
        wating_time += 1
    global wd
    time = 0
    try:
        while (not wd.find_element_by_css_selector(css_locator).is_displayed()) and (time < wait_time):
            skip(time)
    except NoSuchElementException:
            skip(time)


def get_region_statistic():
    groups = {}
    try:
        g_list = get_combobox_options('group_id')[1:]
        print_log('Найдено групп %d' % len(g_list))
        d_list = get_info_list('td>span.date')
        print_log('Список дат %s' % d_list)
        for g_num in range(len(g_list)):
            print_log('Выбор группы %s' % g_list[g_num])
            Select(wd.find_element_by_name("group_id")).select_by_index(g_num + 1)
            wait_until_element_present('.up_position.min_width')
            print_log('Получение статистики группы %s' %g_num)
            k_w = get_group_statistic(d_list)
            print_log('Гет регион статистик: %s' % g_list[g_num])
            groups[g_list[g_num]] = k_w
            print_log('Получено: %s' % groups[g_list[g_num]])
        return groups
    except NoSuchElementException:
        print_log('No groups find')
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
        except NoSuchElementException:
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
        print_log('Анализ региона %s' % r_list[r_num])
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
    print_log('получение статистики по проекту %s' % site_url)
    project_statistics = {}
    se_stat = {}
    se_list = get_combobox_options("searcher")[:-2]
    print_log('se_list %s' % se_list)
    set_dates()
    se_full = ('Yandex', 'Google', 'go.Mail')
    se_short = ('Google.com', 'Yandex.com')
    reg_num = 0
    for index in range(len(se_list)):
        if (se_list[index] in se_full) or (se_list[index] in se_short):
            Select(wd.find_element_by_name("searcher")).select_by_index(index)
            if se_list[index] in se_full:
                se_stat[se_list[index]] = get_se_statistic()
                project_statistics[se_list[index]] = se_stat[se_list[index]]
            elif se_list[index] in se_short:
                domain = se_list[index][:-4]
                se_stat[se_list[index]] = get_se_statistic('87')
                project_statistics[domain]['87'] = se_stat[se_list[index]]['87']
            reg_num += 1
    project_statistics_with_url = dict()
    project_statistics_with_url[site_url] = project_statistics
    project_list[project_url] = project_statistics_with_url


def save_project_list(project_list, export_file_name):
    import json
    with open('%s.json' % export_file_name, 'w') as out_file:
        out_file.write(json.dumps(project_list, indent=2))


def get_user_project_list():
    global user_login, user_password
    full_info = dict()
    full_info['login'] = user_login
    full_info['password'] = user_password
    full_info['projects'] = get_projects_data()
    return full_info

debug = False
init_session(debug=debug)
login(user_login, user_password)
try:
    full_info = get_user_project_list()
    file_name = 'project_list_%s' % full_info['login']
    save_project_list(full_info, file_name)

    project_statistic = dict()
    for num in full_info['projects']:
        get_project_statistic(project_url=num, site_url=full_info['projects'][num], project_list=project_statistic)
    file_name = user_login
    save_project(project=project_statistic, export_file_name=file_name)
except NoSuchElementException:
    print_log('Element not found')
    wd.save_screenshot('Error.png')
finally:
    wd.close()

