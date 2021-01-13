"""Crawler script."""
import random
from collections import defaultdict
from random import choice
from time import time

import pandas as pd
from bs4 import BeautifulSoup
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.proxy import Proxy, ProxyType
from tqdm import tqdm

from src import PROJECT_PATHS

FIRST_DAY = 2500
LAST_DAY = 3001
MAX_PAGES = 111  # max amount of pages for one day to be crawled
RANDOM_SEED = 137

with open(f"{PROJECT_PATHS.configs}/crawl_utils/firefox.txt") as file_:
    agents = [x.replace('\n', '') for x in file_.readlines()]


def get_webdriver(ip_proxy, agent):
    """Create webdriver for selenium.

    Webdriver with new proxy and user-agent allows you
    to introduce yourself to the webpage as completely
    new user and hence you won't be blocked.

    Args:
        ip_proxy (str): https proxy ip:port without password.
        agent (str): Firefox user-agent.

    Returns:
        selenium.webdriver: webdriver with embedded proxy and user-agent
    """
    prox = Proxy()
    prox.proxy_type = ProxyType.MANUAL
    prox.http_proxy = ip_proxy

    capabilities = webdriver.DesiredCapabilities.FIREFOX
    prox.add_to_capabilities(capabilities)

    profile = webdriver.FirefoxProfile()
    profile.accept_untrusted_certs = True
    profile.set_preference("general.useragent.override", agent)

    return webdriver.Firefox(firefox_profile=profile, desired_capabilities=capabilities)


req_proxy = RequestProxy()
proxies = req_proxy.get_proxy_list()

random.seed(RANDOM_SEED)

driver = get_webdriver(choice(proxies).get_address(), choice(agents))
stories = defaultdict(list)

for date in tqdm(range(FIRST_DAY, LAST_DAY)):
    # we should iterate over pages for each date
    # average day contains approximately less than 100 pages
    # 10-14 stories per page, about 600 stories per day
    for page_i in range(1, MAX_PAGES):
        try:
            url = f"https://pikabu.ru/tag/%D0%A2%D0%B5%D0%BA%D1%81%D1%82?n=2&d={date}&D={date}&page={page_i}"
            driver.get(url)
            bs_page = BeautifulSoup(driver.page_source)
            page = bs_page.find_all(attrs={'class': 'story'})
            if not page:
                # skip if we reach end of day or get empty page
                break
            for story in page:
                try:
                    TITLE = story.find(attrs={'class': 'story__title'}).text
                    LIKES = story.find(attrs={'class': 'story__rating-count'}).text
                    TEXT = story.find(attrs={'class': 'story__content-inner'}).text
                    TAGS = "|".join(
                        [x.text for x in story.find_all(attrs={'class': 'tags__tag'})])
                    try:
                        COMMENTS = story.find(attrs={
                            'class': 'story__comments-link-count'
                        }).text
                    except AttributeError:
                        # thera are no comments for some ads
                        COMMENTS = -1

                    try:
                        VIEWS = story.find(attrs={
                            'class': 'story__views'
                        }).attrs.get('aria-label', 'NO_VIEWS').replace("\xa0",
                                                                       '').split()[0]
                    except AttributeError:
                        # there is no views counter for old stories
                        VIEWS = None

                    NICKNAME = story.find(attrs={'class': 'user__nick'}).text
                    TIME_GAP = story.find('time').text
                    TIMESTAMP = story.find('time').attrs['datetime']
                    CURRENT_TIMESTAMP = time()

                    stories['TITLE'].append(TITLE)
                    stories['LIKES'].append(LIKES)
                    stories['TEXT'].append(TEXT)
                    stories['TAGS'].append(TAGS)
                    stories['COMMENTS'].append(COMMENTS)

                    stories['VIEWS'].append(VIEWS)

                    stories['NICKNAME'].append(NICKNAME)
                    stories['TIME_GAP'].append(TIME_GAP)
                    stories['TIMESTAMP'].append(TIMESTAMP)
                    stories['CURRENT_TIMESTAMP'].append(CURRENT_TIMESTAMP)
                except AttributeError:
                    # skip if we reached ad block of page
                    pass
        except (TimeoutException, WebDriverException):
            # sometimes server losts connection and TimeoutException is raised
            # sometimes proxy comes with required password
            # and WebDriverExceprion is rased
            continue

    # safe each day for a separate csv
    df = pd.DataFrame(stories)
    df.to_csv(PROJECT_PATHS.data / "raw" / f"date_{date}.csv")
    del (df)
    stories = defaultdict(list)

    driver.close()
    driver = get_webdriver(choice(proxies).get_address(), choice(agents))
