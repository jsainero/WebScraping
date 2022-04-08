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
    You have to introduce a country name (Spain, France, United Kingdom...).
"""
SUBJECT_HELP = """
    You have to introduce one of these codes:

    00 - General
    01 - History and biography
    03 - Mathematical logic and foundations
    05 - Combinatorics
    06 - Order, lattices, ordered algebraic structures
    08 - General algebraic systems
    11 - Number theory
    12 - Field theory and polynomials
    13 - Commutative rings and algebras
    14 - Algebraic geometry
    15 - Linear and multilinear algebra; matrix theory
    16 - Associative rings and algebras
    17 - Nonassociative rings and algebras
    18 - Category theory, homological algebra
    19 - K-theory
    20 - Group theory and generalizations
    22 - Topological groups, Lie groups
    26 - Real functions
    28 - Measure and integration
    30 - Functions of a complex variable
    31 - Potential theory
    32 - Several complex variables and analytic spaces
    33 - Special functions
    34 - Ordinary differential equations
    35 - Partial differential equations
    37 - Dynamical systems and ergodic theory
    39 - Finite differences and functional equations
    40 - Sequences, series, summability
    41 - Approximations and expansions
    42 - Fourier analysis
    43 - Abstract harmonic analysis
    44 - Integral transforms, operational calculus
    45 - Integral equations
    46 - Functional analysis
    47 - Operator theory
    49 - Calculus of variations and optimal control
    51 - Geometry
    52 - Convex and discrete geometry
    53 - Differential geometry
    54 - General topology
    55 - Algebraic topology
    57 - Manifolds and cell complexes
    58 - Global analysis, analysis on manifolds
    60 - Probability theory and stochastic processes
    62 - Statistics
    65 - Numerical analysis
    68 - Computer science
    70 - Mechanics of particles and systems
    74 - Mechanics of deformable solids
    76 - Fluid mechanics
    78 - Optics, electromagnetic theory
    80 - Classical thermodynamics, heat transfer
    81 - Quantum Theory
    82 - Statistical mechanics, structure of matter
    83 - Relativity and gravitational theory
    85 - Astronomy and astrophysics
    86 - Geophysics
    90 - Operations research, mathematical programming
    91 - Game theory, economics, social and behavioral sciences
    92 - Biology and other natural sciences
    93 - Systems theory; control
    94 - Information and communication, circuits
    97 - Mathematics education
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
