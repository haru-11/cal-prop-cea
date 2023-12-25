import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ptick
from Gen_data import Gen_data
import csv

class Gen_graphs(Gen_data):
    def __init__(self, data_instance):
        super().__init__()
        print("Active generate graphs")
        self.gd = data_instance

    def gen_graphs(self, path, dirs, extension):
        #6．グラフのy軸範囲や要素などを確認

        # 全体のグラフ設定
        
        fig1 = plt.figure(figsize=[10.0, 7.5])
        plt.rcParams["font.size"] = 17
        
        # グラフ描写の１つ目(チャンバ内圧力とチャンバ内温度)
        
        # チャンバ内圧力
        ax1_1 = fig1.add_subplot(1, 1, 1)
        ax1_1.plot(self.gd.x, self.gd.chamber_pressure_data, color="k", label="pressure")
        ax1_1.set_ylim(0, 0.5)  # プロットのY範囲
        ax1_1.set_xlabel("Time[sec]")
        ax1_1.set_ylabel("Camber pressure[MPaA]")
        ax1_1.grid(color='k', linestyle=':', linewidth=0.3)

        # チャンバ内温度
        ax1_2 = ax1_1.twinx()
        ax1_2.plot(self.gd.x, self.gd.chamber_temperature_data, color="red", label="temp")
        ax1_2.set_ylim(0, 200)  # プロットのY範囲
        ax1_2.set_ylabel("Camber temperature[℃]")

        # バルブ電圧
        ax1_3 = ax1_1.twinx()
        ax1_3.plot(self.gd.x, self.gd.valve_data, color="blue", label="valve")
        ax1_3.set_ylim(0, 5)  # プロットのY範囲
        ax1_3.axis("off")

        # 凡例
        h1, l1 = ax1_1.get_legend_handles_labels()
        h2, l2 = ax1_2.get_legend_handles_labels()
        ax1_1.legend(h1 + h2, l1 + l2)

        # 図の保存
        plt.savefig(path + "\\" + dirs + "_fig1" + extension)
        # 図のクリア
        plt.clf()

        # グラフ描写の２つ目(圧力と流量)

        # チャンバ内圧力
        ax2_1 = fig1.add_subplot(1, 1, 1)
        ax2_1.plot(self.gd.x, self.gd.chamber_pressure_data, color="k", label="pressure")
        ax2_1.set_ylim(0, 0.5)  # プロットのY範囲
        ax2_1.set_xlabel("time[sec]")
        ax2_1.set_ylabel("camber pressure[MPaA]")
        ax2_1.grid(color='k', linestyle=':', linewidth=0.3)

        # 質量流量
        ax2_2 = ax2_1.twinx()
        ax2_2.plot(self.gd.x, self.gd.flow_rate_data, color="c", label="flow_rate")
        ax2_2.set_ylim(0, 1.0)  # プロットのY範囲
        ax2_2.set_ylabel("flow rate[g/s]")

        # バルブ電圧
        ax2_3 = ax2_1.twinx()
        ax2_3.plot(self.gd.x, self.gd.valve_data, color="blue", label="valve")
        ax2_3.set_ylim(0, 5)  # プロットのY範囲
        ax2_3.axis("off")

        # 凡例
        h1, l1 = ax2_1.get_legend_handles_labels()
        h2, l2 = ax2_2.get_legend_handles_labels()
        ax2_1.legend(h1 + h2, l1 + l2)

        # 図の保存
        plt.savefig(path + "\\" + dirs + "_fig2" + extension)
        # 図のクリア
        plt.clf()

        # グラフ描写の３つ目(推力と推力係数)

        # 推力
        ax3_1 = fig1.add_subplot(1, 1, 1)
        ax3_1.plot(self.gd.x, self.gd.thrust_data, color="m", label="thrust")
        #ax3_1.plot(self.gd.x, self.gd.cstar_data, color="k", label="cstar(CEA)")
        #ax3_1.plot(self.gd.x, self.gd.cstar_cal_data, color="m", label="cstar")
        ax3_1.set_ylim(0, 200)  # プロットのY範囲
        ax3_1.set_xlabel("time[sec]")
        ax3_1.set_ylabel("Thrust[mN]")
        ax3_1.grid(color='k', linestyle=':', linewidth=0.3)

        # 推力係数
        ax3_2 = ax3_1.twinx()
        ax3_2.plot(self.gd.x, self.gd.cf_act_data, color="k", label="Cf_act")
        #ax3_2.plot(self.gd.x, self.gd.chamber_pressure_data, color="r", label="Pc")
        ax3_2.set_ylim(0.0, 3)  # プロットのY範囲
        ax3_2.set_ylabel("Cf_act[-]")
        #ax3_2.set_ylabel("canber pressure[MPaA]")
        

        # バルブ電圧
        ax3_3 = ax3_1.twinx()
        ax3_3.plot(self.gd.x, self.gd.valve_data, color="blue", label="valve")
        ax3_3.set_ylim(0, 5)  # プロットのY範囲
        ax3_3.axis("off")

        # 凡例
        h1, l1 = ax3_1.get_legend_handles_labels()
        h2, l2 = ax3_2.get_legend_handles_labels()
        ax3_1.legend(h1 + h2, l1 + l2)

        # 図の保存
        plt.savefig(path + "\\" + dirs + "_fig3" + extension)
        # 図のクリア
        plt.clf()

        # グラフ描写の4つ目(c*とc*効率)

        # c*
        ax4_1 = fig1.add_subplot(1, 1, 1)
        ax4_1.plot(self.gd.x, self.gd.cstar_cal_ma_data, color="m", label="cstar")
        ax4_1.set_ylim(0, 4000)  # プロットのY範囲
        ax4_1.set_xlabel("Time[s]")
        ax4_1.set_ylabel("Characteristic exhaust velocity[m/s]")
        ax4_1.grid(color='k', linestyle=':', linewidth=0.3)

        # c*効率
        ax4_2 = ax4_1.twinx()
        ax4_2.plot(self.gd.x, self.gd.cstar_effi_ma_data, color="k", label="cstar_effi")
        ax4_2.set_ylim(0, 1.6)  # プロットのY範囲
        ax4_2.set_ylabel("Cstar_efficiency[-]")
        
        # バルブ電圧
        ax4_3 = ax4_1.twinx()
        ax4_3.plot(self.gd.x, self.gd.valve_data, color="blue", label="valve")
        ax4_3.set_ylim(0, 5)  # プロットのY範囲
        ax4_3.axis("off")
        
        # 凡例
        h1, l1 = ax4_1.get_legend_handles_labels()
        h2, l2 = ax4_2.get_legend_handles_labels()
        ax4_1.legend(h1 + h2, l1 + l2)

        # 図の保存
        plt.savefig(path + "\\" + dirs + "_fig4" + extension)
        # 図のクリア
        plt.clf()

        # グラフ描写の5つ目(推進剤滞在時間とチャンバ内密度)

        # 推進剤滞在時間
        ax5_1 = fig1.add_subplot(1, 1, 1)
        ax5_1.plot(self.gd.x, self.gd.stay_time_data, color="m", label="stay_time")
        ax5_1.set_ylim(0, 0.05)
        ax5_1.set_xlabel("Time[s]")
        ax5_1.set_ylabel("Propellant stay time[s]")
        ax5_1.grid(color='k', linestyle=':', linewidth=0.3)

        # チャンバ内密度
        ax5_2 = ax5_1.twinx()
        ax5_2.plot(self.gd.x, self.gd.density_data, color="k", label="density")
        ax5_2.yaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
        ax5_2.ticklabel_format(style="sci", axis="y", scilimits=(-3, -3))
        ax5_2.set_ylim(0, 0.0025)
        ax5_2.set_ylabel("Density[g/cm$^{3}$]")

        # バルブ電圧
        ax5_3 = ax5_1.twinx()
        ax5_3.plot(self.gd.x, self.gd.valve_data, color="blue", label="valve")
        ax5_3.set_ylim(0, 5)  # プロットのY範囲
        ax5_3.axis("off")

        # 凡例
        h1, l1 = ax5_1.get_legend_handles_labels()
        h2, l2 = ax5_2.get_legend_handles_labels()
        ax5_1.legend(h1 + h2, l1 + l2)

        # 図の保存
        plt.savefig(path + "\\" + dirs + "_fig5" + extension)
        # 図のクリア
        plt.clf()

        # グラフ描写の6つ目(c*の元データと移動平均値と移動中央値)

        # 元データ
        ax6_1 = fig1.add_subplot(1, 1, 1)
        ax6_1.plot(self.gd.x, self.gd.cstar_cal_data, color="m", label="cstar")
        ax6_1.set_ylim(0, 4000)  # プロットのY範囲
        ax6_1.set_xlabel("Time[s]")
        ax6_1.set_ylabel("Characteristic exhaust velocity[m/s]")
        ax6_1.grid(color='k', linestyle=':', linewidth=0.3)

        # 移動平均値
        ax6_2 = ax6_1.twinx()
        ax6_2.plot(self.gd.x, self.gd.cstar_cal_ma_data, color="c", label="cstar_mean")
        ax6_2.set_ylim(0, 4000)
        ax6_2.set_ylabel("Characteristic exhaust velocity mean [m/s]")

        # 移動中央値
        ax6_3 = ax6_1.twinx()
        ax6_3.plot(self.gd.x, self.gd.cstar_cal_mm_data, color="y", label="cstar_median")
        ax6_3.set_ylim(0, 4000)
        ax6_3.set_ylabel("Characteristic exhaust velocity median [m/s]")

        # バルブ電圧
        ax6_4 = ax6_1.twinx()
        ax6_4.plot(self.gd.x, self.gd.valve_data, color="k", label="valve")
        ax6_4.set_ylim(0, 5)  # プロットのY範囲
        ax6_4.axis("off")

        # 凡例
        h1, l1 = ax6_1.get_legend_handles_labels()
        h2, l2 = ax6_2.get_legend_handles_labels()
        h3, l3 = ax6_3.get_legend_handles_labels()
        ax6_1.legend(h1 + h2 + h3, l1 + l2 + l3)

        # 図の保存
        plt.savefig(path + "\\" + dirs + "_fig6" + extension)
        # 図のクリア
        plt.clf()

        # プロットの終了
        plt.close()

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

        data_head_num = 1
        data_end_num = data_len - 1

        Pc_A_column = 5
        Mmfr_A_column = 7
        Sum_column = 9
        Cstar_effi_column = 14

        Pc_A_data = []
        Mmfr_A_data = []
        Sum_data = []
        Cstar_effi_data = []

        for i in range(data_head_num, data_end_num):
            Pc_A_data.append(float(data_csv[i][Pc_A_column]))
            Mmfr_A_data.append(float(data_csv[i][Mmfr_A_column]))
            Sum_data.append(float(data_csv[i][Sum_column]))
            Cstar_effi_data.append(float(data_csv[i][Cstar_effi_column]))
        ex_num = np.arange(data_len - 1)
        
        self.ave_graph(path, "Pc_vs_Total" ,Sum_data,"total[g]",Pc_A_data,"Chamber pressure[MPaA]", "Pc", (0,0.6),"red", 'o')
        self.ave_graph(path, "Cstar_vs_Total" ,Sum_data,"total[g]",Cstar_effi_data,"Cstar efficiency", "Cstar efficiency", (0,1.2),"k", 'o')
        self.ave_graph_2(path,"Pc_and_Cstar_vs_total", Sum_data, "total[g]", Pc_A_data, "Chamber pressure[MPaA]", "Pc", (0,0.6), "red", 'o', Cstar_effi_data, "Cstar efficiency[-]", "Cstar effi", (0,1.2),"k", 'o')
        
    def ave_graph(self,path,filename, x_data, x_label, y_data, y_label, y_legend, y_lim, color, marker):
        fig = plt.figure(figsize=[10, 7.5])
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(x_data, y_data, marker=marker, color=color, label=y_legend)
        #ax.set_xlim(0,350)
        ax.set_ylim(y_lim)  # プロットのY範囲
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.grid(color='k', linestyle=':', linewidth=0.3)
        plt.savefig(path + "\\" + filename + ".png")
        #plt.show()
        plt.clf()
        plt.close()

    def ave_graph_2(self,path,filename, x_data, x_label, y_data, y_label, y_legend, y_lim, color, marker, y_data2, y_label2, y_legend2, y_lim2, color2, marker2):
        fig = plt.figure(figsize=[10, 7.5])
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(x_data, y_data, marker=marker, color=color, label=y_legend)
        #ax.set_xlim(0,350)
        ax.set_ylim(y_lim)  # プロットのY範囲
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.grid(color='k', linestyle=':', linewidth=0.3)

        ax_2 = ax.twinx()
        ax_2.plot(x_data, y_data2, marker=marker2, color=color2, label=y_legend2)
        ax_2.set_ylim(y_lim2)
        ax_2.set_ylabel(y_label2)

        h1, l1 = ax.get_legend_handles_labels()
        h2, l2 = ax_2.get_legend_handles_labels()
        ax.legend(h1 + h2, l1 + l2)
        plt.savefig(path + "\\" + filename + ".png")
        #plt.show()
        plt.clf()
        plt.close()

if __name__ == "__main__":
    from Gen_data import Gen_data
    import csv
    gd = Gen_data()
    gg = Gen_graphs(gd)

    # ２．【毎回変更する】生成ファイルを格納するフォルダ
    result_path = "X:\\書庫\\研究テーマ\\推進系\\実験\\FY2022実験\\220524_前処理触媒_1液\\解析結果_新解析ソフト3"

    # 一液式の場合は１を，二液式の場合は２を入れる．
    graph_file_extension = ".png"
    filename_result_ave = result_path + "\\result_ave.csv"
    filename_result_all = result_path + "\\result_all"
    filename_wavelogger = "auto$0.csv"

    gg.gen_graphs_ave(result_path,filename_result_ave)