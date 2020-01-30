import csv
import locale
import datetime
from urllib import request
from bs4 import BeautifulSoup

def extract_category():
    url = "https://www.amazon.co.jp/gp/bestsellers/"
    html = request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    main_category_indexs = soup.find_all("div", "zg_homeWidget")

    amazon_category_list = []
    for main_category_index in main_category_indexs:
        category_name = main_category_index.find("h3").get_text()
        category_url = main_category_index.find("a").attrs['href']
        amazon_category_list.append([category_name, category_url])

    return amazon_category_list

def save_csv(category_name, amazon_ranking_list):
    locale.setlocale(locale.LC_CTYPE, "Japanese_Japan.932")
    date_now = datetime.datetime.now()
    name = date_now.strftime('%Y年%m月%d日 %H時%M分 ') + category_name +  ".csv"
    with open(name, "w", encoding='shift_jis', errors="ignore") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(amazon_ranking_list)
    
def access_amazon():
    category_list = extract_category()
    for category_name, url in category_list:
        html = request.urlopen(url)
        soup = BeautifulSoup(html, "html.parser")
        main_item_indexs = soup.find_all("li", "zg-item-immersion")

        amazon_ranking_list = []
        for main_item_index in main_item_indexs:
            rank = main_item_index.find("span", "zg-badge-text").get_text()
            title = main_item_index.find("div", "p13n-sc-truncate").get_text().lstrip()
            item_urls = "https://www.amazon.co.jp" + main_item_index.find("a").attrs['href']
            amazon_ranking_list.append([rank, title, item_urls])

        save_csv(category_name, amazon_ranking_list)

def main():
    print("各カテゴリーのランキング上位50位の情報を抽出します。")
    access_amazon()

if __name__ == "__main__":
    main()

# 記事メモ
# 全てのカテゴリーについて自動でランキングを50位まで取得
