#################################################################
#A python LinkedIn bot that views users for you.                #
#                                                               #
#Based on the code by YouTubube user: DrapsTV                   #
#From this video: https://www.youtube.com/watch?v=twRQNSFXiYs   #
#################################################################


import argparse, os, time
import urlparse, random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def getPeopleLinks(page):
    links = []
    for link in page.find_all('a'):
        url = link.get('href')
        if url:
            if 'profile/view?id=' in url:
                    links.append(url)
    return links

def getJobLinks(page):
    links = []
    for link in page.find_all('a'):
        url = link.get('href')
        if url:
                if '/jobs' in url:
                    links.append(url)
    return links

def getID(url):
    pUrl = urlparse.urlparse(url)
    return urlparse.parse_qs(pUrl.query)['id'][0]

def ViewBot(browser):
    visited = {}
    pList = []
    count = 0
    while True:
        #Sleep to make sure everything loads.
        #add random to make us look human.
        time.sleep(random.uniform(5, 10))
        page = BeautifulSoup(browser.page_source, 'html.parser')#added "html.parser to fix error"
        people = getPeopleLinks(page)
        if people:
            for person in people:
                ID = getID(person)
                if ID not in visited:
                    pList.append(person)
                    visited[ID] = 1
                    print ID
        if pList: #if there's people to look at, then do
            person = pList.pop()
            browser.get(person)
            count += 1
        else: #otherwise find people via the job pages
            jobs = getJobLinks(page)
            if jobs:
                job = random, choice(jobs)
                root = 'http://www.linkedin.com'
                roots = 'http:www.linkedin.com'
                if root not in job or roots not in job:
                    job = 'https://www.linkedin.com'+job
                browser.get(job)
            else:
                print "I'm Lost, Exiting..." #switched to "" because it looks cleaner in this context
                break
            #Output make option for this
        print '[+] ' + browser.title + 'Visited! \n(' + str(count) + '/' + str(len(pList))+ ') VisistedQueue'


def Main():
        parser = argparse.ArgumentParser()
        parser.add_argument('email', help = 'linkedin email')
        parser.add_argument('password', help = 'linkedin password')
        args = parser.parse_args()

        browser = webdriver.PhantomJS()#changed from Firefox
        browser.get('https://www.linkedin.com/uas/login')

        emailElement = browser.find_element_by_id('session_key-login')
        emailElement.send_keys(args.email)
        passElement = browser.find_element_by_id('session_password-login')
        passElement.send_keys(args.password)
        passElement.submit()

        os.system('clear')
        print '[+] Success! Logged In, Bot Starting!'
        ViewBot(browser)


if __name__ == '__main__':
    Main()
