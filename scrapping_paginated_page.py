import sys               # import sys package
old_path = sys.path[:]   # make a copy of the old paths
sys.path.pop(0)  
import bs4        # remove the first one (usually the local)
sys.path = old_path 
import bs4 as bs
import urllib.request
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy as np

start_time = time.time()
driver = webdriver.Chrome('C:/chromedriver.exe')




col1List = []
col2List = []
col3List = []
col4List = []
col5List = []
col6List = []
col7List = []
col8List = []
col9List = []

fcol1List = []
fcol2List = []
fcol3List = []
fcol4List = []
fcol5List = []

Case = True
counter = 0
wait = WebDriverWait(driver, 10)
driver.get("http://zakupki.gov.kg/popp/view/order/list.xhtml")
while Case:	
	counter += 1
	time.sleep(2)#delay time requests are sent so we don\'t get kicked by server

	

	initial_active_button = bs.BeautifulSoup(driver.page_source,"lxml").find("a", {"class": "ui-state-active"})
	print('Page__',initial_active_button.text,'__')

	selenium_opened_status_link_list = []
	soup_opened_status_link_list = []

	row = bs.BeautifulSoup(driver.page_source,"lxml").find_all('tr', {'role':'row'})
	# get soup_opened_status_link_list


	for tr in row:

		tr_list = []
		td = tr.find_all('td')
		for t in td:
			span = t.find_all('span')
			for s in span:
				s.extract()
			tr_list.append(t)


		def checker(given_word):
			if (given_word in tr_list[0].text.upper() or given_word in tr_list[1].text.upper() or given_word in tr_list[2].text.upper() or given_word in tr_list[3].text.upper() or given_word in tr_list[4].text.upper()):
				return True
			else:
				return False

		if len(tr_list)==9 and tr_list[8].find_all('a', {'class': 'order-status-opened'}):
			print('--here--')

		given_word = 'Товары'.upper()

		def soup_opened_status_link_list(page_source_x):
			soup_opened_status_link_list_x = []
			row_x = bs.BeautifulSoup(page_source_x,"lxml").find_all('tr', {'role':'row'})
			for tr_x in row_x:
				tr_list_x = []
				td_x = tr_x.find_all('td')
				for t_x in td_x:
					span_x = t_x.find_all('span')
					for s_x in span_x:
						s_x.extract()
					tr_list_x.append(t_x)
				if len(tr_list_x)==9 and tr_list_x[8].find_all('a', {'class': 'order-status-opened'}):
					soup_opened_status_link_list_x.append(tr_list_x[8].find_all('a', {'class': 'order-status-opened'}))
			return soup_opened_status_link_list_x

		# take a list of opend link
		if len(tr_list)==9 and tr_list[8].find_all('a', {'class': 'order-status-opened'}):
			# soup_opened_status_link_list(driver.page_source)
			soup_opened_status_link_list = soup_opened_status_link_list(driver.page_source)
			
		# take a list of opend link with selenium
		if driver.find_elements_by_xpath("//a[@class='order-status-opened']"):
			selenium_opened_status_link_list = [ a for a in driver.find_elements_by_xpath("//a[@class='order-status-opened']")]
			

		if len(tr_list)==9 and checker(given_word) and tr_list[8].find_all('a', {'class': 'order-status-opened'}) and (tr_list[0].text.replace('\n', '').replace('\t', '') not in col1List) and tr_list[8].find_all('a', {'class': 'order-status-opened'}) in soup_opened_status_link_list:
			print(True)
			number_of_opened_link = soup_opened_status_link_list.index(tr_list[8].find_all('a', {'class': 'order-status-opened'}))
			print(number_of_opened_link)
					
			datail_page = selenium_opened_status_link_list[number_of_opened_link]
			# element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(By.XPATH, "//a[@class='order-status-opened']"))
			
			
			while True:
				time.sleep(2)
				try:
					datail_page.click()
					break
				except:
					continue
			# col1List = []
			# col2List = []
			# col3List = []
			row_page = bs.BeautifulSoup(driver.page_source,"lxml").find_all('tr', {'role':'row'})
			print('Titel:           ____<____',tr_list[1].text,'___>___')
			for tr_page in row_page:
				tr_list_page = []
				td_page = tr_page.find_all('td')
				for t_page in td_page:
					tr_list_page.append(t_page)
				if len(tr_list_page) > 3:
					print('1-->',tr_list_page[1].text)
					# print('2>', tr_list_page[2])
					tr_page_detail_list = []
					td_page_detail_list = []
					for tr_page_detail in tr_list_page[2].find_all('tr'):
						tr_page_detail_list.append(tr_page_detail)

						for td_detail_page in tr_page_detail_list[0].find_all('td'):
							td_page_detail_list.append(td_detail_page)

						if len(td_page_detail_list) > 0:
							# for i in range(len(td_page_detail_list)):
							# 	print(i,'--)',td_page_detail_list[i-1].text)
							print('0--)', td_page_detail_list[0].text)
							print('1--)',td_page_detail_list[1].text)
							print('2--)',td_page_detail_list[2].text)
						# fcol1List.append(tr_list[0].text.replace('\n', '').replace('\t', ''))
						fcol2List.append(tr_list[1].text.replace('\n', '').replace('\t', ''))
						fcol3List.append(tr_list_page[1].text.replace('\n', '').replace('\t', ''))
						fcol4List.append(td_page_detail_list[0].text.replace('\n', '').replace('\t', ''))
						fcol5List.append(td_page_detail_list[2].text.replace('\n', '').replace('\t', ''))
			driver.back()
			# check in which pahe we stay
			print('Current page: __',bs.BeautifulSoup(driver.page_source,"lxml").find("a", {"class": "ui-state-active"}).text,'__')

		# print('q1')
		if len(tr_list) == 9 and (tr_list[0].text.replace('\n', '').replace('\t', '') not in col1List):
			col1List.append(tr_list[0].text.replace('\n', '').replace('\t', ''))
			col2List.append(tr_list[1].text.replace('\n', '').replace('\t', ''))
			col3List.append(tr_list[2].text.replace('\n', '').replace('\t', ''))
			col4List.append(tr_list[3].text.replace('\n', '').replace('\t', ''))
			col5List.append(tr_list[4].text.replace('\n', '').replace('\t', ''))
			col6List.append(tr_list[5].text.replace('\n', '').replace('\t', ''))
			col7List.append(tr_list[6].text.replace('\n', '').replace('\t', ''))
			col8List.append(tr_list[7].text.replace('\n', '').replace('\t', ''))
			col9List.append(tr_list[8].text.replace('\n', '').replace('\t', ''))

		# if len(tr_list)==9 and (tr_list[0].text.replace('\n', '').replace('\t', '') in col1List):
		# 	print('This one in the list')

	# if int(active_button.text) != 1 and int(active_button.text) > 1:
	# 	driver.find_element_by_xpath("//a[@aria-label='Page "+ str(active_button.text) + "']").click();
	# 	print('Back to page: __',active_button.text,'__')
		# print('q2')
		active_button = bs.BeautifulSoup(driver.page_source,"lxml").find("a", {"class": "ui-state-active"})
		if int(active_button.text) != int(initial_active_button.text) and int(active_button.text) > 0:
			print('Go from if ')
			Button_case = True
			while Button_case:
				time.sleep(2)
				print('Current page: __  ',bs.BeautifulSoup(driver.page_source,"lxml").find("a", {"class": "ui-state-active"}).text,'  __LooP')
				pages_list = [ int(page.text) for page in bs.BeautifulSoup(driver.page_source,"lxml").find_all('a', {'class', 'ui-paginator-page'}) ]
				print(pages_list)
				biggest_page = max(pages_list)
				active_button = bs.BeautifulSoup(driver.page_source,"lxml").find("a", {"class": "ui-state-active"})
				if int(initial_active_button.text) in pages_list:
					while True:
						time.sleep(2)
						try:
							# element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(By.XPATH, "//a[contains(@aria-label, 'Page %s')]" %(initial_active_button.text)))
							driver.find_element_by_xpath("//a[contains(@aria-label, 'Page %s')]" %(initial_active_button.text)).click()
							break
						except:
							continue
					print('Current page: __',bs.BeautifulSoup(driver.page_source,"lxml").find("a", {"class": "ui-state-active"}).text,'__1')
					pages_list = []
					Button_case = False
				else:
					while True:
						time.sleep(2)
						try:
							# element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(By.XPATH, "//a[contains(@aria-label, 'Page %s')]" %(biggest_page)))
							driver.find_element_by_xpath("//a[contains(@aria-label, 'Page %s')]" %(biggest_page)).click()
							break
						except:
							continue

					pages_list = []
					del biggest_page
					time.sleep(2)
					print('Get to page: __',initial_active_button.text,'__')
			time.sleep(2)
		# print('q3')
			# while initial_active_button.text == active_button.text:

			# driver.find_element_by_xpath("//a[contains(text(), '%s')]" %(initial_active_button.text)).click();
			# driver.find_element_by_xpath("//a[@class='ui-paginator-page'][text() = '%s')]" %(initial_active_button.text)).click();
			# driver.find_element_by_xpath("//a[contains(@aria-label, 'Page %s')]" %(initial_active_button.text)).click()
			# print('Back to page: __',initial_active_button.text,'__')
	# print('q4')
	selenium_opened_status_link_list = []
	soup_opened_status_link_list = []
	while True:
		time.sleep(2)
		try:
			driver.find_element_by_class_name("ui-paginator-next").click()
			break
		except:
			continue

	# driver.implicitly_wait(10)	
	# element = WebDriverWait(driver, 10).until((EC.element_to_be_clickable(By.XPATH, "//a[@class='ui-paginator-next']")))
		
	if counter == 20:
		Case = False

