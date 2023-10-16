# -*- coding: utf-8 -*-
##ブランチテスト
import os
import Gen_data
import Gen_graphs
import gen_gif

from tkinter import filedialog

gd = Gen_data.Gen_data()
gg = Gen_graphs.Gen_graphs(gd)
g_gif = gen_gif.Gen_gif()

filename_data = []



#確認・変更すること

#1. 実験データが格納されているフォルダ名
data_dir = '生データ'

#2. 解析結果を格納するために生成するフォルダ名
result_dir = '解析結果'

#3. 実験結果があるエクセルのcsvファイル名
data_filename = 'MB$0'

#4. 推進系のモード（一液式は1，二液式は2を記入）
sel_bm = 1


dir = 'Z:\\書庫\\研究テーマ\\推進系\\実験'
data_path = filedialog.askdirectory(initialdir=dir, title=data_dir + 'が格納されているフォルダを選択')
zikken_path = os.path.join(data_path, data_dir)
result_path = os.path.join(data_path, result_dir)
os.mkdir(result_path)

graph_file_extension = ".png"
filename_result_ave = result_path + "\\result_ave.csv"
filename_result_all = result_path + "\\result_all"
filename_wavelogger = data_filename + ".csv"

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