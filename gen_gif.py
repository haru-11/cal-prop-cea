# -*- coding: utf-8 -*-
from PIL import Image
import os

class Gen_gif:
    def __init__(self):
        print("Active Generate gif")

    def gen_gif(self, result_path, dirs, fig_num, duration):
        pictures = []

        for i in range(len(dirs)):
            pic_name = result_path + "\\" + dirs[i] + "_fig" + str(fig_num) + '.png'
            img = Image.open(pic_name)
            pictures.append(img)

        pictures[0].save( result_path + "\\" + 'fig' + str(fig_num) + '_' + str(duration) + 'ms.gif', save_all=True, append_images=pictures[1:], optimize=True, duration=duration, loop=0)

if __name__ == "__main__":

    # １．【毎回変更する】実験データが格納されているフォルダ
    zikken_path = "X:\\書庫\\研究テーマ\\推進系\\実験\\FY2022実験\\220524_前処理触媒_1液\\解析データ"

    # ２．【毎回変更する】生成ファイルを格納するフォルダ
    result_path = "X:\\書庫\\研究テーマ\\推進系\\実験\\FY2022実験\\220524_前処理触媒_1液\\解析結果_新解析ソフト"

    dirs = os.listdir(zikken_path)
    pictures=[]

    for i in range(len(dirs)):
        pic_name = result_path + "\\" + dirs[i] + "_fig1" + '.png'
        img = Image.open(pic_name)
        pictures.append(img)
    #gifアニメを出力する

    pictures[0].save( result_path + "\\" + 'fig1.gif', save_all=True, append_images=pictures[1:], optimize=True, duration=200, loop=0)