# -*- coding: utf-8 -*-
from rocketcea.cea_obj import CEA_Obj, add_new_oxidizer
import csv
import os
import numpy as np
import matplotlib.pyplot as plt

card_str = """
oxid H2O2(L) H 2 O 2  wt%=60.00
h,cal=-44880.0     t(k)=298.15  rho.g/cc=1.407
oxid = WATER H 2.0 O 1.0 wt%= 40.0
h,cal=-68317. t(k)=298.15 rho.g/cc=1.0
"""
add_new_oxidizer( '60_H2O2', card_str )
ispObj = CEA_Obj( oxName='60_H2O2', fuelName='C2H5OH')

path = os.getcwd()
filename = 'C:\\Users\\SAHARA-7\\workspace\\cal-prop-cea\\01_0.6MPaA_30s\\auto$0.csv'
filename_result_ave = 'C:\\Users\\SAHARA-7\\workspace\\cal-prop-cea\\01_0.6MPaA_30s\\result_ave.csv'
filename_result_all = 'C:\\Users\\SAHARA-7\\workspace\\cal-prop-cea\\01_0.6MPaA_30s\\result_all.csv'
#filename = '/home/haru-11/cal-prop-cea/01_0.6MPaA_30s/auto$0.csv'

#csv読み込み
with open(filename, newline='', encoding="shift-jis") as f:
    reader = csv.reader(f)
    data_csv = [row for row in reader] #data start at 62rows

data_len = len(data_csv) - 66
header = data_csv[61]
print(data_len)
print(data_csv[data_len+62])
print(header[0])
#--------------

#変数定義
At_diameter = 1.0 #[mm]
Interval = 100 #[Hz] サンプリング周波数
OF_RHO = 1.24 #推進剤の密度
Pre_TRG = 2 #[sec]バルブ開の前後何秒グラフ描写,データ生成するか？
Valve_TRG = 3.00 #[V]バルブの立ち上がりのエッジトリガの閾値
Statick_ratio = 0.2 #[-]定常区間の割合を指定

valve_column = 9 #CSVの何列目かを書く．A列が0，B列が1である．
Pc_column = 3
Pt_column = 2
Pa_column = 4
flow_rate_column = 5
Tc_column = 8

At = ((At_diameter/2.0)*(At_diameter/2.0))*(np.pi)
valve_data = []
chamber_pressure_data = []
supply_pressure_data = []
above_pressure_data = []
flow_rate_data = []
chamber_temperature_data = []
cstar_data = []
cf_data = []
thrust_data = []
isp_vac_data = []
result_data_ave = [["No","start","end","Pt_A","Pa_A","Pc_A","Pt_A","Mmfr_A","Isp_A","F_A"]]
#---------------

#計算するデータ範囲取得
valve_open_num = 0
plt_start_num = 0
plt_end_num = 0
for i in range(data_len):
    if float(data_csv[i+62][9]) > Valve_TRG and valve_open_num == 0:
        valve_open_num = i + 62
        plt_start_num = valve_open_num - (Pre_TRG*Interval)
    if float(data_csv[i+62][9]) < 1.00 and plt_start_num > 0 and plt_end_num == 0:
        plt_end_num = i+ 62 + (Pre_TRG*Interval)
#--------------------------

#各データをlistに入れる．
for i in range(plt_start_num,plt_end_num):
    valve_data.append(float(data_csv[i][valve_column]))
    chamber_pressure_data.append(float(data_csv[i][Pc_column]))
    supply_pressure_data.append(float(data_csv[i][Pt_column]))
    above_pressure_data.append(float(data_csv[i][Pa_column]))
    flow_rate_data.append(float(data_csv[i][flow_rate_column]))
    chamber_temperature_data.append(float(data_csv[i][Tc_column]))

    pambcf = ispObj.getFrozen_PambCf(Pamb=0.000001, Pc=(float(data_csv[i][Pc_column])*145.038), MR=7.4, eps=100.0, frozenAtThroat=0)
    vac_cstar_tc = ispObj.get_IvacCstrTc((float(data_csv[i][Pc_column])*145.038), MR=7.4, eps=100.0, frozen=1, frozenAtThroat=0) 
    cstar_data.append(float(vac_cstar_tc[1])*0.3048)
    cf_data.append(float(pambcf[0]))
    thrust_data.append(float(data_csv[i][Pc_column])*float(pambcf[0])*At*1000)
    if i < (plt_start_num+(Pre_TRG*Interval)) or i > (plt_end_num-(Pre_TRG*Interval)):
        isp_vac_data.append(0.0)
    else:
        isp_vac_data.append(float(data_csv[i][3])*float(pambcf[0])*At*1000/(float(data_csv[i][flow_rate_column])*OF_RHO*9.80665))
