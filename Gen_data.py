from math import cos
from rocketcea.cea_obj import add_new_oxidizer, add_new_propellant
from rocketcea.cea_obj_w_units import CEA_Obj
import csv
import numpy as np
import scipy.constants as const
import statistics

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

ispObj_2 = CEA_Obj(oxName="60_H2O2", fuelName="C2H5OH", 
                   pressure_units='MPa', temperature_units='K', 
                   isp_units='sec', cstar_units='m/s', sonic_velocity_units='m/s', 
                   enthalpy_units='J/kg', density_units='kg/m^3',specific_heat_units='J/kg-K',thermal_cond_units='W/cm-degC')  # 二液
ispObj_1 = CEA_Obj(propName="60_H2O2_mono", 
                   pressure_units='MPa', temperature_units='K', 
                   isp_units='sec', cstar_units='m/s', sonic_velocity_units='m/s', 
                   enthalpy_units='J/kg', density_units='kg/m^3',specific_heat_units='J/kg-K',thermal_cond_units='W/cm-degC')  # 一液


class Gen_data:
    def __init__(self):
        print("Active Generate data")
        self.total_throughput_sum = []
        self.chamber_pressure_ave_sum = []

    def gen_data(self, filename_data, filename_result_all, filename_result_ave, dirs, sel_bm):
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
        print(data_csv[62])
        print("最後のデータ", end=":")
        print(data_csv[data_len + 62])
        # --------------

        #5．【毎回確認】変数定義
        Dt = 0.54  # スロート径[mm]
        Vc = 615.946865648317 # 燃焼室容積[mm^3]
        Nozzle_cone_half_ang = 15 # ノズルコーン半頂角,Θ
        Thrust_coefficient_effi = 0.92 # 推力係数効率
        Interval = 100  # [Hz] サンプリング周波数
        O_RHO = 1.24       # 60%H2O2の場合は1.24，水の場合は1.00
        F_RHO = 0.79       # エタノールの場合は0.79，水の場合は1.00
        MR = 7.4      # OFを入力．一液の場合は0を記入
        Pre_TRG = 2  # [sec]バルブ開の前後何秒グラフ描写,データ生成するか？
        Valve_TRG = 3.00  # [V]バルブの立ち上がりのエッジトリガの閾値
        Statick_ratio = 0.2  # [-]定常区間の割合を指定
        moving_num = 10 # 移動平均の個数

        valve_column = 7  # バルブ電圧のカラムが，CSVの何列目かを書く．A列が0，B列が1である．
        Pt_column = 2  # 供給圧力がのカラム
        Pa_column = 4  # 直上圧力のカラム
        Pc_column = 3  # チャンバ圧力のカラム
        Tc_column = 6  # チャンバ温度のカラム
        flow_rate_column = 5  # 流量のカラム

        At = ((Dt / 2.0) ** 2 ) * (np.pi) # [mm^2]
        Lster = Vc / At # [mm]

        if MR > 0:
            OF_RHO = (O_RHO * F_RHO) * (1 + MR)/(O_RHO + F_RHO * MR)
        elif MR == 0:
            OF_RHO = 1.24  # 推進剤の密度
        else:
            print("O/F ERROR")
        nozzle_factor = 0.5*(1+ cos(Nozzle_cone_half_ang/180*np.pi)) # ノズル修正係数の計算
        
        # ---------------------------

        self.valve_data = []
        self.supply_pressure_data = []  # 供給圧力
        self.above_pressure_data = []  # 直上圧力
        self.chamber_pressure_data = []  # 燃焼室内圧力
        self.chamber_temperature_data = []  # 燃焼室内温度
        self.flow_rate_data = []  # 質量流量
        self.total_throughput_data = []  # 推進剤使用量
        self.cf_cea_data = []  # ceaによる推力係数
        self.cf_act_data = []  # 効率をかけた実際の推力係数
        self.thrust_data = []  # 推力
        self.isp_vac_data = []  # 比推力
        self.cstar_cea_data = []  # ceaによるc*
        self.cstar_cal_data = []  # 実験値によるc*
        self.cstar_effi_data = []  # c*効率
        self.cstar_cal_ma_data = []  # 実験値によるc*の移動平均値
        self.cstar_effi_ma_data = []  # 移動平均値によるc*効率
        self.cstar_cal_mm_data = []  # 実験値によるc*の移動中央値
        self.cstar_effi_mm_data = []  # 移動中央値によるc*効率
        self.density_data = []  # 燃焼室内密度
        self.stay_time_data = []  # 推進剤滞在時間

        total_throughput = 0.0

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
        on_time = (plt_end_num - plt_start_num - (Pre_TRG * Interval * 2)) / Interval
        #on_time = (plt_end_num - plt_start_num - (Pre_TRG * Interval * 2))
        print("valve on time[sec]:"+ str(on_time))
        # --------------------------

        # 各データをlistに入れる．
        for i in range(plt_start_num, plt_end_num):
            self.valve_data.append(float(data_csv[i][valve_column]))
            self.chamber_pressure_data.append(float(data_csv[i][Pc_column]))
            self.supply_pressure_data.append(float(data_csv[i][Pt_column]))
            self.above_pressure_data.append(float(data_csv[i][Pa_column]))
            self.flow_rate_data.append(float(data_csv[i][flow_rate_column])*OF_RHO)
            self.chamber_temperature_data.append(float(data_csv[i][Tc_column]))

            if sel_bm == 2:
                pambcf = ispObj_2.getFrozen_PambCf(Pamb=0.000001, Pc=(float(data_csv[i][Pc_column])), MR=MR, eps=100.0, frozenAtThroat=0)
                vac_cstar_tc = ispObj_2.get_IvacCstrTc(Pc=(float(data_csv[i][Pc_column])), MR=MR, eps=100.0, frozen=1, frozenAtThroat=0)
                density = ispObj_2.get_Densities(Pc=(float(data_csv[i][Pc_column])), MR=MR, eps=100.0, frozen=1, frozenAtThroat=0)
            elif sel_bm == 1:
                pambcf = ispObj_1.get_PambCf(Pamb=0.000001, Pc=(float(data_csv[i][Pc_column])), eps=100.0)
                vac_cstar_tc = ispObj_1.get_IvacCstrTc(Pc=(float(data_csv[i][Pc_column])), eps=100.0, frozen=0, frozenAtThroat=0)
                density = ispObj_1.get_Densities(Pc=(float(data_csv[i][Pc_column])), eps=100.0, frozen=0, frozenAtThroat=0)

            else:
                print("select MR(O/F) error")

            self.cstar_cea_data.append(float(vac_cstar_tc[1]))
            self.cf_cea_data.append(float(pambcf[0]))
            self.cf_act_data.append(float(pambcf[0])*nozzle_factor*Thrust_coefficient_effi)
            self.thrust_data.append(float(data_csv[i][Pc_column]) * float(pambcf[0])*nozzle_factor*Thrust_coefficient_effi * At * 1000)
            self.density_data.append(float(density[0])/1000)

            if (    #流量はバルブオン以外は0とする．
                i < (plt_start_num + (Pre_TRG * Interval))
                or i > (plt_end_num - (Pre_TRG * Interval))
                or (float(data_csv[i][flow_rate_column]) == 0.0)
            ):
                self.isp_vac_data.append(0.0)
                self.cstar_cal_data.append(0.0)
                self.stay_time_data.append(0.0)
            else:
                self.isp_vac_data.append((self.thrust_data[i-plt_start_num]) / (self.flow_rate_data[i-plt_start_num] * const.g))
                self.cstar_cal_data.append(self.chamber_pressure_data[i-plt_start_num] * At / (self.flow_rate_data[i-plt_start_num] / 1000))
                self.stay_time_data.append(Vc / (float(data_csv[i][flow_rate_column])*OF_RHO) * (float(density[0])/1000000))

            total_throughput = total_throughput + self.flow_rate_data[i-plt_start_num]*(1.0/Interval)
            self.total_throughput_data.append(total_throughput)
            self.cstar_effi_data.append(self.cstar_cal_data[i-plt_start_num]/self.cstar_cea_data[i-plt_start_num])

        self.x = np.arange((0 - Pre_TRG), len(self.valve_data) / Interval - Pre_TRG, 1 / Interval)  # バルブデータから時間を生  

        # c*の移動平均値および移動中央値を出す
        self.cstar_cal_ma_data = self.moving_ave(self.cstar_cal_data, moving_num)  # c*の移動平均値
        self.cstar_cal_mm_data = self.moving_med(self.cstar_cal_data, moving_num)  # c*の移動中央値
        for i in range(len(self.x)):
            self.cstar_effi_ma_data.append(self.cstar_cal_ma_data[i] / self.cstar_cea_data[i])  # 移動平均値によるc*効率
            self.cstar_effi_mm_data.append(self.cstar_cal_mm_data[i] / self.cstar_cea_data[i])  # 移動中央値によるc*効率

        
        # ------------------------------

        # 定常区間の平均値を取得
        Static_start_num = int((plt_end_num - plt_start_num - (Pre_TRG * Interval * 2)) * (1 - Statick_ratio)) + int(Pre_TRG * Interval)  # 平均取得開始番号
        Static_end_num = int(plt_end_num - plt_start_num - (Pre_TRG * Interval * 2)) + int(Pre_TRG * Interval)  # 平均取得終了時間
        supply_pressure_ave = statistics.mean(self.supply_pressure_data[Static_start_num:Static_end_num])  # 供給圧力
        above_pressure_ave = statistics.mean(self.above_pressure_data[Static_start_num:Static_end_num])  # 直上圧力
        chamber_pressure_ave = statistics.mean(self.chamber_pressure_data[Static_start_num:Static_end_num])  # 燃焼室内圧力
        chamber_temperature_ave =  statistics.mean(self.chamber_temperature_data[Static_start_num:Static_end_num])  # 燃焼室内温度
        flow_rate_ave = statistics.mean(self.flow_rate_data[Static_start_num:Static_end_num])  # 質量流量
        cf_cea_ave = statistics.mean(self.cf_cea_data[Static_start_num:Static_end_num])  # ceaによる推力係数
        cf_act_ave = statistics.mean(self.cf_act_data[Static_start_num:Static_end_num])  # 効率をかけた実際の推力係数
        thrust_ave = statistics.mean(self.thrust_data[Static_start_num:Static_end_num])  # 推力
        isp_vac_ave = statistics.mean(self.isp_vac_data[Static_start_num:Static_end_num])  # 比推力
        cstar_cea_ave = statistics.mean(self.cstar_cea_data[Static_start_num:Static_end_num])  # ceaによるc*
        cstar_cal_ave = statistics.mean(self.cstar_cal_data[Static_start_num:Static_end_num])  # 実験値によるc*
        cstar_effi_ave = statistics.mean(self.cstar_effi_data[Static_start_num:Static_end_num])  # c*効率
        cstar_cal_ma_ave = statistics.mean(self.cstar_cal_ma_data[Static_start_num:Static_end_num])  # 実験値によるc*の移動平均値
        cstar_effi_ma_ave = statistics.mean(self.cstar_effi_ma_data[Static_start_num:Static_end_num])  # 移動平均値によるc*効率
        cstar_cal_mm_ave = statistics.mean(self.cstar_cal_mm_data[Static_start_num:Static_end_num])  # 実験値によるc*の移動中央値
        cstar_effi_mm_ave = statistics.mean(self.cstar_effi_mm_data[Static_start_num:Static_end_num])  # 移動中央値によるc*効率
        density_ave = statistics.mean(self.density_data[Static_start_num:Static_end_num])  # 燃焼室内密度
        stay_time_ave = statistics.mean(self.stay_time_data[Static_start_num:Static_end_num])  # 推進剤滞在時間
        
        if len(self.total_throughput_sum) == 0:
            _tt = total_throughput
        else:
            _tt = self.total_throughput_sum[len(self.total_throughput_sum)-1] + total_throughput
        self.total_throughput_sum.append(_tt)
        self.chamber_pressure_ave_sum.append(chamber_pressure_ave)

        result_data_ave = [  # 平均値をcsvにまとめる時のヘッダー
            [  # データ名
                "No",  # 実験番号
                "start",  # 平均取得開始時間
                "end",  # 平均取得終了時間
                "Pt",  # 供給圧力
                "Pa",  # 直上圧力
                "Pc",  # 燃焼室内圧力
                "Tc",  # 燃焼室内温度
                "mdot",  # 質量流量
                "Total",  # 推進剤使用量
                "Sum",  # 推進剤使用量の合計
                "Cf_cea",  # ceaによる推力係数
                "Cf_act",  # 効率をかけた実際の推力係数
                "F",  # 推力
                "Isp",  # 比推力
                "Cstar_cea",  # ceaによるc*
                "Cstar_cal",  # 実験値によるc*
                "Cstar_effi",  # c*効率
                "Cstar_cal_ma",  # 実験値によるc*の移動平均値
                "Cstar_effi_ma",  # 移動平均値によるc*効率
                "Cstar_cal_mm",  # 実験値によるc*の移動中央値
                "Cstar_effi_mm",  # 移動中央値によるc*効率
                "Den",  # 燃焼室内密度
                "ts",  # 推進剤滞在時間
                "Dt",  # スロート径
                "Vc",  # 燃焼室容積
                "L*",  # 燃焼室特性長さ
                "O/F",  # 混合比
                "RHO",  # 推進剤密度
                "Slect B/M"  # モード
            ], 
            [  # 単位
                "-",  # 実験番号
                "s",  # 平均取得開始時間
                "s",  # 平均取得終了時間
                "MPaA",  # 供給圧力
                "MPaA",  # 直上圧力
                "MPaA",  # 燃焼室内圧力
                "℃",  # 燃焼室内温度
                "g/s",  # 質量流量
                "g",  # 推進剤使用量
                "g",  # 推進剤使用量の合計
                "-",  # ceaによる推力係数
                "-",  # 効率をかけた実際の推力係数
                "mN",  # 推力
                "s",  # 比推力
                "m/s",  # ceaによるc*
                "m/s",  # 実験値によるc*
                "-",  # c*効率
                "m/s",  # 実験値によるc*の移動平均値
                "-",  # 移動平均値によるc*効率
                "m/s",  # 実験値によるc*の移動中央値
                "-",  # 移動中央値によるc*効率
                "g/cm^3",  # 燃焼室内密度
                "s",  # 推進剤滞在時間
                "mm",  # スロート径
                "mm^3",  # 燃焼室容積
                "mm",  # 燃焼室特性長さ
                "-",  # 混合比
                "g/cm^3",  # 推進剤密度
                "-"  # モード
            ]
        ]
        
        result_data_ave.append(
            [  # 各種実験データ
                dirs,  # 実験番号
                (Static_start_num - (Pre_TRG * Interval)) / Interval,  # 平均取得開始時間
                (Static_end_num - (Pre_TRG * Interval)) / Interval,  # 平均取得終了時間
                supply_pressure_ave,  # 供給圧力
                above_pressure_ave,  # 直上圧力
                chamber_pressure_ave,  # 燃焼室内圧力
                chamber_temperature_ave,  # 燃焼室内温度
                flow_rate_ave,  # 質量流量
                total_throughput,  # 推進剤使用量
                self.total_throughput_sum[len(self.total_throughput_sum)-1],  # 推進剤使用量の合計
                cf_cea_ave,  # ceaによる推力係数
                cf_act_ave,  # 効率をかけた実際の推力係数
                thrust_ave,  # 推力
                isp_vac_ave,  # 比推力
                cstar_cea_ave,  # ceaによるc*
                cstar_cal_ave,  # 実験値によるc*
                cstar_effi_ave,  # c*効率
                cstar_cal_ma_ave,  # 実験値によるc*の移動平均値
                cstar_effi_ma_ave,  # 移動平均値によるc*効率
                cstar_cal_mm_ave,  # 実験値によるc*の移動中央値
                cstar_effi_mm_ave,  # 移動中央値によるc*効率
                density_ave,  # 燃焼室内密度
                stay_time_ave,  # 推進剤滞在時間
                Dt,  # スロート径
                Vc,  # 燃焼室容積
                Lster,  # 燃焼室特性長さ
                MR,  # 混合比
                OF_RHO,  # 推進剤密度
                sel_bm  # モード
            ]
        )

        with open(filename_result_ave, "a", newline="") as f:  # まずファイルを作成
            writer = csv.writer(f)
        with open(filename_result_ave, newline="") as f:  # ファイルを読む
            r = f.read()
        with open(filename_result_ave, "a", newline="") as f:  # csvで平均値を保存
            writer = csv.writer(f)
            if r == "":  # ファイルの中身が空の場合は，ヘッダーを追加
                writer.writerow(result_data_ave[0])  # データ名を記入
                writer.writerow(result_data_ave[1])  # 単位を記入
            writer.writerow(result_data_ave[2])  # 実験データを記入
        # ---------------------

        # 計算に用いたデータを全てcsvで出力
        result_data_all = [
            [
                "Time",  # 噴射時間
                "Pt[MPaA]",  # 供給圧力
                "Pa[MPaA]",  # 直上圧力
                "Pc[MPaA]",  # 燃焼室圧力
                "Tc[℃]",  # 燃焼室内温度
                "Mmfr[g/s]",  # 質量流量
                "Total[g]",  # 推進剤使用量
                "Cf_cea[-]",  # ceaによる推力係数
                "Cf_act[-]",  # 効率をかけた実際の推力係数
                "F[mN]",  # 推力
                "Isp[sec]",  # 比推力
                "Cstar_cea[m/s]",  # ceaによるc*
                "Cater_cal[m/s]",  # 実験値によるc*
                "Cstar_effi[-]",  # c*効率
                "Cstar_ma[m/s]",  # 実験値によるc*の移動平均値
                "Cstar_effi_ma[-]",  # 移動平均値によるc*効率
                "Cstar_mm[m/s]",  # 実験値によるc*の移動中央値
                "Cstar_effi_ma[-]",  # 移動中央値によるc*効率
                "Den[g/cm^3]",  # 燃焼室内密度
                "ts[s]",  # 推進剤滞在時間
                "Dt[mm]",  # スロート径
                "Vc[mm^3]",  # 燃焼室容積
                "L*[mm]",  # 燃焼室特性長さ
                "O/F[-]",  # 混合比
                "RHO[g/cm^3]",  # 推進剤密度
                "Slect B/M[-]", # モード
            ]
        ]
        for i in range(len(self.valve_data)):
            result_data_all.append(
                [
                    self.x[i],  # 噴射時間
                    self.supply_pressure_data[i],  # 供給圧力
                    self.above_pressure_data[i],  # 直上圧力
                    self.chamber_pressure_data[i],  # 燃焼室圧力
                    self.chamber_temperature_data[i],  # 燃焼室内温度
                    self.flow_rate_data[i],  # 質量流量
                    self.total_throughput_data[i],  # 推進剤使用量
                    self.cf_cea_data[i],  # ceaによる推力係数
                    self.cf_act_data[i],  # 効率をかけた実際の推力係数
                    self.thrust_data[i],  # 推力
                    self.isp_vac_data[i],  # 比推力
                    self.cstar_cea_data[i],  # ceaによるc*
                    self.cstar_cal_data[i],  # 実験値によるc*
                    self.cstar_effi_data[i],  # c*効率
                    self.cstar_cal_ma_data[i],  # 実験値によるc*の移動平均値
                    self.cstar_effi_ma_data[i],  # 移動平均値によるc*効率
                    self.cstar_cal_mm_data[i],  # 実験値によるc*の移動中央値
                    self.cstar_effi_mm_data[i],  # 移動中央値によるc*効率
                    self.density_data[i],  # 燃焼室内密度
                    self.stay_time_data[i],  # 推進剤滞在時間
                    Dt,  # スロート径
                    Vc,  # 燃焼室容積
                    Lster,  # 燃焼室特性長さ
                    MR,  # 混合比
                    OF_RHO,  # 推進剤密度
                    sel_bm  # モード
                ]
            )
        with open(filename_result_all + "_" + dirs + ".csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(result_data_all)
        # --------------------------

    def moving_ave(self, data_list, moving_num):
        _list = []
        _data =[]
        for i in range(len(data_list)):
            _list.append(data_list[i])
            if len(_list) >= moving_num + 1:
                del _list[0]
            _list_mea = statistics.mean(_list)
            _data.append(_list_mea)
        return _data 
    
    def moving_med(self, data_list, moving_num):
        _list = []
        _data =[]
        for i in range(len(data_list)):
            _list.append(data_list[i])
            if len(_list) >= moving_num + 1:
                del _list[0]
            _list_med = statistics.median(_list)
            _data.append(_list_med)
        return _data

