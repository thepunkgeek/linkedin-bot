#####################################################################
#	A python LinkedIn bot that views users for you.					#
#																	#
#	Based on the code by YouTubube user: DrapsTV					#
#	From this video:https://www.youtube.com/watch?v=twRQNSFXiYs 	#
#																	#
#	Written using Tabs with a width of 4...							#
#####################################################################


import argparse, os, time
import urlparse, random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display #To run Firefox in a virtual display(headless)

display = Display(visible=0, size=(800,600))

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
				if '/jobs' in url and not 'profile_pic' or 'identity-name':
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
		time.sleep(random.uniform(10, 30))#Sleep to assure page loads, random to appear more human.
		page = BeautifulSoup(browser.page_source, 'html.parser')#added 'html.parser' to fix error
		people = getPeopleLinks(page)
		if people:
			for person in people:
				ID = getID(person)
				if ID not in visited:
					pList.append(person)
					visited[ID] = 1
					#print ID #uncomment to show all the raw IDs as they are scraped(for debugging)
		while pList: #if there's people to look at, then do
			person = pList.pop()
			browser.get(person)
			#print(person)
			count += 1
			print('[+] ' + browser.title[:-10] + ' was visited! (' + str(count) + '/' + str(len(pList))+ ') Visisted Queue')
			time.sleep(random.uniform(3, 10))#To appear human...
		else: #otherwise find people via the job pages
			jobs = getJobLinks(page)
			if jobs:
				job = random.choice(jobs)
			root = 'http://www.linkedin.com'
			roots = 'http:www.linkedin.com'
			if root not in job or roots not in job:
				job = 'https://www.linkedin.com' + job
				browser.get(job)
				print(job)
				time.sleep(random.uniform(3, 10))
			else:
				print("I'm Lost, Exiting...")
				print("LinkedIn may have caught on, and might be requiring proof that we're not a robot ;D")
				print("Try loggin in a few times manually, then run again... or don't run headless & watch browser")
				browser.quit()
				display.stop()
				break
		#Output make option for this
		print('[+] ' + browser.title + ' was visited! (' + str(count) + '/' + str(len(pList))+ ') Visisted Queue')
		#os.system('say "Boom"') #for OSX, and strictly for the lolz



def Main():
		parser = argparse.ArgumentParser()
		parser.add_argument('email', help = 'linkedin email')
		parser.add_argument('password', help = 'linkedin password')
		args = parser.parse_args()
		
		display.start()#To run Firefox in a virtual display(headless)
		browser = webdriver.Firefox()#changed from PhantomJS
		browser.get('https://www.linkedin.com/uas/login')

		emailElement = browser.find_element_by_id('session_key-login')
		emailElement.send_keys(args.email)
		passElement = browser.find_element_by_id('session_password-login')
		passElement.send_keys(args.password)
		passElement.submit()

		os.system('clear')
		print('[+] Success! Logged In, Bot Is Starting!')
		#os.system('say "logged in, bot is starting!"')#for OSX, and strictly for the lolz
		#time.sleep(5)
		ViewBot(browser)


if __name__ == '__main__':
	Main()
