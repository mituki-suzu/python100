import csv
import locale
import datetime
from urllib import request
from bs4 import BeautifulSoup

def save_csv(amazon_ranking_list):
    locale.setlocale(locale.LC_CTYPE, "Japanese_Japan.932")
    date_now = datetime.datetime.now()
    name = date_now.strftime('%Y年%m月%d日 %H時%M分') + ".csv"
    with open(name, "w", encoding='shift_jis', errors="ignore") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(amazon_ranking_list)
    
def access_amazon():
    url = 'https://www.amazon.co.jp/gp/bestsellers/electronics/'\
        'ref=zg_bs_electronics_home_all?pf_rd_p='\
        'fd07610d-cd90-4456-add0-20bd73a998a5&pf_rd_s=center-3&pf_rd_t=2101&pf_rd_i'\
        '=home&pf_rd_m=AN1VRQENFRJN5&pf_rd_r=K8BJBDBFCPPWP2ZRE5D9&pf_rd_r='\
        'K8BJBDBFCPPWP2ZRE5D9&pf_rd_p=fd07610d-cd90-4456-add0-20bd73a998a5'

    html = request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    main_item_indexs = soup.find_all("li", "zg-item-immersion")

    amazon_ranking_list = []

    for main_item_index in main_item_indexs:
        rank = main_item_index.find("span", "zg-badge-text").get_text()
        title = main_item_index.find("div", "p13n-sc-truncate p13n-sc-line-clamp-2").get_text().lstrip()
        item_urls = "https://www.amazon.co.jp" + main_item_index.find("a").attrs['href']
        amazon_ranking_list.append([rank, title, item_urls])

    save_csv(amazon_ranking_list)

def main():
    access_amazon()

if __name__ == "__main__":
    main()\

# 記事メモ
# bs4,urllib インストール
# find, find_all 使い方（詰まった話）
# get_textをするのとしないのと
# attrsについて
# titleの頭の空白を消す
# リストに追加の話 
# 上級編（アドな話）
# リアルタイムに時間を取得して1名前を変更する
# UnicodeEncodeError: 'locale' codec can't encode character '\u5e74' in position 2: encoding error

# 出たエラー
# find, find_all入れ子できないエラー
# AttributeError: ResultSet object has no attribute 'find_all'. You're probably treating a list of items like a single item. Did you call find_all() when you meant to call find()?
# shift_jisじゃないと文字化けするけど特殊文字今回は🄬ない案件
# UnicodeEncodeError: 'shift_jis' codec can't encode character '\xae' in position 112: illegal multibyte sequence