# df = pd.DataFrame()
# df['ID'] = pd.Series(col1List)
# df['НАИМЕНОВАНИЕ ОРГАНИЗАЦИИ'] = pd.Series(col2List)
# df['ВИД ЗАКУПОК'] = pd.Series(col3List)
# df['НАИМЕНОВАНИЕ ЗАКУПКИ'] = pd.Series(col4List)
# df['МЕТОД ЗАКУПОК'] = pd.Series(col5List)
# df['ПЛАНИРУЕМАЯ СУММА'] = pd.Series(col6List)
# df['ДАТА ОПУБЛИКОВАНИЯ'] = pd.Series(col7List)
# df['СРОК ПОДАЧИ КОНКУРСНЫХ ЗАЯВОК'] = pd.Series(col8List)
# df['Documentation'] = pd.Series(col9List)
# print(df)


df = pd.DataFrame()
# df['ID'] = pd.Series(fcol1List)
df['НАИМЕНОВАНИЕ ОРГАНИЗАЦИИ'] = pd.Series(fcol2List)
df['НАИМЕВОНИЕ УЧАСТНИКА'] = pd.Series(fcol3List)
df['НОМЕР ЛОТА'] = pd.Series(fcol4List)
df['ПРЕДЛОЖЕННАЯ ЦЕНА'] = pd.Series(fcol5List)
print(df)


arrays = [fcol2List, fcol3List, fcol4List, fcol5List]
tuples = list(zip(*arrays))
index = pd.MultiIndex.from_tuples(tuples, names=['НАИМЕНОВАНИЕ ОРГАНИЗАЦИИ', 'НАИМЕВОНИЕ УЧАСТНИКА', 'НОМЕР ЛОТА', 'ПРЕДЛОЖЕННАЯ ЦЕНА'])
s = pd.Series(index=index)
print(s)


writer = pd.ExcelWriter('output.xlsx')
df.to_excel(writer,'Sheet1')
s.to_excel(writer,'Sheet2')
writer.save()
# table = pd.pivot_table(df, index = 'НАИМЕНОВАНИЕ ОРГАНИЗАЦИИ')
# print(table)
print("--- Timer %s seconds ---" % (time.time() - start_time))