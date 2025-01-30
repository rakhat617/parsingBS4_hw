import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox

def parse():
    response_txt = requests.get(link).text
    soup = BeautifulSoup(response_txt, "lxml")

    input_tag = entry_tag.get()
    input_class = entry_class.get()
    input_tag_title = entry_tag_title.get()
    input_class_title = entry_class_title.get()
    input_tag_price = entry_tag_price.get()
    input_class_price = entry_class_price.get()

    main = soup.find(input_tag, class_=input_class)

    titles = main.find_all(input_tag_title, class_=input_class_title)
    prices = main.find_all(input_tag_price, class_=input_class_price)
    return titles, prices


def write_info():
    [titles, prices] = parse()

    for i in range(len(titles)):
        with open("olx.txt", "a", encoding="utf-8") as file:
            file.write(f"{titles[i].text}: {prices[i].text}\n")

def check_status():
    response = requests.get(link)

    status = response.status_code

    messagebox.showinfo("Request status code", f"Status: {status}")

def calculate_avg_price():
    prices = parse()[1]
    price_sum = 0
    for i in prices:
        price = i.text
        price_num = ""
        for char in price:
            if char in "0123456789":
                price_num += char
        price_sum += int(price_num)
    price_avg = round(price_sum / len(prices))
    messagebox.showinfo("Average price", f"Average price: {price_avg}")

link = "https://www.olx.kz/elektronika/igry-i-igrovye-pristavki/pristavki/karaganda/?search%5Bfilter_enum_console_manufacturers%5D%5B0%5D=2272"

root = tk.Tk()

root.title("Window")
root.geometry("600x600")

label_tag = tk.Label(text="Enter tag name")
label_tag.pack()

entry_tag = tk.Entry()
entry_tag.pack()

label_class = tk.Label(text="Enter its class")
label_class.pack()

entry_class = tk.Entry()
entry_class.pack()

label_tag_title = tk.Label(text="Enter title tag")
label_tag_title.pack()

entry_tag_title = tk.Entry()
entry_tag_title.pack()

label_class_title = tk.Label(text="Enter title class")
label_class_title.pack()

entry_class_title = tk.Entry()
entry_class_title.pack()

label_tag_price = tk.Label(text="Enter price tag")
label_tag_price.pack()

entry_tag_price = tk.Entry()
entry_tag_price.pack()

label_class_price = tk.Label(text="Enter price class")
label_class_price.pack()

entry_class_price = tk.Entry()
entry_class_price.pack()

btn_check = tk.Button(text="Check request", command=check_status)
btn_check.pack()

btn_parse = tk.Button(text="Get info", command=write_info)
btn_parse.pack()

btn_avg = tk.Button(text="Calculate average price", command=calculate_avg_price)
btn_avg.pack()




root.mainloop()