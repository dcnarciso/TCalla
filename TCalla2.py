import tkinter as tk
from tkinter import ttk

import pandas as pd 
import numpy as np 
import math

LARGE_FONT= ("Verdana", 12)

df_cart = pd.DataFrame()


class TCalA(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, "./taco-16.ico")
        tk.Tk.wm_title(self, "TCalA")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff = 0)
        filemenu.add_command(label="Save settings")

        self.frames = {}

        for F in (StartPage,
                  MenuPage,
                  CartPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()



# def qf(quickPrint):
#     print(quickPrint)
        
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text=("""Taco Calorie Application
            """), font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Cart Page",
                            command=lambda: controller.show_frame(CartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Menu Page",
                            command = lambda: controller.show_frame(MenuPage))
        button2.pack()


class CartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=("""Cart Page
            """), font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text = "To Menu",
                            command = lambda: controller.show_frame(MenuPage))
        button2.pack()

        button3 = ttk.Button(self, text = "Refresh Cart",
                             command = lambda: [self.t.delete('1.0', tk.END), 
                                                self.t.insert(tk.END, (df_cart[['Item', 'Cost', 'Cals']])),
                                                self.t.insert(tk.END, "\n"),
                                                self.t.insert(tk.END, ("--------------------------------\n")),
                                                self.t.insert(tk.END, ("Total Cost: $" + str(
                                                    math.ceil((
                                                        sum(
                                                            list(df_cart.floatCost))*1.07) * 100)/100)))
                                                ])

        button3.pack()

        button4 = ttk.Button(self, text = "-",
                             command = lambda: self.remove_from_cart(self.e2.get()))
        button4.pack(side = tk.RIGHT)

        button5 = ttk.Button(self, text = "+", 
                             command = lambda: self.add_to_cart(self.e2.get()))
        button5.pack(side = tk.RIGHT)

        self.e2 = tk.Entry(self)
        self.e2.insert(tk.END, '')
        self.e2.pack(side = tk.RIGHT)

        tk.Label(self, 
                 text="""What you want to eat.""",
                 justify = tk.LEFT,
                 padx = 20).pack()
        self.t = tk.Text(self)
        self.t.place(relx = .5, rely = 0.5, anchor = tk.CENTER)

    # def show_cart(self):
    #     self.t.delete('1.0', tk.END)
    #     self.t.insert(tk.END, (df_cart[['Item', 'Cost', 'Cals']]))

    def add_to_cart(self, x):
        global df_cart
        df_cart = df_cart.append(df[df.index == int(x)])

    def remove_from_cart(self, x):
        global df_cart
        df_cart = df_cart.drop(int(x), axis = 0)

class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=("""Menu Page
            """), font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command = lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text = "To Cart",
                            command = lambda: controller.show_frame(CartPage))
        button2.pack()

        button3 = ttk.Button(self, text = "-",
                             command = lambda: self.remove_from_cart(self.e2.get()))
        button3.pack(side = tk.RIGHT)

        button4 = ttk.Button(self, text = "+", 
                             command = lambda: self.add_to_cart(self.e2.get()))
        button4.pack(side = tk.RIGHT)

        v = tk.IntVar()
        v.set(1)

        self.e1 = tk.Entry(self)
        self.e1.insert(tk.END, '')
        self.e1.pack()
        self.e1.focus_set()

        self.e2 = tk.Entry(self)
        self.e2.insert(tk.END, '')
        self.e2.pack(side = tk.RIGHT)

        tk.Label(self, 
                 text="""What do you want to eat?""",
                 justify = tk.LEFT,
                 padx = 20).pack()
        self.t = tk.Text(self)
        self.t.place(relx = .5, rely = 0.5, anchor = tk.CENTER)

        for val, category in enumerate(categories):
             tk.Radiobutton(self, 
                          text=category.capitalize(),
                          indicatoron = 0,
                          width = 20,
                          padx = 20, 
                          variable=v, 
                          command=lambda : self.menu_filter(categories[v.get()]),
                          value=val).pack(anchor=tk.W)

    def menu_filter(self, category):
        self.t.delete('1.0', tk.END)
        money = float(self.e1.get())
        afford = df[df.Cost.apply(lambda x: float(x.split('$')[1])) <= money].sort_values(by=['Cals'], ascending = False)
        display = afford[afford.Category == category].sort_values(by=['Cals'], ascending = False).head(25)
        self.t.insert(tk.END, (display[['Item', 'Cost', 'Cals']]))

    def add_to_cart(self, x):
        global df_cart
        df_cart = df_cart.append(df[df.index == int(x)])

    def remove_from_cart(self, x):
        global df_cart
        df_cart = df_cart.drop(int(x), axis = 0)


if __name__ == '__main__':
    df = pd.read_csv('./menu.csv', index_col = 0)
    df['floatCost'] = df.Cost.apply(lambda x: x.split('$')[1]).apply(float)
    categories = list(df.Category.drop_duplicates())



    app = TCalA()
    app.geometry("1280x720")
    app.mainloop()

    #C:/Users/DMoney/Desktop/Programming/Python/3.4/tkinter_megaseries/menus/TacoBell