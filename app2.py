import requests
from bs4 import BeautifulSoup
from flask import(
    Flask,
    redirect,
    render_template,
    request
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def get_home():
    if request.method == "POST":
        link = request.form.get("page_url",type=str)
        input_tag = request.form.get("input_tag",type=str)
        input_class = request.form.get("input_class",type=str)
        input_tag_title = request.form.get("input_tag_title",type=str)
        input_class_title = request.form.get("input_class_title",type=str)
        input_tag_price = request.form.get("input_tag_price",type=str)
        input_class_price = request.form.get("input_class_price",type=str)
        
        response = requests.get(link)
        status = response.status_code

        response_txt = requests.get(link).text
        soup = BeautifulSoup(response_txt, "lxml")
        main = soup.find(input_tag, class_=input_class)
        titles = main.find_all(input_tag_title, class_=input_class_title)
        prices = main.find_all(input_tag_price, class_=input_class_price)

        write_info(titles, prices)

        titles_txt = []
        prices_txt = []

        for i in range(len(titles)):
            titles_txt.append(titles[i].text)
            prices_txt.append(prices[i].text)

        avg_price = calculate_avg_price(prices)

        return render_template("index.html", titles_prices = zip(titles_txt, prices_txt), status = status, avg_price = avg_price)

    return render_template("index.html")


def write_info(titles, prices):
    with open("olx.txt", "w") as file:
        file.write("")
    for i in range(len(titles)):
        with open("olx.txt", "a", encoding="utf-8") as file:
            file.write(f"{titles[i].text}: {prices[i].text}\n")



def calculate_avg_price(prices):
    price_sum = 0
    quantity = len(prices)
    for i in prices:
        price = i.text
        price_num = ""
        for char in price:
            if char in "0123456789":
                price_num += char
        try:
            price_sum += int(price_num)
        except:
            quantity -= 1
    price_avg = round(price_sum / quantity)
    return price_avg



if __name__ == "__main__":
    app.run(debug=True)