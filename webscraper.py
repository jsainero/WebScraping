from distutils.log import error
import json
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup, NavigableString, Tag
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import re
from tqdm import tqdm

COUNTRY_HELP = """
this is the country helper
"""
SUBJECT_HELP = """
this is the subject helper
"""
URL = "https://genealogy.math.ndsu.nodak.edu/"


def get_search_content(driver, country, subject):
    # Clicar para la búsqueda avanzada en "Advanced Search"
    advance_search = driver.find_element(By.XPATH, '//a[@href="search.php"]')
    advance_search.click()
    if subject:
        subject_search = driver.find_element(
            By.XPATH, f'//option[@value="{subject}"]')
        subject_search.click()

    if country:
        country_search = driver.find_element(By.ID, 'country')
        country_search.send_keys(country)
    country_search.send_keys(Keys.ENTER)
    # time.sleep(20)
    return BeautifulSoup(driver.page_source, features="lxml")


def authors_ids(authors_searched):
    ids = []
    for author in authors_searched:
        link = author.find('a').get('href')
        id = re.search('id=(.*)', link).group(1)
        ids.append(id)
    return ids


def author_info(driver, id):
    # LECTURA DE LA PÁGINA
    driver.get(URL+"id.php?id="+id)
    soup = BeautifulSoup(driver.page_source, features="lxml")

    # WEB SCRAPING
    main_content = soup.find(id='mainContent')

    # author name
    # strip() remove spaces at the beginning and at the end of the string
    author_name = main_content.find('h2').get_text().strip()

    # university
    author_university = main_content.find_next(
        'span').find_next('span').get_text()

    # PHD publication year
    phd_year = main_content.find('span').get_text()
    phd_year = ''.join(re.findall(r"\d{4}$", phd_year))

    # Country
    if main_content.find('img'):
        author_country = main_content.find('img').get('title')
    else:
        author_country = ''

    for div in range(0, len(main_content.find_all('div'))):
        # PHD title
        if div == 3:
            phd_title = ''.join([i if type(i) == NavigableString else '' for i in main_content.find_all(
                'div')[3].contents[2].contents]).strip()
        # Subject
        if div == 4:
            try:
                phd_subject = main_content.find_all(
                    'div')[div].get_text().split(r":", 1)[1].strip()
            except:
                phd_subject = ''

    # Advisors
    advisor_text = re.search(r'Advisor.*', main_content.get_text())
    if advisor_text is not None:
        advisor_text = advisor_text.group(0)
        advisors_pre = re.split(r"No students known.", advisor_text)[0]
        advisors = re.split(r"Advisor: |Advisor \d: ", advisors_pre)[1:]
    else:
        advisors = []

    # Students
    students = []
    if main_content.table != None:
        students_searched = main_content.table.find_all('a')
        for stud in students_searched:
            students.append(stud.get_text())

    return {
        'name': author_name,
        'country': author_country,
        'university': author_university,
        'PHD title': phd_title,
        'year of publication': phd_year,
        'subject': phd_subject,
        'advisor': advisors,
        'students': students
    }


def main(country, subject):
    if args.country:
        print('country:', country)

    if args.subject:
        print('subject:', subject)

    options_chrome = webdriver.ChromeOptions()
    options_chrome.add_argument('--headless')
    driver = webdriver.Chrome(options=options_chrome)
    driver.get(URL)
    soup = get_search_content(driver, country, subject)

    main_content = soup.find(id='mainContent').table
    authors_searched = main_content.find_all('tr')
    ids = authors_ids(authors_searched)

    print(f'Your search has found {len(ids)} records in the database')
    i = 0
    authors_info = []
    for _ in tqdm(range(len(ids))):
        authors_info.append(author_info(driver, ids[i]))
        i += 1
        sleep(0.1)

    search_info = {
        'country': country,
        'subject': subject,
        'number_of_records': len(authors_info),
        'mathematicians': authors_info
    }

    with open('mathematicians_dataset.json', 'w') as file:
        json.dump(search_info, file, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--country", type=str, help=COUNTRY_HELP)
    parser.add_argument("--subject", type=str, help=SUBJECT_HELP)
    args = parser.parse_args()

    if args.country is not None or args.subject is not None:
        main(args.country, args.subject)
    else:
        error('At least one argument needed')
