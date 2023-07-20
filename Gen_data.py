from rocketcea.cea_obj import CEA_Obj, add_new_oxidizer, add_new_propellant
import csv
import numpy as np

card_str = """
oxid H2O2(L) H 2 O 2  wt%=60.00
h,cal=-44880.0     t(k)=298.15  rho.g/cc=1.407
oxid = WATER H 2.0 O 1.0 wt%= 40.0
h,cal=-68317. t(k)=298.15 rho.g/cc=1.0
"""
add_new_oxidizer("60_H2O2", card_str)

card_str = """
name H2O2(L) H 2 O 2  wt%=60.00
h,cal=-44880.0     t(k)=298.15  rho.g/cc=1.407
oxid = WATER H 2.0 O 1.0 wt%= 40.0
h,cal=-68317. t(k)=298.15 rho.g/cc=1.0
"""
add_new_propellant("60_H2O2_mono", card_str)

ispObj = CEA_Obj(oxName="60_H2O2", fuelName="C2H5OH")  # 二液
#ispObj = CEA_Obj(propName="60_H2O2_mono")  # 一液


class Gen_data:
    def __init__(self):
        print("Active Generate data")

    def gen_data(self, filename_data, filename_result_all, filename_result_ave, dirs):
        # csv読み込み．waveloggerの設定をいじらなければ変えなくて良い．
        with open(filename_data, newline="", encoding="shift-jis") as f:
            reader = csv.reader(f)
            data_csv = [row for row in reader]  # data start at 62rows

        data_len = len(data_csv) - 66
        header = data_csv[61]
        print("データの長さ：", data_len)
        print("ヘッダー", end=":")
        print(header)
        print("最初のデータ", end=":")
        print(data_csv[data_len + 62])
        # --------------

        # ３．【毎回確認】変数定義
        At_diameter = 1.0  # [mm]
        Interval = 100  # [Hz] サンプリング周波数
        OF_RHO = 1.24  # 推進剤の密度
        Pre_TRG = 2  # [sec]バルブ開の前後何秒グラフ描写,データ生成するか？
        Valve_TRG = 3.00  # [V]バルブの立ち上がりのエッジトリガの閾値
        Statick_ratio = 0.2  # [-]定常区間の割合を指定

        valve_column = 7  # バルブ電圧のカラムが，CSVの何列目かを書く．A列が0，B列が1である．
        Pc_column = 3  # チャンバ圧力のカラム
        Pt_column = 2  # 供給圧力がのカラム
        Pa_column = 4  # 直上圧力のカラム
        flow_rate_column = 5  # 流量のカラム
        Tc_column = 6  # チャンバ温度のカラム

        result_data_ave = [  # 平均値をcsvにまとめる時のヘッダー
            [
                "No",
                "start",
                "end",
                "Pt_A",
                "Pa_A",
                "Pc_A",
                "Pt_A",
                "Mmfr_A",
                "Isp_A",
                "F_A",
            ]
        ]
        # ---------------------------

        At = ((At_diameter / 2.0) * (At_diameter / 2.0)) * (np.pi)
        self.valve_data = []
        self.chamber_pressure_data = []
        self.supply_pressure_data = []
        self.above_pressure_data = []
        self.flow_rate_data = []
        self.chamber_temperature_data = []
        self.cstar_data = []
        self.cf_data = []
        self.thrust_data = []
        self.isp_vac_data = []

        # 計算するデータ範囲取得
        valve_open_num = 0
        plt_start_num = 0
        plt_end_num = 0
        for i in range(data_len):
            if (
                float(data_csv[i + 62][valve_column]) > Valve_TRG
                and valve_open_num == 0
            ):
                valve_open_num = i + 62
                plt_start_num = valve_open_num - (Pre_TRG * Interval)
            if (
                float(data_csv[i + 62][valve_column]) < 1.00
                and plt_start_num > 0
                and plt_end_num == 0
            ):
                plt_end_num = i + 62 + (Pre_TRG * Interval)
        # --------------------------

        # 各データをlistに入れる．
        for i in range(plt_start_num, plt_end_num):
            self.valve_data.append(float(data_csv[i][valve_column]))
            self.chamber_pressure_data.append(float(data_csv[i][Pc_column]))
            self.supply_pressure_data.append(float(data_csv[i][Pt_column]))
            self.above_pressure_data.append(float(data_csv[i][Pa_column]))
            self.flow_rate_data.append(float(data_csv[i][flow_rate_column]))
            self.chamber_temperature_data.append(float(data_csv[i][Tc_column]))

            pambcf = ispObj.getFrozen_PambCf(
                Pamb=0.000001,
                Pc=(float(data_csv[i][Pc_column]) * 145.038),
                MR=7.4,
                eps=100.0,
                frozenAtThroat=0,
            )
            vac_cstar_tc = ispObj.get_IvacCstrTc(
                (float(data_csv[i][Pc_column]) * 145.038),
                MR=7.4,
                eps=100.0,
                frozen=1,
                frozenAtThroat=0,
            )
            self.cstar_data.append(float(vac_cstar_tc[1]) * 0.3048)
            self.cf_data.append(float(pambcf[0]))
            self.thrust_data.append(
                float(data_csv[i][Pc_column]) * float(pambcf[0]) * At * 1000
            )
            if (
                i < (plt_start_num + (Pre_TRG * Interval))
                or i > (plt_end_num - (Pre_TRG * Interval))
                or (float(data_csv[i][flow_rate_column]) == 0.0)
            ):
                self.isp_vac_data.append(0.0)
            else:
                self.isp_vac_data.append(
                    (float(data_csv[i][3]) * float(pambcf[0]) * At * 1000)
                    / (float(data_csv[i][flow_rate_column]) * OF_RHO * 9.80665)
                )
        self.x = np.arange(
            (0 - Pre_TRG), len(self.valve_data) / Interval - Pre_TRG, 1 / Interval
        )  # バルブデータから時間を生成
        # ------------------------------

        # 定常区間の平均値を取得
        Static_start_num = int(
            (plt_end_num - plt_start_num - (Pre_TRG * Interval * 2))
            * (1 - Statick_ratio)
        ) + int(Pre_TRG * Interval)
        Static_end_num = int(
            plt_end_num - plt_start_num - (Pre_TRG * Interval * 2)
        ) + int(Pre_TRG * Interval)
        chamber_pressure_ave = sum(
            self.chamber_pressure_data[Static_start_num:Static_end_num]
        ) / len(self.chamber_pressure_data[Static_start_num:Static_end_num])
        supply_pressure_ave = sum(
            self.supply_pressure_data[Static_start_num:Static_end_num]
        ) / len(self.supply_pressure_data[Static_start_num:Static_end_num])
        above_pressure_ave = sum(
            self.above_pressure_data[Static_start_num:Static_end_num]
        ) / len(self.above_pressure_data[Static_start_num:Static_end_num])
        chamber_temperature_ave = sum(
            self.chamber_temperature_data[Static_start_num:Static_end_num]
        ) / len(self.chamber_temperature_data[Static_start_num:Static_end_num])
        flow_rate_ave = sum(self.flow_rate_data[Static_start_num:Static_end_num]) / len(
            self.flow_rate_data[Static_start_num:Static_end_num]
        )
        isp_vac_ave = sum(self.isp_vac_data[Static_start_num:Static_end_num]) / len(
            self.isp_vac_data[Static_start_num:Static_end_num]
        )
        thrust_ave = sum(self.thrust_data[Static_start_num:Static_end_num]) / len(
            self.thrust_data[Static_start_num:Static_end_num]
        )

        result_data_ave.append(
            [
                dirs,
                (Static_start_num - (Pre_TRG * Interval)) / Interval,
                (Static_end_num - (Pre_TRG * Interval)) / Interval,
                supply_pressure_ave,
                above_pressure_ave,
                chamber_pressure_ave,
                chamber_temperature_ave,
                flow_rate_ave,
                isp_vac_ave,
                thrust_ave,
            ]
        )

        with open(filename_result_ave, "a", newline="") as f:  # まずファイルを作成
            writer = csv.writer(f)
        with open(filename_result_ave, newline="") as f:  # ファイルを読む
            r = f.read()
        with open(filename_result_ave, "a", newline="") as f:  # csvで平均値を保存
            writer = csv.writer(f)
            if r == "":  # ファイルの中身が空の場合は，ヘッダーを追加
                writer.writerow(result_data_ave[0])
            writer.writerow(result_data_ave[1])
        # ---------------------

        # 計算に用いたデータを全てcsvで出力
        result_data_all = [
            [
                "Time",
                "Pt[MPaA]",
                "Pa[MPaA]",
                "Pc[MPaA]",
                "Tc[K]",
                "Mmfr[ml/s]",
                "Isp[sec]",
                "F[mN]",
            ]
        ]
        for i in range(len(self.valve_data)):
            result_data_all.append(
                [
                    self.x[i],
                    self.supply_pressure_data[i],
                    self.above_pressure_data[i],
                    self.chamber_pressure_data[i],
                    self.chamber_temperature_data[i],
                    self.flow_rate_data[i],
                    self.isp_vac_data[i],
                    self.thrust_data[i],
                ]
            )
        with open(filename_result_all + "_" + dirs + ".csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(result_data_all)
        # --------------------------


if __name__ == "__main__":
    str = ispObj.get_full_cea_output(
        Pc=40.0,
        eps=100.0,
        MR=7.4,
        frozen=1,
        frozenAtThroat=0,
        short_output=1,
        pc_units="bar",
        output="siunits",
    )

    print(str)
