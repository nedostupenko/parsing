from pprint import pprint
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from transliterate import translit

# https://hh.ru/search/vacancy?search_field=description&search_field=company_name&search_field=name&text=сантехник
# https://russia.superjob.ru/vakansii/santehnik.html?page=1

url_1 = 'https://hh.ru'
url_2 = 'https://russia.superjob.ru'

query_value = 'сантехник'

params_1 = {'search_field': 'description',
          'search_field': 'company_name',
          'search_field': 'name',
          'text': query_value,
          'items_on_page': 20,
          'page': 0}
params_2 = {'page': 1}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85'
                         ' YaBrowser/21.11.0.1996 Yowser/2.5 Safari/537.36'}

response_hh = requests.get(url_1 + '/search/vacancy', params=params_1, headers=headers)
dom_hh = BeautifulSoup(response_hh.text, 'html.parser')
vacancies_hh = dom_hh.find_all('div', {'class': 'vacancy-serp-item'})
pages_hh = dom_hh.find_all('span', {'class': 'pager-item-not-in-short-range'})[-1]
max_page_hh = int(pages_hh.find('span').getText())

response_sj = requests.get(url_2 + f'/vakansii/{translit(query_value, language_code="ru", reversed=True)}.html', headers=headers, params=params_2)
dom_sj = BeautifulSoup(response_sj.text, 'html.parser')
vacancies_sj = dom_sj.find_all('div', {'class': '_3eZwq iJCa5 f-test-vacancy-item _1fma_ _2nteL'})
pages_sj = dom_sj.find_all('span', {'class': '_3hkiy _30F5F _290uh _1tqyb _3PbQP _1AKho'})[-2]
max_page_sj = int(pages_sj.getText())

def page_scrapping_hh(vacancies, url):
    vacancies_list = []
    for vacancy in vacancies:
        vacancy_dict = {}
        link = vacancy.find('a', {'class': 'bloko-link'})['href']
        name = vacancy.find('a', {'class': 'bloko-link'}).getText()
        try:
            salary = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText().replace('\u202f', '')
        except:
            salary = None
            salary_up = None
            salary_to = None
            salary_currency = None

        if salary != None:
            salary = salary.split(' ')
            if salary[0] == 'от':
                salary_up = int(salary[1])
                salary_to = None
                salary_currency = salary[-1]
            elif salary[0] == 'до':
                 salary_up = None
                 salary_to = int(salary[1])
                 salary_currency = salary[-1]
            elif salary[0] == '':
                 salary_up = None
                 salary_to = None
                 salary_currency = salary[-1]
            else:
                 salary_up = int(salary[0])
                 salary_to = int(salary[2])
                 salary_currency = salary[-1]
        try:
            company = vacancy.find('a', {'class': 'bloko-link bloko-link_secondary'}).getText().replace('\xa0', ' ')
        except:
            company = None
        try:
            company_loc = vacancy.find('a', {'class': 'bloko-link bloko-link_secondary'}).parent.parent.nextSibling.getText()
        except:
            company_loc = None

        vacancy_dict['url'] = url
        vacancy_dict['link'] = link
        vacancy_dict['name'] = name
        # vacancy_dict['salary'] = salary
        vacancy_dict['salary_up'] = salary_up
        vacancy_dict['salary_to'] = salary_to
        vacancy_dict['salary_currency'] = salary_currency
        vacancy_dict['company'] = company
        vacancy_dict['company_loc'] = company_loc

        vacancies_list.append(vacancy_dict)

    return vacancies_list

def page_scrapping_sj(vacancies, url):
    vacancies_list = []
    for vacancy in vacancies:
        vacancy_dict = {}
        try:
            link = url + vacancy.find('a', {'class': 'icMQ_'})['href']
        except:
            link = None
        try:
            name = vacancy.find('a', {'class': 'icMQ_'}).getText()
        except:
            name = None
        try:
            salary = vacancy.find('span', {'class': '_2Wp8I'}).getText()
        except:
            salary = None
            salary_up = None
            salary_to = None
            salary_currency = None

        if salary != None:
            if salary[0:2] == 'от':
                # salary = salary[3:].replace('\xa0', '', 1).split('\xa0')
                salary_up = int(salary[3:].replace('\xa0', '', 1).split('\xa0')[0])
                salary_to = None
                salary_currency = salary[3:].replace('\xa0', '', 1).split('\xa0')[-1]
            elif salary[0:2] == 'до':
                # salary = salary[3:].replace('\xa0', '', 1).split('\xa0')
                salary_up = None
                salary_to = int(salary[3:].replace('\xa0', '', 1).split('\xa0')[0])
                salary_currency = salary[3:].replace('\xa0', '', 1).split('\xa0')[-1]
            elif salary == '':
                salary_up = None
                salary_to = None
                salary_currency = None
            elif salary == 'По договорённости':
                salary_up = None
                salary_to = None
                salary_currency = None
            else:
                try:
                    # salary = salary.replace('\xa0', '', 4).split('\xa0')
                    salary_up = int(salary.replace('\xa0', '', 4).split('\xa0')[0].split('—')[0])
                    salary_to = int(salary.replace('\xa0', '', 4).split('\xa0')[0].split('—')[1])
                    salary_currency = salary.replace('\xa0', '', 4).split('\xa0')[-1]
                except:
                    # salary = salary.replace('\xa0', '', 1).split('\xa0')
                    salary_up = int(salary.replace('\xa0', '', 1).split('\xa0')[0])
                    salary_to = int(salary.replace('\xa0', '', 1).split('\xa0')[0])
                    salary_currency = salary.replace('\xa0', '', 1).split('\xa0')[-1]
            try:
                company = vacancy.find_all('a', {'class': 'icMQ_'})[-1]
                company = company.getText()
            except:
                company = None
            try:
                company_loc = vacancy.find('span', {'class': 'f-test-text-company-item-location'}).getText().split('•')[1]
            except:
                company_loc = None

        vacancy_dict['url'] = url
        vacancy_dict['link'] = link
        vacancy_dict['name'] = name
        vacancy_dict['salary_up'] = salary_up
        vacancy_dict['salary_to'] = salary_to
        vacancy_dict['salary_currency'] = salary_currency
        vacancy_dict['company'] = company
        vacancy_dict['company_loc'] = company_loc

        vacancies_list.append(vacancy_dict)

    return vacancies_list

total_vacancies = []
for page in range(max_page_hh):
    params = {'search_field': 'description',
              'search_field': 'company_name',
              'search_field': 'name',
              'text': query_value,
              'items_on_page': 20,
              'page': page}
    response_hh = requests.get(url_1 + '/search/vacancy', params=params_1, headers=headers)
    dom_hh = BeautifulSoup(response_hh.text, 'html.parser')
    vacancies_hh = dom_hh.find_all('div', {'class': 'vacancy-serp-item'})
    total_vacancies += page_scrapping_hh(vacancies_hh, url_1)
    # time.sleep(1) # timeout

for page in range(1, max_page_sj):
    params_2 = {'page': page}
    response_sj = requests.get(url_2 + f'/vakansii/{translit(query_value, language_code="ru", reversed=True)}.html',
                               headers=headers, params=params_2)
    dom_sj = BeautifulSoup(response_sj.text, 'html.parser')
    vacancies_sj = dom_sj.find_all('div', {'class': '_3eZwq iJCa5 f-test-vacancy-item _1fma_ _2nteL'})
    total_vacancies += page_scrapping_sj(vacancies_sj, url_2)
    # time.sleep(1)  # timeout

df = pd.DataFrame(total_vacancies)
df.to_csv('total_vacancies.csv', sep=';')