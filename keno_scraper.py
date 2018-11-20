'''
	scraper.py
	
	Author: Michael Mallar
	Date created:  10/26/2018
	Date last modified: 11/19/2018
	Python version: 3.6.6
	OS: Ubuntu 18.04
	To Run: python3 keno_scraper
	Prereqs: numpy, pandas, beautiful soup, chrome, chromedriver
		- chrome driver install (Steps 1-3): https://tecadmin.net/setup-selenium-chromedriver-on-ubuntu/ 
		
'''

import os
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def scrape(url):
	# Adjust the path to where you installed chromedriver (might be /usr/bin/chromedriver)
	chromedriver_path = "/usr/local/bin/chromedriver"
	os.environ["webdriver.chrome.driver"] = chromedriver_path
	chrome_options = Options()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome(executable_path=r'/usr/local/bin/chromedriver',chrome_options=chrome_options)	
	driver.get(url)
	try:
		# Wait until the table is loaded 
		keno_table = WebDriverWait(driver,20).until(
			EC.presence_of_element_located((By.XPATH,"//*[@id='target-area']"))
		)
		
		print("Table Loaded...")
		
		# Wait until the elements are loaded 
		table_elements = WebDriverWait(driver,20).until(
			EC.presence_of_element_located((By.XPATH,"//*[@id='target-area']/tr[2]"))
		)
		print("Table Elements loaded...")
	except:
		print("Request Timed Out")
	finally:
		print("Gathering Data...")
		table = driver.find_element_by_xpath("//*[@id='main-content']/div/div[4]/div")
		table_html = table.get_attribute('innerHTML')
		soup = BeautifulSoup(table_html)
		table = soup.findChildren('table')[0]
		tbody = table.findChildren('tbody')[0]
		trs = tbody.findChildren('tr')
		rtn_list = []
		for row in trs:
			tds_list = []
			tds = row.findChildren('td')
			for elem in tds:
				tds_list.append(elem.text)
			rtn_list.append(tds_list)
		print(rtn_list)
		print("Data Gathered")
		driver.quit()

if __name__ == '__main__':
	# Change the date param to get data from another timeframe
	scrape('https://www.masslottery.com/games/lottery/search/results-history.html?game_id=15&mode=2&selected_date=2018-11-18')	
