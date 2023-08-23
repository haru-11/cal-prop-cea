# -*- coding: utf-8 -*-
##ブランチテスト
import os
import Gen_data
import Gen_graphs
import gen_gif

gd = Gen_data.Gen_data()
gg = Gen_graphs.Gen_graphs(gd)
g_gif = gen_gif.Gen_gif()

filename_data = []

# １．【毎回変更する】実験データが格納されているフォルダ
zikken_path = "C:\\Users\\SAHARA-7\\OneDrive - 東京都公立大学法人\\ドキュメント\\首都大\\M1研究\\FY2021実験\\211201_NM-12_一液式_ワイヤーカット影響確認試験\\解析データ"

# ２．【毎回変更する】生成ファイルを格納するフォルダ
result_path = "C:\\Users\\SAHARA-7\\OneDrive - 東京都公立大学法人\\ドキュメント\\首都大\\M1研究\\FY2021実験\\211201_NM-12_一液式_ワイヤーカット影響確認試験\\解析結果_新解析ソフト2"

# ３．一液式の場合は１を，二液式の場合は２を入れる．
sel_bm = 1

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

    #データ処理
    gd.gen_data(filename_data[i], filename_result_all, filename_result_ave, dirs[i], sel_bm)

    # 時系列グラフ生成
    gg.gen_graphs(result_path, dirs[i], graph_file_extension)
    
    print("完了：" + dirs[i])

#推進剤使用量系列グラフ生成
gg.gen_graphs_ave(result_path,filename_result_ave)

#図のgif画像生成
print("gif生成中")
for i in range(4):
    g_gif.gen_gif(result_path, dirs, i+1, 200)
print("gif生成完了")

#gg.gen_graphs_ave(result_path, dirs[i], graph_file_extension,filename_result_ave)