from math import cos
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

ispObj_2 = CEA_Obj(oxName="60_H2O2", fuelName="C2H5OH")  # 二液
ispObj_1 = CEA_Obj(propName="60_H2O2_mono")  # 一液


class Gen_data:
    def __init__(self):
        print("Active Generate data")
        self.total_throughput_sum = []
        self.chamber_pressure_ave_sum = [] #謎のリストが定義されている．

    def gen_data(self, filename_data, filename_result_all, filename_result_ave, filename_result_ave2,filename_result_std, dirs, sel_bm): #標準偏差，平均値2を追加
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

        # ４．【毎回確認】変数定義

        At_diameter =1.0  # [mm]

        Nozzle_cone_half_ang = 15 #ノズルコーン半頂角,Θ
        Thrust_coefficient_effi = 0.983 #推力係数効率
        Interval = 100  # [Hz] サンプリング周波数
        O_RHO = 1.24       #60%H2O2の場合は1.24，水の場合は1.00
        F_RHO = 1.00       #エタノールの場合は0.79，水の場合は1.00
        MR = 0.0     #OFを入力．一液の場合は0を記入
        Pre_TRG = 2  # [sec]バルブ開の前後何秒グラフ描写,データ生成するか？（intのみ）
        Valve_TRG = 3.002  # [V]バルブの立ち上がりのエッジトリガの閾値
        Statick_ratio = float(2/10)  # [-]定常区間の割合を指定
        moving_average_num = 5 #移動平均の個数

        valve_column = 9  # バルブ電圧のカラムが，CSVの何列目かを書く．A列が0，B列が1である．
        Pc_column = 5  # チャンバ圧力のカラム
        Pt_column = 2  # 供給圧力がのカラム
        Pa_column = 4  # 直上圧力のカラム
        flow_rate_column = 6  # 流量のカラム
        Tc_column =  8# チャンバ下流の温度のカラム
        TcM_column = 8 # チャンバ中流の温度のカラム
        TcU_column = 8 # チャンバ上流の温度のカラム


        if MR > 0:
            OF_RHO = (O_RHO * F_RHO) * (1 + MR)/(O_RHO + F_RHO * MR)
        elif MR == 0:
            OF_RHO = O_RHO  # 推進剤の密度,20241024修正「1.00→O_RHO」
        else:
            print("O/F ERROR")
        nozzle_factor = 0.5*(1+ cos(Nozzle_cone_half_ang/180*3.141592)) #ノズル修正係数の計算


        result_data_ave = [  # 平均値をcsvにまとめる時のヘッダー※z-のこと
            [
                "No",
                "start[s]",
                "end[s]",
                "Pt_A[MPaA]",
                "Pa_A[MPaA]",
                "Pc_A[MPaA]",
                "Tc_A[℃]",
                "TcM_A[℃]",
                "TcU_A[℃]",
                "Mmfr_A[g/s]",
                "Total[g]",
                "Sum[g]",
                "Cf_cea[-]",
                "Cf_act[-]",
                "Cstar_act[m/s]",
                "Cstar_cea[-]",
                "Cstar_effi[-]",
                "Isp_A[s]",
                "F_A[mN]",
                "start[s]",
                "end[s]",
                "Itotal_valveopenperiod[mNs]",
                "AT[mm]", At_diameter, 
                "O/F[-]", MR, 
                "RHO[g/ml]",OF_RHO,
                "Slect B/M", sel_bm
            ]
        ]

        result_data_ave2 = [  # 平均値2をcsvにまとめる時のヘッダー※z^のこと
            [
                "No",
                "start[s]",
                "end[s]",
                "Pt_A[MPaA]",
                "Pa_A[MPaA]",
                "Pc_A[MPaA]",
                "Tc_A[℃]",
                "TcM_A[℃]",
                "TcU_A[℃]",
                "Mmfr_A[g/s]",
                "Total[g]",
                "Sum[g]",
                "Cf_cea[-]",
                "Cf_act[-]",
                "Cstar_act[m/s]",
                "Cstar_cea[-]",
                "Cstar_effi[-]",
                "Isp_A[s]",
                "F_A[mN]",
                "AT[mm]", At_diameter, 
                "O/F[-]", MR, 
                "RHO[g/ml]",OF_RHO,
                "Slect B/M", sel_bm
            ]
        ]

        result_data_std = [  # 標準偏差をcsvにまとめる時のヘッダー
            [
                "No",
                "start[s]",
                "end[s]",
                "Pt_A[MPaA]",
                "Pa_A[MPaA]",
                "Pc_A[MPaA]",
                "Tc_A[℃]",
                "TcM_A[℃]",
                "TcU_A[℃]",
                "Mmfr_A[g/s]",
                "Total[g]",
                "Sum[g]",
                "Cf_cea[-]",
                "Cf_act[-]",
                "Cstar_act[m/s]",
                "Cstar_cea[-]",
                "Cstar_effi[-]",
                "Isp_A[s]",
                "F_A[mN]",
                "start[s]",
                "end[s]",
                "Itotal_valveopenperiod[mNs]",
                "AT[mm]", At_diameter, 
                "O/F[-]", MR, 
                "RHO[g/ml]",OF_RHO,
                "Slect B/M", sel_bm
            ]
        ]
        # ---------------------------

        At = ((At_diameter / 2.0) * (At_diameter / 2.0)) * (np.pi) #[mm^2]
        self.valve_data = []
        self.chamber_pressure_data = []
        self.supply_pressure_data = []
        self.above_pressure_data = []
        self.flow_rate_data = []
        self.chamber_temperature_data = []
        self.chamber_Middle_temperature_data = []
        self.chamber_Upper_temperature_data = []
        self.cstar_data = []
        self.cstar_cal_data = []
        self.cstar_cal_ma_data = []
        self.cstar_effi_data = []
        self.cstar_effi_ma_data = []
        self.cf_cea_data = []
        self.cf_act_data = []
        self.thrust_data = []
        self.isp_vac_data = []
        self.total_throughput_data = []
        total_throughput = 0.0
        self.impulse_data=[]


        # 計算するデータ範囲取得
        valve_open_num = 0
        valve_close_num = 0
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
                float(data_csv[i + 62][valve_column]) < Valve_TRG
                and plt_start_num > 0
                and plt_end_num == 0
            ):
                valve_close_num = i + 62
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
            self.chamber_Middle_temperature_data.append(float(data_csv[i][TcM_column]))
            self.chamber_Upper_temperature_data.append(float(data_csv[i][TcU_column]))

            if sel_bm == 2:
                pambcf = ispObj_2.getFrozen_PambCf(
                    Pamb=0.000001,
                    Pc=(float(data_csv[i][Pc_column]) * 145.038),
                    MR=MR,
                    eps=100.0,
                    frozenAtThroat=0,
                )
                vac_cstar_tc = ispObj_2.get_IvacCstrTc(
                    (float(data_csv[i][Pc_column]) * 145.038),
                    MR=MR,
                    eps=100.0,
                    frozen=1,
                    frozenAtThroat=0,
                )
            elif sel_bm == 1:
                vac_cstar_tc = ispObj_1.get_IvacCstrTc(
                    (float(data_csv[i][Pc_column]) * 145.038),
                    eps=100.0,
                    frozen=0,
                    frozenAtThroat=0,
                )
                pambcf = ispObj_1.get_PambCf(Pamb=0.000001, Pc=(float(data_csv[i][Pc_column]) * 145.038), eps=100.0)
                #pambcf = ispObj_1.getFrozen_PambCf(Pamb=14.7 , Pc=(float(data_csv[i][Pc_column]) * 145.038), eps=100.0, frozenAtThroat=0)
            else:
                print("select MR(O/F) error")


            #print(str(i)+",cf:"+str(pambcf[0])+","+str(vac_cstar_tc))

            self.cstar_data.append(float(vac_cstar_tc[1]) * 0.3048)
            self.cf_cea_data.append(float(pambcf[0]))
            self.cf_act_data.append(float(pambcf[0])*nozzle_factor*Thrust_coefficient_effi)
            self.thrust_data.append(
            float(data_csv[i][Pc_column]) * float(pambcf[0])*nozzle_factor*Thrust_coefficient_effi * At * 1000
            )
            self.impulse_data.append(float(data_csv[i][Pc_column]) * float(pambcf[0])*nozzle_factor*Thrust_coefficient_effi * At * 1000/Interval)

            if (    #流量はバルブオン以外は0とする．
                i < (plt_start_num + (Pre_TRG * Interval))
                or i > (plt_end_num - (Pre_TRG * Interval))
                or (float(data_csv[i][flow_rate_column]) == 0.0)
            ):
                self.isp_vac_data.append(0.0)
                self.cstar_cal_data.append(0.0)
            else:
                self.isp_vac_data.append(
                    (self.thrust_data[i-plt_start_num])
                    / (self.flow_rate_data[i-plt_start_num] * 9.80665)
                )
                self.cstar_cal_data.append(
                    self.chamber_pressure_data[i-plt_start_num]*At
                    / (self.flow_rate_data[i-plt_start_num]/1000)
                )

            total_throughput = total_throughput + self.flow_rate_data[i-plt_start_num]*(1.0/Interval)
            self.total_throughput_data.append(total_throughput)
            self.cstar_effi_data.append(self.cstar_cal_data[i-plt_start_num]/self.cstar_data[i-plt_start_num])

        self.x = np.arange(
            (0 - Pre_TRG), len(self.valve_data) / Interval - Pre_TRG, 1 / Interval
        )  # バルブデータから時間を生  

        self.cstar_cal_ma_data = self.moving_ave(self.cstar_cal_data, moving_average_num) #移動平均を出す
        for i in range(len(self.x)):
            self.cstar_effi_ma_data.append(self.cstar_cal_ma_data[i] / self.cstar_data[i])
        
        # ------------------------------

        # 定常区間の平均値を取得※ここでの平均値はz-のこと(zは多変数関数だが，それぞれ測定値a,b,c...から逐次zを計算し，平均値求める．zの母集団？が分かっている．自分の修論での定義と違う．)
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
        chamber_Middle_temperature_ave = sum(
            self.chamber_Middle_temperature_data[Static_start_num:Static_end_num]
        ) / len(self.chamber_temperature_data[Static_start_num:Static_end_num])
        chamber_Upper_temperature_ave = sum(
            self.chamber_Upper_temperature_data[Static_start_num:Static_end_num]
        ) / len(self.chamber_temperature_data[Static_start_num:Static_end_num])
        flow_rate_ave = sum(self.flow_rate_data[Static_start_num:Static_end_num]) / len(
            self.flow_rate_data[Static_start_num:Static_end_num]
        )
        isp_vac_ave = sum(self.isp_vac_data[Static_start_num:Static_end_num]) / len(
            self.isp_vac_data[Static_start_num:Static_end_num]
        )
        cstar_act_ave = sum(self.cstar_cal_data[Static_start_num:Static_end_num]) / len(
            self.cstar_cal_data[Static_start_num:Static_end_num]
        )
        cstar_cea_ave = sum(self.cstar_data[Static_start_num:Static_end_num]) / len(
            self.cstar_data[Static_start_num:Static_end_num]
        )
        cstar_effi_ave = cstar_act_ave / cstar_cea_ave
        thrust_ave = sum(self.thrust_data[Static_start_num:Static_end_num]) / len(
            self.thrust_data[Static_start_num:Static_end_num]
        )
        cf_act_ave = sum(self.cf_act_data[Static_start_num:Static_end_num]) / len(
            self.cf_act_data[Static_start_num:Static_end_num]
        )
        cf_cea_ave = sum(self.cf_cea_data[Static_start_num:Static_end_num]) / len(
            self.cf_cea_data[Static_start_num:Static_end_num]
        )

        #バルブ開区間の合計を算出
        valve_open_evaluation_num=int(Pre_TRG*Interval)
        valve_close_evaluation_num=int(Pre_TRG*Interval)+int(valve_close_num-valve_open_num)
        total_impulse= sum(self.impulse_data[valve_open_evaluation_num:valve_close_evaluation_num])
        
        if len(self.total_throughput_sum) == 0:
            _tt = total_throughput
        else:
            _tt = self.total_throughput_sum[len(self.total_throughput_sum)-1] + total_throughput
        self.total_throughput_sum.append(_tt)
        self.chamber_pressure_ave_sum.append(chamber_pressure_ave) #謎のリストに燃焼室圧力の平均が入れられている謎．特にこれで計算はしていなさそう．

        result_data_ave.append(
            [
                dirs,
                (Static_start_num - (Pre_TRG * Interval)) / Interval,
                (Static_end_num - (Pre_TRG * Interval)) / Interval,
                supply_pressure_ave,
                above_pressure_ave,
                chamber_pressure_ave,
                chamber_temperature_ave,
                chamber_Middle_temperature_ave,
                chamber_Upper_temperature_ave,
                flow_rate_ave,
                total_throughput,
                self.total_throughput_sum[len(self.total_throughput_sum)-1],
                cf_cea_ave,
                cf_act_ave,
                cstar_act_ave,
                cstar_cea_ave,
                cstar_effi_ave,
                isp_vac_ave,
                thrust_ave,
                (valve_open_evaluation_num-(Pre_TRG*Interval))/Interval,
                (valve_close_evaluation_num-(Pre_TRG*Interval))/Interval,
                total_impulse,
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


        # 定常区間の平均値2を取得※ここでの平均値はz^のこと(zは多変数関数だが，それぞれ測定値a,b,c...の平均値を取ってからzの平均値求める．自分の修論での定義と同じ．)
        chamber_pressure_ave2 = sum(
            self.chamber_pressure_data[Static_start_num:Static_end_num]
        ) / len(self.chamber_pressure_data[Static_start_num:Static_end_num])
        supply_pressure_ave2 = sum(
            self.supply_pressure_data[Static_start_num:Static_end_num]
        ) / len(self.supply_pressure_data[Static_start_num:Static_end_num])
        above_pressure_ave2 = sum(
            self.above_pressure_data[Static_start_num:Static_end_num]
        ) / len(self.above_pressure_data[Static_start_num:Static_end_num])
        chamber_temperature_ave2 = sum(
            self.chamber_temperature_data[Static_start_num:Static_end_num]
        ) / len(self.chamber_temperature_data[Static_start_num:Static_end_num])
        chamber_Middle_temperature_ave2 = sum(
            self.chamber_Middle_temperature_data[Static_start_num:Static_end_num]
        ) / len(self.chamber_temperature_data[Static_start_num:Static_end_num])
        chamber_Upper_temperature_ave2 = sum(
            self.chamber_Upper_temperature_data[Static_start_num:Static_end_num]
        ) / len(self.chamber_temperature_data[Static_start_num:Static_end_num])
        flow_rate_ave2 = sum(self.flow_rate_data[Static_start_num:Static_end_num]) / len(
            self.flow_rate_data[Static_start_num:Static_end_num]
        )
        pambcf2 = ispObj_1.get_PambCf(Pamb=0.000001, Pc=(float(chamber_pressure_ave2) * 145.038), eps=100.0)
        cf_cea_ave2 = pambcf2[0]
        cf_act_ave2 = cf_cea_ave2*nozzle_factor*Thrust_coefficient_effi
        vac_cstar_tc2 = ispObj_1.get_IvacCstrTc(
                    (float(chamber_pressure_ave2) * 145.038),
                    eps=100.0,
                    frozen=0,
                    frozenAtThroat=0,
                )
        thrust_ave2 = float(chamber_pressure_ave2) * cf_act_ave2 * At * 1000
        if flow_rate_ave2 == 0:
            cstar_ave2 = 0
            isp_vac_ave2 = 0
        else:
            cstar_ave2 = chamber_pressure_ave2*At/(flow_rate_ave2/1000)
            isp_vac_ave2 = thrust_ave2/(flow_rate_ave2* 9.80665)
        
        cstar_cea_ave2 =float(vac_cstar_tc2[1])* 0.3048
        cstar_effi_ave2 = cstar_ave2 / cstar_cea_ave2

        result_data_ave2.append(
            [
                dirs,
                (Static_start_num - (Pre_TRG * Interval)) / Interval,
                (Static_end_num - (Pre_TRG * Interval)) / Interval,
                supply_pressure_ave2,
                above_pressure_ave2,
                chamber_pressure_ave2,
                chamber_temperature_ave2,
                chamber_Middle_temperature_ave2,
                chamber_Upper_temperature_ave2,
                flow_rate_ave2,
                total_throughput,
                self.total_throughput_sum[len(self.total_throughput_sum)-1],
                cf_cea_ave2,
                cf_act_ave2,
                cstar_ave2,
                cstar_cea_ave2,
                cstar_effi_ave2,
                isp_vac_ave2,
                thrust_ave2,
            ]
        )

        with open(filename_result_ave2, "a", newline="") as f:  # まずファイルを作成
            writer = csv.writer(f)
        with open(filename_result_ave2, newline="") as f:  # ファイルを読む
            r = f.read()
        with open(filename_result_ave2, "a", newline="") as f:  # csvで平均値を保存
            writer = csv.writer(f)
            if r == "":  # ファイルの中身が空の場合は，ヘッダーを追加
                writer.writerow(result_data_ave2[0])
            writer.writerow(result_data_ave2[1])

         # 定常区間の標準偏差を取得
        chamber_pressure_std = np.std(
            self.chamber_pressure_data[Static_start_num:Static_end_num]
        )
        supply_pressure_std = np.std(
            self.supply_pressure_data[Static_start_num:Static_end_num]
        )
        above_pressure_std = np.std(
            self.above_pressure_data[Static_start_num:Static_end_num]
        )
        chamber_temperature_std = np.std(
            self.chamber_temperature_data[Static_start_num:Static_end_num]
        )
        chamber_Middle_temperature_std = np.std(
            self.chamber_Middle_temperature_data[Static_start_num:Static_end_num]
        )
        chamber_Upper_temperature_std = np.std(
            self.chamber_Upper_temperature_data[Static_start_num:Static_end_num]
        )
        flow_rate_std = np.std(self.flow_rate_data[Static_start_num:Static_end_num]
        )
        isp_vac_std = np.std(self.isp_vac_data[Static_start_num:Static_end_num]
        )
        cstar_act_std = np.std(self.cstar_cal_data[Static_start_num:Static_end_num]
        )
        cstar_cea_std = np.std(self.cstar_data[Static_start_num:Static_end_num]
        )
        cstar_effi_std = cstar_act_ave / cstar_cea_ave
        thrust_std = np.std(self.thrust_data[Static_start_num:Static_end_num]
        )
        cf_act_std = np.std(self.cf_act_data[Static_start_num:Static_end_num]
        )
        cf_cea_std = np.std(self.cf_cea_data[Static_start_num:Static_end_num]
        )

        #バルブ開区間の合計を算出（？？間違いか？コピペしたからそのまま残っただけ？）
        result_data_std.append(
            [
                dirs,
                (Static_start_num - (Pre_TRG * Interval)) / Interval,
                (Static_end_num - (Pre_TRG * Interval)) / Interval,
                supply_pressure_std,
                above_pressure_std,
                chamber_pressure_std,
                chamber_temperature_std,
                chamber_Middle_temperature_std,
                chamber_Upper_temperature_std,
                flow_rate_std,
                total_throughput,
                self.total_throughput_sum[len(self.total_throughput_sum)-1],
                cf_cea_std,
                cf_act_std,
                cstar_act_std,
                cstar_cea_std,
                cstar_effi_std,
                isp_vac_std,
                thrust_std,
                (valve_open_evaluation_num-(Pre_TRG*Interval))/Interval,
                (valve_close_evaluation_num-(Pre_TRG*Interval))/Interval,
                total_impulse,
            ]
        )

        with open(filename_result_std, "a", newline="") as f:  # まずファイルを作成
            writer = csv.writer(f)
        with open(filename_result_std, newline="") as f:  # ファイルを読む
            r = f.read()
        with open(filename_result_std, "a", newline="") as f:  # csvで平均値を保存
            writer = csv.writer(f)
            if r == "":  # ファイルの中身が空の場合は，ヘッダーを追加
                writer.writerow(result_data_std[0])
            writer.writerow(result_data_std[1])
        # ---------------------

        # 計算に用いたデータを全てcsvで出力
        result_data_all = [
            [
                "Time",
                "Pt[MPaA]",
                "Pa[MPaA]",
                "Pc[MPaA]",
                "Tc[K]",
                "TcM[K]",
                "TcU[K]",
                "Mmfr[g/s]",
                "Total[g]",
                "Cf_cea[-]",
                "Cf_act[-]",
                "Cstar_CEA[sec]",
                "Cstar_cal[sec]",
                "Cstar_effi[-]",
                "Isp[sec]",
                "F[mN]",
                "Ibit[mNs]",
                "AT", At_diameter, 
                "O/F", MR,
                "RHO",OF_RHO,
                "selct B/M", sel_bm
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
                    self.chamber_Middle_temperature_data[i],
                    self.chamber_Upper_temperature_data[i],
                    self.flow_rate_data[i],
                    self.total_throughput_data[i],
                    self.cf_cea_data[i],
                    self.cf_act_data[i],
                    self.cstar_data[i],
                    self.cstar_cal_data[i],
                    self.cstar_effi_data[i],
                    self.isp_vac_data[i],
                    self.thrust_data[i],
                    self.impulse_data[i]
                ]
            )
        with open(filename_result_all + "_" + dirs + ".csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(result_data_all)
        # --------------------------

    def moving_ave(self, data_list, moving_average_num):
            #cstarの移動平均を求めてる．
            _data = []
            _d = np.array(data_list)
            _e = np.convolve(_d, np.ones(moving_average_num)/moving_average_num, mode='valid')
            _f = _e.tolist()
            if (moving_average_num) % 2 == 1:
                for i in range((moving_average_num-1)//2):
                    _data.append(data_list[i])
                for i in range(len(_f)):
                    _data.append(_f[i])
                for i in range(len(_data)-1, len(_data)-1 + ((moving_average_num-1)//2)):
                    _data.append(data_list[i])
            else:
                for i in range((moving_average_num)//2):
                    _data.append(data_list[i])
                for i in range(len(_f)):
                    _data.append(_f[i])
                for i in range(len(_data)-1 , len(_data) - 1 + ((moving_average_num-1)//2)):
                    _data.append(data_list[i])
            return _data

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
