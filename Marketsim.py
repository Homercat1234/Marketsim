import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
#from scipy.optimize import curve_fit
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys

def run_simulation(num_buyers, num_sellers, num_iterations):
    buyers = [[random.uniform(5, 60), 0] for i in range(num_buyers)]
    sellers = [[random.uniform(10, 40), 0] for i in range(num_sellers)]

    buyerorder = [-1 for i in range(len(buyers))]
    sellerorder = [-1 for i in range(len(buyers))]

    for i in range(num_iterations):
        for x in range(len(buyers)- 1):
            buyer_choice = random.choice(range(len(buyers) - 1))
            buyerorder[x] = buyer_choice

            seller_choice = random.choice(range(len(sellers) - 1))
            sellerorder[x] = seller_choice
        
        for x in range(len(buyers) - 1):
            buyer_qty = buyers[buyerorder[x]][1]
            seller_qty = sellers[sellerorder[x]][1]
        
            if buyers[buyerorder[x]][0] >= sellers[sellerorder[x]][0] and seller_qty > 0:
                sellers[sellerorder[x]][1] += 1
                if buyer_qty > 0:
                    buyers[buyerorder[x]][1] -= 1
                buyers[buyerorder[x]][0] = max(buyers[buyerorder[x]][0] - 0.1 * buyer_qty, 0)
                sellers[sellerorder[x]][0] = sellers[sellerorder[x]][0] + 0.1 * buyer_qty
            
            elif buyers[buyerorder[x]][0] < sellers[sellerorder[x]][0] and buyer_qty > 0:
                if seller_qty > 0:
                    buyers[buyerorder[x]][1] += 1
                    sellers[sellerorder[x]][1] -= 1
                buyers[buyerorder[x]][0] = buyers[buyerorder[x]][0] + 0.1 * seller_qty
                sellers[sellerorder[x]][0] = max(sellers[sellerorder[x]][0] - 0.1 * seller_qty, 0)

    sellerprice = [0 for i in range(len(sellers))]
    sellerx = [0 for i in range(len(sellers))]
    buyersprice = [0 for i in range(len(buyers))]
    buyerx = [0 for i in range(len(buyers))]

    for i in range (len(buyers)):
        buyersprice[i] = buyers[i][0]
        buyerx[i] = i

    for i in range (len(sellers)):
        sellerprice[i] = sellers[i][0]
        sellerx[i] = i

    return sellerx, sellerprice, buyerx, buyersprice 

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Market Simulation")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.num_buyers = tk.IntVar()
        self.num_buyers.set(100)
        self.num_sellers = tk.IntVar()
        self.num_sellers.set(100)
        self.num_iterations = tk.IntVar()
        self.num_iterations.set(100)

        self.num_buyers_str = tk.StringVar(value=str(self.num_buyers.get()))
        self.num_sellers_str = tk.StringVar(value=str(self.num_sellers.get()))
        self.num_iterations_str = tk.StringVar(value=str(self.num_iterations.get()))

        ttk.Label(self, text="Number of Buyers:", font=('Arial', 14)).grid(column=0, row=0, padx=10, pady=1)
        ttk.Scale(self, from_=1, to=500, variable=self.num_buyers, command=self.update_buyers_label).grid(column=1, row=0, pady=5)
        ttk.Label(self, textvariable=self.num_buyers_str, font=('Arial', 14)).grid(column=2, row=0, padx=10, pady=1)

        ttk.Label(self, text="Number of Sellers:", font=('Arial', 14)).grid(column=0, row=1, padx=10, pady=1)
        ttk.Scale(self, from_=1, to=500, variable=self.num_sellers, command=self.update_sellers_label).grid(column=1, row=1, pady=5)
        ttk.Label(self, textvariable=self.num_sellers_str, font=('Arial', 14)).grid(column=2, row=1, padx=10, pady=1)

        ttk.Label(self, text="Number of Iterations:", font=('Arial', 14)).grid(column=0, row=2, padx=10, pady=1)
        ttk.Scale(self, from_=1, to=500, variable=self.num_iterations, command=self.update_iterations_label).grid(column=1, row=2, pady=5)
        ttk.Label(self, textvariable=self.num_iterations_str, font=('Arial', 14)).grid(column=2, row=2, padx=10, pady=1)

        self.update_button = ttk.Button(self, text="Update", command=self.update_values)
        self.update_button.grid(column=0, row=3, columnspan=5, padx=5, pady=0, sticky="ew")

        # Create the figure and canvas
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        dpi = 100
        figsize = (screen_width / dpi, screen_height / dpi)
        self.fig, self.ax = plt.subplots(figsize=figsize, dpi=dpi)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(column=3, row=0, rowspan=3, padx=1, pady=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=2)

        self.update_values()

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            sys.exit()

    def update_buyers_label(self, value):
        self.num_buyers_str.set(str(int(float(value))))

    def update_sellers_label(self, value):
        self.num_sellers_str.set(str(int(float(value))))

    def update_iterations_label(self, value):
        self.num_iterations_str.set(str(int(float(value))))

    def update_values(self):
        num_buyers = self.num_buyers.get()
        num_sellers = self.num_sellers.get()
        num_iterations = self.num_iterations.get()
        
        self.num_buyers_str.set(str(num_buyers))
        self.num_sellers_str.set(str(num_sellers))
        
        sellerx, sellerprice, buyerx, buyersprice = run_simulation(num_buyers, num_sellers, num_iterations)

        sellerprice.sort()
        buyersprice.sort(reverse=True)

        p1 = np.polyfit(sellerx, sellerprice, 5)
        poly1d_fn1 = np.poly1d(p1)

        p2 = np.polyfit(buyerx, buyersprice, 5)
        poly1d_fn2 = np.poly1d(p2)

        self.ax.clear()
        self.ax.plot(np.array(sellerx), poly1d_fn1(sellerx), '-', label="Supply Curve", linewidth=2)
        self.ax.plot(np.array(buyerx), poly1d_fn2(buyerx), '-', label="Demand Curve", linewidth=2)
        self.ax.legend(loc="upper right")
        self.ax.set_title("Supply v Demand")
        self.ax.set_xlabel("Quantity")
        self.ax.set_ylabel("Price")
        self.fig.canvas.draw()

if __name__ == '__main__':
    app = App()
    app.mainloop()
