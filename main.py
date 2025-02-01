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
# 00_ダミーデータを入れることで，01以降のCf_actが正しく算出される
zikken_path = "Z:\\書庫\\研究テーマ\\推進系\\実験\\FY2024実験\\241217_LeeINJ付け前処理形状変更一液予熱150℃_合\\解析データ" 

# ２．【毎回変更する】生成ファイルを格納するフォルダ
result_path = "Z:\\書庫\\研究テーマ\\推進系\\実験\\FY2024実験\\241217_LeeINJ付け前処理形状変更一液予熱150℃_合\\解析結果3"


# ３．一液式の場合は１を，二液式の場合は２を入れる．
sel_bm = 1

graph_file_extension = ".png"
filename_result_ave = result_path + "\\result_ave.csv"
filename_result_ave2 = result_path + "\\result_ave2.csv"
filename_result_std = result_path + "\\result_std.csv"
filename_result_all = result_path + "\\result_all"
filename_wavelogger = "M$0.csv"

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
    if i ==0: #00_ダミーデータをfilename_result_ave, filename_result_stdへ含めないために消す．
        gd.gen_data(filename_data[i], filename_result_all, filename_result_ave, filename_result_ave2, filename_result_std, dirs[i], sel_bm)
        if(os.path.isfile(filename_result_ave) or os.path.isfile(filename_result_ave2) or os.path.isfile(filename_result_std)):
            os.remove(filename_result_ave)
            os.remove(filename_result_ave2)
            os.remove(filename_result_std)
    else:
        gd.gen_data(filename_data[i], filename_result_all, filename_result_ave, filename_result_ave2, filename_result_std, dirs[i], sel_bm)
        # 時系列グラフ生成
        gg.gen_graphs(result_path, dirs[i], graph_file_extension)
        #推進剤使用量系列グラフ生成
        gg.gen_graphs_ave(result_path,filename_result_ave)
    
    print("完了：" + dirs[i])

#図のgif画像生成
print("")
print("gif生成中")
dirs_2 = os.listdir(zikken_path) #gif画像を作るためにフォルダ名を取得
dirs_2.remove("00_ダミーデータ") #00_ダミーデータは不要のため削除
print(dirs_2) #gif画像生成に使うフォルダ名一覧を確認
for i in range(4): #4種類のgif画像生成
    g_gif.gen_gif(result_path, dirs_2, i+1, 200)
print("gif生成完了")

#gg.gen_graphs_ave(result_path, dirs[i], graph_file_extension,filename_result_ave)