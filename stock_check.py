import csv

#data.cvsを読み込みモードで開く（UTF-8は日本語対応）
with open('data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)  #１行づつ「列名：値」の辞書形式で取得

    print('在庫切れの商品の一覧')  #出力の見出し
    print('------------------')

    #csvの各行を１行ずつ処理
    for row in reader:
        #stock列を整数に変換して「在庫数０」か判定/csvは文字列で読み込まれるためint()が必要
        print(row["item"], row["stock"])

        if int(row['stock']) == 0:
            print('在庫切れ：', row['item'])  #在庫切れの商品名を表示