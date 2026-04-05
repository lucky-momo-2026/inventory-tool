import csv

OUTPUT_FILE ='stock_result.csv'  #在庫チェックの結果を書き出すCSVファイル

#data.cvsを読み込みモードで開く（UTF-8は日本語対応）
with open('data.csv', 'r', encoding='utf-8') as f:

    out_of_stock = []  # 在庫切れ商品を保存するリスト
    low_stock = []     # 在庫が少ない商品を保存するリスト

    rows = list(csv.DictReader(f))  

    print('在庫切れの商品の一覧')  #出力の見出し
    print('------------------')

    #csvの各行を１行ずつ処理
    for row in rows:
        #stock列を整数に変換して「在庫数０」か判定/csvは文字列で読み込まれるためint()が必要
        if int(row['stock']) == 0:
            print('在庫切れ：', row['item'], '/仕入れ先：', row['supplier'])  #在庫切れの商品名と仕入先を表示
            out_of_stock.append(row) #csv書き出し用にデータを保存

    print('在庫が少ない商品の一覧')
    print('------------------')

    #在庫が少ない商品（５以下）を確認するためにループ
    for row in rows:
        if int(row['stock']) <=5:  #sctokは文字列で読み込まれるため数値比較のためintに変換
            print('在庫少：', row['item'], row['stock'], '/仕入先：', row['supplier'])
            low_stock.append(row)  #csv書き出し用にデータを保存

with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='')as f:  #在庫チェック結果をCSVに書き出す
    writer = csv.writer(f)

    writer.writerow(['種類', '商品名', '在庫数', '仕入先'])  #ヘッダーの行

    for row in out_of_stock:  #在庫切れ
        writer.writerow(['在庫切れ', row['item'], row['stock'], row['supplier']])

    for row in low_stock:  #在庫少
        writer.writerow(['在庫少', row['item'], row['stock'], row['supplier']])