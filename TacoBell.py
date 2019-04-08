##########################
''' given input in dollars, return which items on the Taco Bell 
	menu I can afford, ordered by calorie count
'''

import pandas as pd 
import numpy as np 
import re 
import requests
from bs4 import BeautifulSoup
from tkinter import *

def tb_scrape(cat):
	url = f'https://www.tacobell.com/food/{cat}'
	resp = requests.get(url)
	soup = BeautifulSoup(resp.text, 'html.parser')
	fooditem = soup.find_all('div', attrs={'class': 'product-name'})
	foodcost = soup.find_all('div', attrs={'class': 'product-price'})
	foodcals = soup.find_all('div', attrs={'class': 'product-calorie'})

	templist = []
	for i in range(len(fooditem)):
		templist.append([cat, fooditem[i].text.split('>')[0].strip(), 
								   foodcost[i].text.split('>')[0].strip(),
						 		   foodcals[i].text.split('>')[0].strip()])

	return templist

if __name__=='__main__':
	money = input("How much you got?")

# 	url_main = 'https://www.tacobell.com/food'
# 	resp_main = requests.get(url_main)
# 	soup_main = BeautifulSoup(resp_main.text, 'html.parser')

# 	foodcat = soup_main.find_all('div', attrs={'class':'text'})

# 	cats = []
# 	for cat in foodcat:
# 		tempcat = cat.text.split('span')[0].strip().lower()
# 		cats.append(tempcat)

# 	frames = []
# 	for cat in cats:
# 		temp = tb_scrape(cat)
# 		frames.append(temp)

# 	frames2 = [item for sublist in frames for item in sublist]

# 	df = pd.DataFrame(frames2, columns = ['Category', 'Item', 'Cost', 'Cals'])
# 	df.to_csv('C:/Users/DMoney/Desktop/Programming/Python/3.4/TacoBell/menu.csv')

	df = pd.read_csv('C:/Users/DMoney/Desktop/Programming/Python/3.4/TacoBell/menu.csv', index_col = 0)
	categories = df.Category.drop_duplicates()
	afford = df[df.Cost.apply(lambda x: float(x.split('$')[1])) <= money].sort_values(by=['Cals'], ascending = False)

# GUI through tkinter
