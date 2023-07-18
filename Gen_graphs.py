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
        ax1_1.set_ylim(0, 0.7)  # プロットのY範囲
        ax1_1.set_xlabel("time[sec]")
        ax1_1.set_ylabel("camber pressure[MPaA]")

        ax1_2 = ax1_1.twinx()
        ax1_2.plot(
            self.gd.x, self.gd.chamber_temperature_data, color="green", label="temp"
        )
        ax1_2.set_ylim(0, 1500)  # プロットのY範囲
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
        ax2_1.set_ylim(0, 0.7)  # プロットのY範囲
        ax2_1.set_xlabel("time[sec]")
        ax2_1.set_ylabel("camber pressure[MPaA]")

        ax2_2 = ax2_1.twinx()
        ax2_2.plot(self.gd.x, self.gd.flow_rate_data, color="c", label="flow_rate")
        ax2_2.set_ylim(0, 2)  # プロットのY範囲
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
        ax3_1.plot(self.gd.x, self.gd.cstar_data, color="k", label="cstar")
        ax3_1.set_ylim(1313, 1317)  # プロットのY範囲
        ax3_1.set_xlabel("time[sec]")
        ax3_1.set_ylabel("cstar[m/s]")

        ax3_2 = ax3_1.twinx()
        ax3_2.plot(self.gd.x, self.gd.cf_data, color="c", label="cf")
        ax3_2.set_ylim(1.856, 1.860)  # プロットのY範囲
        ax3_2.set_ylabel("cf[-]")

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
        ax4_1 = fig1.add_subplot(1, 1, 1)
        ax4_1.plot(self.gd.x, self.gd.thrust_data, color="m", label="thrust")
        ax4_1.set_ylim(0, 1000)  # プロットのY範囲
        ax4_1.set_xlabel("time[sec]")
        ax4_1.set_ylabel("thrust[mN]")

        ax4_2 = ax4_1.twinx()
        ax4_2.plot(self.gd.x, self.gd.isp_vac_data, color="k", label="isp")
        ax4_2.set_ylim(0, 300)  # プロットのY範囲
        ax4_2.set_ylabel("Isp[sec]")

        ax4_3 = ax4_1.twinx()
        ax4_3.plot(self.gd.x, self.gd.valve_data, color="blue", label="valve")
        ax4_3.set_ylim(0, 6)  # プロットのY範囲
        ax4_3.axis("off")

        # 凡例
        h1, l1 = ax4_1.get_legend_handles_labels()
        h2, l2 = ax4_2.get_legend_handles_labels()
        ax4_1.legend(h1 + h2, l1 + l2)
        plt.savefig(path + "\\" + dirs + "_fig4" + extension)

        # plt.show()
