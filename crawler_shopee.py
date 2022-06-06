import requests as req
import json, sqlite3, csv
#%%
# request is "search_items?by=relevancy..."
# ?by = relevancy綜合排名 sale最熱銷 ctime最新

def crawler_shopee(keywordStr, limitNum):
    url = "https://shopee.tw/api/v4/search/search_items?by=sale&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"
    keyword = "&keyword=" + keywordStr # 查詢關鍵字
    limit = "&limit=" + limitNum # 更改limit可以調整搜尋數量，最多100筆
    
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    }
    
    response = req.get(url + keyword + limit, headers= headers)
    response.encoding = "utf-8"
    roots = json.loads(response.text)
    
    print("success crawler.")
    return roots

def data_arrange(roots):
    data = []
    flag = 0
    for i in range(len(roots["items"])):
        data.append([])
        data[i].append(roots["items"][i]["item_basic"]["name"]) # 商品標題
        data[i].append(roots["items"][i]["item_basic"]["price"] / 100000) # 商品價錢
        data[i].append(roots["items"][i]["item_basic"]["historical_sold"]) # 銷售量
        data[i].append(roots["items"][i]["item_basic"]["item_rating"]["rating_count"][5]) # 總評論數
        flag += 1
    print("success arrange.")
    return data

def csv_outfile(data):    
    with open("database.csv", "w", newline = "", encoding="utf-8") as outfile:
        w = csv.writer(outfile, delimiter =",")
        for i in range(len(data)):
            w.writerow(data[i])
    print ("success outfile.")
#%%
roots = crawler_shopee("襪子", "60")
data = data_arrange(roots)
csv_outfile(data)

#%% 資料庫
conn = sqlite3.connect("database.db")
cur = conn.cursor()
cur.execute('''CREATE TABLE shopee
                (
                  No INTEGER,   
                  Item TEXT,
                  Price INTEGER,
                  Sold INTEGER,
                  Rating INTEGER,
                  PRIMARY KEY("No" AUTOINCREMENT)
                    );''')
conn.commit()

sql = "INSERT INTO shopee VALUES (NULL, ?, ?, ?, ?)"

flag = 0
for i in range(len(data)):
    cur.execute(sql, data[i])
    flag += 1

conn.commit()
print("success database:", flag)    

conn.close()

