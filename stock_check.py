import csv
import sys #コマンドライン引数を引き受けるため

OUTPUT_FILE ='stock_result.csv'  #在庫チェックの結果を書き出すCSVファイル

LOW_STOCK_THRESHOLD = 5  #在庫が少ないと判断する基準

#コマンドラインから、しきい値を変更できるようにする
if len(sys.argv) >1:
        LOW_STOCK_THRESHOLD = int(sys.argv[1])

#data.cvsを読み込みモードで開く（utf-8は日本語対応）
with open('data.csv', 'r', encoding='utf-8') as f:

    out_of_stock = []  # 在庫切れ商品を保存するリスト
    low_stock = []     # 在庫が少ない商品を保存するリスト
    supplier_summary_rows = []  #csvに出力する仕入先ごとの集計結果を保存

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
        if int(row['stock']) <=LOW_STOCK_THRESHOLD:  #sctokは文字列で読み込まれるため数値比較のためintに変換
            print('在庫少：', row['item'], row['stock'], '/仕入先：', row['supplier'])
            low_stock.append(row)  #csv書き出し用にデータを保存
    
    print('仕入先ごとの要補充件数')
    print('------------------')   

    supplier_count = {}  #仕入先事の件数を集計する辞書

    #在庫少リストを使って、仕入先ごとの件数を数える
    for row in low_stock:
        supplier = row['supplier']
    
        #まだ辞書にない仕入先は０件で初期化する
        if supplier not in supplier_count:
            supplier_count[supplier] = 0
    
        supplier_count[supplier] += 1    #1件追加する

    total = sum(supplier_count.values())  #SUM()で仕入れ数合計　.values()で件数だけ取り出す

    #集計結果を表示する
    for supplier, count in sorted(supplier_count.items(), key=lambda X: X[1], reverse=True): #件数を多い順にソート
        print(f'仕入先：{supplier} → {count}件')
        supplier_summary_rows.append(['仕入先集計', supplier, count])  #csv出力用に１行ずつ保存する
    
    print("------------------")
    print(f"合計：{total}件")

with open(OUTPUT_FILE, 'w', encoding='cp932', newline='')as f:  #在庫チェック結果をCSVに書き出す cp932はExcelで見れる
    writer = csv.writer(f)

    writer.writerow(['種類', '商品名', '在庫数', '仕入先'])  #ヘッダーの行

    for row in out_of_stock:  #在庫切れ
        writer.writerow(['在庫切れ', row['item'], row['stock'], row['supplier']])

    for row in low_stock:  #在庫少
        writer.writerow(['在庫少', row['item'], row['stock'], row['supplier']])

    writer.writerow(['合計',total])