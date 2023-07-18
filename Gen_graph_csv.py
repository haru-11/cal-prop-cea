import matplotlib.pyplot as plt
import os
import csv


class GenGraph:
    def __init__(self):
        # グラフ化するcsvファイル名のリストを取得
        path_list = []
        path = "C:\\Users\\SAHARA-7\\workspace\\cal-prop-cea\\実験結果"
        ls = os.listdir(path)
        for i in ls:
            base, ext = os.path.splitext(i)
            if (
                ext == ".csv" and base.find("result_all") != -1
            ):  # 拡張子がcsvで，かつファイル名にresult_allが含まれているもののみ対象とする．
                path_list.append(os.path.join(path, i))
                print(os.path.join(path, i))
        # -------------------------
        data_header = [
            "Time",
            "Pt[MPaA]",
            "Pa[MPaA]",
            "Pc[MPaA]",
            "Tc[K]",
            "Mmfr[ml/s]",
            "Isp[sec]",
            "F[mN]",
        ]
        self.gen_dataset(path_list[0])

    def gen_dataset(self, filename):
        with open(filename, newline="", encoding="shift-jis") as f:
            reader = csv.reader(f)
            data_csv = [row for row in reader]  # data start at 62rows


if __name__ == "__main__":
    ggc = GenGraph()
