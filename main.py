# -*- coding: utf-8 -*-
import os
import Gen_data
import Gen_graphs

gd = Gen_data.Gen_data()
gg = Gen_graphs.Gen_graphs(gd)

filename_data = []

# １．【毎回変更する】実験データが格納されているフォルダ
zikken_path = "C:\\Users\\SAHARA-7\\workspace\\cal-prop-cea\\解析データ"

# ２．【毎回変更する】生成ファイルを格納するフォルダ
result_path = "C:\\Users\\SAHARA-7\\workspace\\cal-prop-cea\\実験結果"

graph_file_extension = ".png"
filename_result_ave = result_path + "\\result_ave.csv"
filename_result_all = result_path + "\\result_all"
filename_wavelogger = "auto$0.csv"

dirs = os.listdir(zikken_path)
print("読み込んだフォルダリストは以下です．")

for i in dirs:
    print(i)
    # print(zikken_path + '\\' + i + '\\' + filename_wavelogger)
    filename_data.append(zikken_path + "\\" + i + "\\" + filename_wavelogger)

for i in range(len(dirs)):
    print(" ")
    print("処理中のフォルダ：" + dirs[i])
    gd.gen_data(filename_data[i], filename_result_all, filename_result_ave, dirs[i])

    # グラフを作らない場合は，以下の関数をコメントアウトする．
    gg.gen_graphs(result_path, dirs[i], graph_file_extension)

    print("完了：" + dirs[i])