x = np.arange((0-Pre_TRG), len(valve_data)/Interval-Pre_TRG, 1/Interval) #バルブデータから時間を生成
#------------------------------

#定常区間の平均値を取得
Static_start_num = int((plt_end_num - plt_start_num - (Pre_TRG*Interval*2))*(1-Statick_ratio)) + int(Pre_TRG*Interval)
Static_end_num = int(plt_end_num - plt_start_num - (Pre_TRG*Interval*2)) + int(Pre_TRG*Interval)
chamber_pressure_ave = sum(chamber_pressure_data[Static_start_num : Static_end_num])/len(chamber_pressure_data[Static_start_num : Static_end_num])
supply_pressure_ave = sum(supply_pressure_data[Static_start_num : Static_end_num])/len(supply_pressure_data[Static_start_num : Static_end_num])
above_pressure_ave = sum(above_pressure_data[Static_start_num : Static_end_num])/len(above_pressure_data[Static_start_num : Static_end_num])
chamber_temperature_ave = sum(chamber_temperature_data[Static_start_num : Static_end_num])/len(chamber_temperature_data[Static_start_num : Static_end_num])
flow_rate_ave = sum(flow_rate_data[Static_start_num : Static_end_num])/len(flow_rate_data[Static_start_num : Static_end_num])
isp_vac_ave = sum(isp_vac_data[Static_start_num : Static_end_num])/len(isp_vac_data[Static_start_num : Static_end_num])
thrust_ave = sum(thrust_data[Static_start_num : Static_end_num])/len(thrust_data[Static_start_num : Static_end_num])

#print(Static_start_num,Static_end_num)
result_data_ave.append([1,(Static_start_num-(Pre_TRG*Interval))/Interval, (Static_end_num-(Pre_TRG*Interval))/Interval, supply_pressure_ave, above_pressure_ave, chamber_pressure_ave, chamber_temperature_ave, flow_rate_ave, isp_vac_ave, thrust_ave])
#chamber_pressure_ave = sum(chamber_pressure_data[((plt_end_num - plt_start_num - (Pre_TRG*Interval*2))*(1-Statick_ratio)) : (plt_end_num - plt_start_num - (Pre_TRG*Interval*2))]) / len(chamber_pressure_data[((plt_end_num - plt_start_num - (Pre_TRG*Interval*2))*(1-Statick_ratio)) : (plt_end_num - plt_start_num - (Pre_TRG*Interval*2))])

with open(filename_result_ave, 'w', newline='') as f: #csvで平均値を保存
    writer = csv.writer(f)
    writer.writerows(result_data_ave)
#---------------------

#計算に用いたデータを全てcsvで出力
result_data_all = [["Time","Pt[MPaA]","Pa[MPaA]","Pc[MPaA]","Tc[K]","Mmfr[ml/s]","Isp[sec]","F[mN]"]]
for i in range(len(valve_data)):
    result_data_all.append([x[i], supply_pressure_data[i], above_pressure_data[i], chamber_pressure_data[i],chamber_temperature_data[i],flow_rate_data[i],isp_vac_data[i],thrust_data[i]])
