import numpy as np
import matplotlib.pyplot as plt
from Gen_data import Gen_data


class Gen_graphs(Gen_data):
    def __init__(self, data_instance):
        super().__init__()
        print("Active generate graphs")
        self.gd = data_instance

    def gen_graphs(self, path, dirs, extension):
        # グラフ描写
        # 全体のグラフ設定
        fig1 = plt.figure(figsize=[8, 4.5])

        # 一つ目のグラフ描写
        ax1_1 = fig1.add_subplot(1, 1, 1)
        ax1_1.plot(
            self.gd.x, self.gd.chamber_pressure_data, color="red", label="pressure"
        )
        ax1_1.set_ylim(0, 0.6)  # プロットのY範囲
        ax1_1.set_xlabel("time[sec]")
        ax1_1.set_ylabel("camber pressure[MPaA]")

        ax1_2 = ax1_1.twinx()
        ax1_2.plot(
            self.gd.x, self.gd.chamber_temperature_data, color="green", label="temp"
        )
        ax1_2.set_ylim(0, 200)  # プロットのY範囲
        ax1_2.set_ylabel("camber temperature[K]")

        ax1_3 = ax1_1.twinx()
        ax1_3.plot(self.gd.x, self.gd.valve_data, color="blue", label="valve")
        ax1_3.set_ylim(0, 6)  # プロットのY範囲
        ax1_3.axis("off")

        h1, l1 = ax1_1.get_legend_handles_labels()
        h2, l2 = ax1_2.get_legend_handles_labels()
        ax1_1.legend(h1 + h2, l1 + l2)

        plt.savefig(path + "\\" + dirs + "_fig1" + extension)
        plt.clf()

        # グラフ描写の二つ目
        ax2_1 = fig1.add_subplot(1, 1, 1)
        ax2_1.plot(
            self.gd.x, self.gd.chamber_pressure_data, color="red", label="pressure"
        )
        ax2_1.set_ylim(0, 0.6)  # プロットのY範囲
        ax2_1.set_xlabel("time[sec]")
        ax2_1.set_ylabel("camber pressure[MPaA]")

        ax2_2 = ax2_1.twinx()
        ax2_2.plot(self.gd.x, self.gd.flow_rate_data, color="c", label="flow_rate")
        ax2_2.set_ylim(0, 1)  # プロットのY範囲
        ax2_2.set_ylabel("flow rate[ml/s]")

        ax2_3 = ax2_1.twinx()
        ax2_3.plot(self.gd.x, self.gd.valve_data, color="blue", label="valve")
        ax2_3.set_ylim(0, 6)  # プロットのY範囲
        ax2_3.axis("off")

        # 凡例
        h1, l1 = ax2_1.get_legend_handles_labels()
        h2, l2 = ax2_2.get_legend_handles_labels()
        ax2_1.legend(h1 + h2, l1 + l2)

        plt.savefig(path + "\\" + dirs + "_fig2" + extension)
        plt.clf()

        # グラフ描写の３つ目
        ax3_1 = fig1.add_subplot(1, 1, 1)
        ax3_1.plot(self.gd.x, self.gd.cstar_data, color="k", label="cstar(CEA)")
        ax3_1.plot(self.gd.x, self.gd.cstar_cal_data, color="m", label="cstar")
        ax3_1.set_ylim(0, 1000)  # プロットのY範囲
        ax3_1.set_xlabel("time[sec]")
        ax3_1.set_ylabel("cstar[m/s]")

        ax3_2 = ax3_1.twinx()
        ax3_2.plot(self.gd.x, self.gd.chamber_pressure_data, color="r", label="Pc")
        ax3_2.set_ylim(0.0, 0.6)  # プロットのY範囲
        ax3_2.set_ylabel("canber pressure[MPaA]")

        ax3_3 = ax3_1.twinx()
        ax3_3.plot(self.gd.x, self.gd.valve_data, color="blue", label="valve")
        ax3_3.set_ylim(0, 6)  # プロットのY範囲
        ax3_3.axis("off")

        # 凡例
        h1, l1 = ax3_1.get_legend_handles_labels()
        h2, l2 = ax3_2.get_legend_handles_labels()
        ax3_1.legend(h1 + h2, l1 + l2)

        # 凡例
        h1, l1 = ax2_1.get_legend_handles_labels()
        h2, l2 = ax2_2.get_legend_handles_labels()
        ax2_1.legend(h1 + h2, l1 + l2)
        plt.savefig(path + "\\" + dirs + "_fig3" + extension)
        plt.clf()

        # グラフ描写の4つ目
        print(self.gd.total_throughput_sum, self.gd.chamber_pressure_ave_sum)
        ax4_1 = fig1.add_subplot(1, 1, 1)
        ax4_1.plot(self.gd.total_throughput_sum, self.gd.chamber_pressure_ave_sum, color="m", label="Pc")
        ax4_1.set_ylim(0, 0.6)  # プロットのY範囲
        ax4_1.set_xlabel("total_throughput[g]")
        ax4_1.set_ylabel("camber pressure[MPaA]")

        '''
        ax4_2 = ax4_1.twinx()
        ax4_2.plot(self.gd.total_throughput_sum, self.gd.isp_vac_data, color="k", label="isp")
        ax4_2.set_ylim(0, 300)  # プロットのY範囲
        ax4_2.set_ylabel("Isp[sec]")
        '''
        '''
        ax4_3 = ax4_1.twinx()
        ax4_3.plot(self.gd.x, self.gd.valve_data, color="blue", label="valve")
        ax4_3.set_ylim(0, 6)  # プロットのY範囲
        ax4_3.axis("off")
        '''
        # 凡例
        h1, l1 = ax4_1.get_legend_handles_labels()
        #h2, l2 = ax4_2.get_legend_handles_labels()
        #ax4_1.legend(h1 + h2, l1 + l2)
        #ax4_1.legend(h1 + h2)
        plt.savefig(path + "\\" + dirs + "_fig4" + extension)
        # plt.show()

    def gen_graphs_ave(self, path, filename):
        # csv読み込み．waveloggerの設定をいじらなければ変えなくて良い．
        with open(filename, newline="", encoding="shift-jis") as f:
            reader = csv.reader(f)
            data_csv = [row for row in reader]  # data start at 62rows
        #print(data_csv)
        data_len = len(data_csv)
        header = data_csv[0]
        print(data_len)
        print(header)

if __name__ == "__main__":
    from Gen_data import Gen_data
    import csv
    gd = Gen_data()
    gg = Gen_graphs(gd)

    # ２．【毎回変更する】生成ファイルを格納するフォルダ
    result_path = "C:\\Users\\SAHARA-7\\OneDrive - 東京都公立大学法人\\ドキュメント\\首都大\\M2\\FY2022実験\\220524_前処理触媒_1液\\解析結果_python"

    # 一液式の場合は１を，二液式の場合は２を入れる．
    graph_file_extension = ".png"
    filename_result_ave = result_path + "\\result_ave.csv"
    filename_result_all = result_path + "\\result_all"
    filename_wavelogger = "auto$0.csv"

    gg.gen_graphs_ave(result_path,filename_result_ave)