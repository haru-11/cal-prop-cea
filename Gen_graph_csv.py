import matplotlib.pyplot as plt
import os
import csv


class GenGraph:
    def __init__(self):
        print("Hello world!")

    def gen_dataset(self, filename,column):
        _data = []
        _time = []
        with open(filename, newline="", encoding="shift-jis") as f:
            reader = csv.reader(f)
            data_csv = [row for row in reader]  # data start at 62rows
        for i in range(1, len(data_csv) ,1):
            _data.append(float(data_csv[i][column]))
            _time.append(float(data_csv[i][0]))
        self.element_name = data_header[column]
        return _data,_time

    def all_gen(self):
        for data_column in range(1, len(data_header)):
            ggc.single_gen(data_column)
        
    def single_gen(self,data_column):
        dataset = []
        timeset = []
        for j in range(len(path_list)):
            _d, _t = ggc.gen_dataset(path_list[j],data_column)
            dataset.append(_d)
            timeset.append(_t)
            #print(path_list[j])

        cmap = plt.get_cmap("plasma")
        fig = plt.figure(figsize=[10, 7.5])
        ax = fig.add_subplot(1, 1, 1)
        #ax.plot(timeset[0], dataset[0] , marker=None, color='k')
        for i in range(len(dataset)-1,0,-1):
            ind = i / len(dataset)
            ax.plot(timeset[i], dataset[i] , marker=None, color=cmap(ind))
        #ax.set_xlim(-2.5,17.5)
        ax.set_ylim(0,1.6)  # プロットのY範囲
        ax.set_xlabel("time")
        ax.set_ylabel(data_header[data_column])
        ax.grid(color='k', linestyle=':', linewidth=0.3)
        
        print(path + "\\series_"+ ggc.element_name + ".png")
        plt.savefig(path + "\\series_"+ ggc.element_name + ".png")
        #plt.show()
        plt.clf()
        #plt.close()




if __name__ == "__main__":
    ggc = GenGraph()

    # グラフ化するcsvファイル名のリストを取得
    path_list = []
    path = "C:\\Users\\SAHARA-7\\OneDrive - 東京都公立大学法人\\ドキュメント\\首都大\M2\\FY2022実験\\220928_1U推力測定_スラストスタンド_2液\\解析結果_新解析ソフト"
    ls = os.listdir(path)

    for i in ls:
        base, ext = os.path.splitext(i)
        if (
            ext == ".csv" and base.find("result_all") != -1
        ):  # 拡張子がcsvで，かつファイル名にresult_allが含まれているもののみ対象とする．
            path_list.append(os.path.join(path, i))
            #print(os.path.join(path, i))
            #print(path_list)
    # -------------------------
    data_header = [
        "Time",
        "Pt[MPaA]",
        "Pa[MPaA]",
        "Pc[MPaA]",
        "Tc[K]",
        "Mmfr[g_per_s]",
        "Total[g]",
        "Cf_cea[-]",
        "Cf_act[-]",
        "Cstar_CEA[sec]",
        "Cater_cal[sec]",
        "Cstar_effi[-]",
        "Isp[sec]",
        "F[mN]",
    ]
    #data_column = 12
    #ggc.all_gen()
    ggc.single_gen(11)