with open(filename_result_all, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(result_data_all)
#--------------------------


#グラフ描写
#全体のグラフ設定
fig1 = plt.figure(figsize=[8,4.5])
print(x)
print(len(x),len(chamber_pressure_data))
#print(isp_vac_data)
#一つ目のグラフ描写
ax1_1 = fig1.add_subplot(1, 1, 1)
ax1_1.plot(x,chamber_pressure_data, color = "red", label = "pressure")
#ax1_1.scatter(x,chamber_pressure_data, c=None, marker=None, linewidths=1)
#ax1.legend(['pressure']) # 凡例の表示
#ax.set_xlim(0, 8)  # プロットのX範囲
ax1_1.set_ylim(0, 0.7) # プロットのY範囲
ax1_1.set_xlabel('time[sec]')
ax1_1.set_ylabel('camber pressure[MPaA]')

ax1_2 = ax1_1.twinx()
ax1_2.plot(x,chamber_temperature_data, color = "green", label = "temp")
#ax2.legend(['valve']) # 凡例の表示
#ax.set_xlim(0, 8)  # プロットのX範囲
ax1_2.set_ylim(0, 1500) # プロットのY範囲
ax1_2.set_ylabel('camber temperature[K]')

ax1_3 = ax1_1.twinx()
ax1_3.plot(x,valve_data, color = "blue", label = "valve")
#ax2.legend(['valve']) # 凡例の表示
#ax.set_xlim(0, 8)  # プロットのX範囲
ax1_3.set_ylim(0, 6) # プロットのY範囲
ax1_3.axis("off")

#凡例
h1, l1 = ax1_1.get_legend_handles_labels()
h2, l2 = ax1_2.get_legend_handles_labels()
ax1_1.legend(h1+h2, l1+l2)

plt.savefig(path + "/fig1.png")
plt.clf()

#グラフ描写の二つ目
ax2_1 = fig1.add_subplot(1, 1, 1)
ax2_1.plot(x,chamber_pressure_data, color = "red", label = "pressure")
#ax1.legend(['pressure']) # 凡例の表示
#ax.set_xlim(0, 8)  # プロットのX範囲
ax2_1.set_ylim(0, 0.7) # プロットのY範囲
ax2_1.set_xlabel('time[sec]')
ax2_1.set_ylabel('camber pressure[MPaA]')

ax2_2 = ax2_1.twinx()
ax2_2.plot(x,flow_rate_data, color = "c", label = "flow_rate")
#ax2.legend(['valve']) # 凡例の表示
#ax.set_xlim(0, 8)  # プロットのX範囲
ax2_2.set_ylim(0, 2) # プロットのY範囲
ax2_2.set_ylabel('flow rate[ml/s]')

ax2_3 = ax2_1.twinx()
ax2_3.plot(x,valve_data, color = "blue", label = "valve")
#ax2.legend(['valve']) # 凡例の表示
#ax.set_xlim(0, 8)  # プロットのX範囲
ax2_3.set_ylim(0, 6) # プロットのY範囲
ax2_3.axis("off")

#凡例
h1, l1 = ax2_1.get_legend_handles_labels()
h2, l2 = ax2_2.get_legend_handles_labels()
ax2_1.legend(h1+h2, l1+l2)

plt.savefig(path + "/fig2.png")
plt.clf()

#グラフ描写の３つ目
ax3_1 = fig1.add_subplot(1, 1, 1)
ax3_1.plot(x,cstar_data, color = "k", label = "cstar")
#ax1.legend(['pressure']) # 凡例の表示
#ax.set_xlim(0, 8)  # プロットのX範囲
ax3_1.set_ylim(1313, 1317) # プロットのY範囲
ax3_1.set_xlabel('time[sec]')
ax3_1.set_ylabel('cstar[m/s]')

ax3_2 = ax3_1.twinx()
ax3_2.plot(x,cf_data, color = "c", label = "cf")
#ax2.legend(['valve']) # 凡例の表示
#ax.set_xlim(0, 8)  # プロットのX範囲
ax3_2.set_ylim(1.856, 1.860) # プロットのY範囲
ax3_2.set_ylabel('cf[-]')

ax3_3 = ax3_1.twinx()
ax3_3.plot(x,valve_data, color = "blue", label = "valve")
#ax2.legend(['valve']) # 凡例の表示
#ax.set_xlim(0, 8)  # プロットのX範囲
ax3_3.set_ylim(0, 6) # プロットのY範囲
ax3_3.axis("off")

#凡例
h1, l1 = ax3_1.get_legend_handles_labels()
h2, l2 = ax3_2.get_legend_handles_labels()
ax3_1.legend(h1+h2, l1+l2)

#凡例
h1, l1 = ax2_1.get_legend_handles_labels()
h2, l2 = ax2_2.get_legend_handles_labels()
ax2_1.legend(h1+h2, l1+l2)
plt.savefig(path + "/fig3.png")
plt.clf()

#グラフ描写の4つ目
ax4_1 = fig1.add_subplot(1, 1, 1)
ax4_1.plot(x,thrust_data, color = "m", label = "thrust")
#ax1.legend(['pressure']) # 凡例の表示
#ax.set_xlim(0, 8)  # プロットのX範囲
ax4_1.set_ylim(0, 1000) # プロットのY範囲
ax4_1.set_xlabel('time[sec]')
ax4_1.set_ylabel('thrust[mN]')

ax4_2 = ax4_1.twinx()
ax4_2.plot(x,isp_vac_data, color = "k", label = "isp")
#ax2.legend(['valve']) # 凡例の表示
#ax.set_xlim(0, 8)  # プロットのX範囲
ax4_2.set_ylim(0, 300) # プロットのY範囲
ax4_2.set_ylabel('Isp[sec]')

ax4_3 = ax4_1.twinx()
ax4_3.plot(x,valve_data, color = "blue", label = "valve")
#ax2.legend(['valve']) # 凡例の表示
#ax.set_xlim(0, 8)  # プロットのX範囲
ax4_3.set_ylim(0, 6) # プロットのY範囲
ax4_3.axis("off")

#凡例
h1, l1 = ax4_1.get_legend_handles_labels()
h2, l2 = ax4_2.get_legend_handles_labels()
ax4_1.legend(h1+h2, l1+l2)
plt.savefig(path + "/fig4.png")

plt.show()
#plt.savefig('result.png')
