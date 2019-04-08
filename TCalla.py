##########################
''' given input in dollars, return which items on the Taco Bell 
	menu I can afford, ordered by calorie count
'''

import pandas as pd 
import numpy as np 
import re 
import requests
from bs4 import BeautifulSoup
import tkinter as tk


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


def tb_cats_scrape():
	url_main = 'https://www.tacobell.com/food'
	resp_main = requests.get(url_main)
	soup_main = BeautifulSoup(resp_main.text, 'html.parser')

	foodcat = soup_main.find_all('div', attrs={'class':'text'})

	cats = []
	for cat in foodcat:
		tempcat = cat.text.split('span')[0].strip().lower()
		cats.append(tempcat)

	frames = []
	for cat in cats:
		temp = tb_scrape(cat)
		frames.append(temp)

	frames2 = [item for sublist in frames for item in sublist]
	df = pd.DataFrame(frames2, columns = ['Category', 'Item', 'Cost', 'Cals'])
	return df


def ShowChoice():
	print(v.get())


def menu_filter(category):
	t.delete('1.0', tk.END)
	money = float(e1.get())
	afford = df[df.Cost.apply(lambda x: float(x.split('$')[1])) <= money].sort_values(by=['Cals'], ascending = False)
	display = afford[afford.Category == category].sort_values(by=['Cals'], ascending = False).head(25)
	t.insert(tk.END, (display[['Item', 'Cost', 'Cals']]))


def get_money():
	money = float(e1.get())
	afford = df[df.Cost.apply(lambda x: float(x.split('$')[1])) <= money].sort_values(by=['Cals'], ascending = False)

def search():
	t.delete('1.0', tk.END)
	text = SearchBox.get()
	t.insert(tk.END, df[df.Item.str.contains('(?i)'+text)])


# def add_to_order(selection):
# 	d = {}
# 	d[selection] = {selection.name: name,
# 					selection.cost: cost,
# 					selection.cals: cals}

# 	order[i_order] = d 
# 	i_order += 1

if __name__=='__main__':

# GUI through tkinter

	df = pd.read_csv('C:/Users/DMoney/Desktop/Programming/Python/3.4/tkinter_megaseries/menus/TacoBell/menu.csv', index_col = 0)
	categories = list(df.Category.drop_duplicates())
	money = 10.00
	order = {}
	i_order = 0


	root = tk.Tk()

	v = tk.IntVar()
	v.set(1)  
	options = ''

	e1 = tk.Entry(root)
	e1.insert(tk.END, '10')
	e1.pack()
	e1.focus_set()

	b1 = tk.Button(root, text = 'Update Money', command = lambda : get_money())
	b1.pack()

	b2 = tk.Button(root, text = 'Update Menu')
	b2.pack()

	tk.Label(root, 
	         text="""What do you want to eat?""",
	         justify = tk.LEFT,
	         padx = 20).pack()
	t = tk.Text(root)
	t.pack(side = tk.RIGHT)

	# tk.Label(root,
	# 		text = """Search""",
	# 		justify = tk.LEFT,
	# 		padx = 0).pack()
	# t2 = tk.Text(root)
	# t2.pack(side = tk.RIGHT)

	SearchBox = tk.Entry(root).pack()
	SearchButton = tk.Button(root, text = 'Search', command = lambda: search()).pack()

	for val, category in enumerate(categories):
	     tk.Radiobutton(root, 
	                  text=category.capitalize(),
	                  indicatoron = 0,
	                  width = 20,
	                  padx = 20, 
	                  variable=v, 
	                  command=lambda : menu_filter(categories[v.get()]),
	                  value=val).pack(anchor=tk.W)

	root.mainloop()
