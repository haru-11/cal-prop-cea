from rocketcea.cea_obj_w_units import CEA_Obj
from rocketcea.cea_obj import add_new_oxidizer, add_new_propellant
import scipy.constants as const
import math
from scipy import optimize

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

C_1 = CEA_Obj(propName="60_H2O2_mono", 
                   pressure_units='MPa', temperature_units='K', 
                   isp_units='sec', cstar_units='m/s', sonic_velocity_units='m/s', 
                   enthalpy_units='J/kg', density_units='kg/m^3',specific_heat_units='J/kg-K',thermal_cond_units='W/cm-degC')

C_2 = CEA_Obj(oxName='60_H2O2', fuelName='C2H5OH', 
                 pressure_units='MPa', temperature_units='K', 
                 isp_units='sec', cstar_units='m/s', sonic_velocity_units='m/s', 
                 enthalpy_units='J/kg', density_units='kg/m^3',specific_heat_units='J/kg-K',thermal_cond_units='W/cm-degC' )

#設定値の記入
#メモ
pc = 0.4 # 燃焼室圧力 MPaA
m = 7.4 # 混合比
a = 60 # 過酸化水素濃度 wt%
e = 100 # 開口比
F = 500 # 推力 mN
deg = 15 # ノズル半頂角 deg
n = 0.92 # 推力効率係数
LR_list = [10000, 22000, 34000, 47000, 63000, 67000] # アトマイザの型番のリスト
LR = LR_list[1] # アトマイザの型番
Lstr = 2 # 燃焼室特性長さ m

#物性値の計算
rho_2 = 1/(0.806 * (m/(m + 1)) * a/60 + 1.002 * (m/(m + 1)) * (1 - a/60) + 1.266 * (1/(m + 1)))
rho_1 = 1/(0.806 * a/60 + 1.002 * (1-a/60))
lam = 1/2 * (1 + math.cos(math.radians(deg)))

#rocket-ceaによる推進性能の算出
ICT = C_2.get_IvacCstrTc(Pc=pc, MR=m, eps=e, frozen=1, frozenAtThroat=0)
rhoc = C_2.get_Densities(Pc=pc, MR=m, eps=e, frozen=1, frozenAtThroat=0)
PambCF = C_2.getFrozen_PambCf(Pamb=0.0000001, Pc=pc, MR=m, eps=e, frozenAtThroat=0)
#Tc = C_2.get_Temperatures(Pc=pc, MR=m, eps=e, frozen=1, frozenAtThroat=0)
#H = C_2.get_Enthalpies(Pc=pc, MR=m, eps=e, frozen=1, frozenAtThroat=0)
#CF = (ICT[0] * const.g)/ICT[1]
#print(ICT[2], rhoc_2[0], H[0], ICT[1], PambCF[0], ICT[0], CF)

#設計値の算出
CF_ass = PambCF[0] * n * lam
At = F/(CF_ass * pc) * 10 ** (-3)
Dt = (At/math.pi) ** (1/2) * 2
mdot = At * pc/ICT[1] * 1000
pt = rho_2 * (60 * mdot/rho_2 * 0.366 * 60/(20/LR * 10 ** 6)) ** 2 + pc

#一液式の作動解析
pt_1_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, pt] # MPaA
pc_1_list = []
Ivac_1_list = []
cstr_1_list = []
F_1_list = []
rhoc_1_list = []
ts_1_list = []
for P in pt_1_list:
    pc_1new = pc
    diff = 1
    while (diff >1.0E-17):
        pc_1 = pc_1new
        def f(p):
            return (20/LR * 10 ** 6)/(0.366 * 60 ** 2) * (rho_1 * (P - p)) ** 0.5
        def g(p):
            return p * At/C_1.get_IvacCstrTc(Pc=pc_1, eps=e, frozen=0, frozenAtThroat=0)[1] * 1000
        def h(p):
            return f(p)-g(p)
        pc_1new = optimize.fsolve(h,0)[0]
        diff = pc_1 - pc_1new
        if diff < 0:
            diff = -diff
    if pc_1 != 0:
        ICT_1 = C_1.get_IvacCstrTc(Pc=pc_1, eps=e, frozen=0, frozenAtThroat=0)
        PambCF_1 = C_1.get_PambCf(Pamb=0.0000001, Pc=pc_1, eps=e)
        F_1 = PambCF_1[0] * n * lam * pc_1 * At * 10 ** 3
        rhoc_1 = C_1.get_Densities(Pc=pc_1, eps=e, frozen=0, frozenAtThroat=0)
        ts_1 = ICT_1[1] * rhoc_1[0]/pc_1  * Lstr * 10 ** -3
        pc_1_list.append(pc_1)
        Ivac_1_list.append(ICT_1[0])
        cstr_1_list.append(ICT_1[1])
        F_1_list.append(F_1)
        rhoc_1_list.append(rhoc_1[0])
        ts_1_list.append(ts_1)
    else:
        pc_1_list.append(0)
        Ivac_1_list.append(0)
        cstr_1_list.append(0)
        F_1_list.append(0)
        rhoc_1_list.append(0)
        ts_1_list.append(0)
print(pc_1_list)
print(F_1_list)
#print(ts_1_list)

#二液式の作動解析
pt_2_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, pt] # MPaA
pc_2_list = []
Ivac_2_list = []
cstr_2_list = []
F_2_list = []
rhoc_2_list = []
ts_2_list = []
for P in pt_2_list:
    pc_2new = pc
    diff = 1
    while (diff >1.0E-17):
        pc_2 = pc_2new
        def f(p):
            return (20/LR * 10 ** 6)/(0.366 * 60 ** 2) * (rho_2 * (P - p)) ** 0.5
        def g(p):
            return p * At/C_2.get_IvacCstrTc(Pc=pc_2, MR=m, eps=e, frozen=1, frozenAtThroat=0)[1] * 1000
        def h(p):
            return f(p)-g(p)
        pc_2new = optimize.fsolve(h,0)[0]
        diff = pc_2 - pc_2new
        if diff < 0:
            diff = -diff
    if pc_2 != 0:
        ICT_2 = C_2.get_IvacCstrTc(Pc=pc_2, MR=m, eps=e, frozen=1, frozenAtThroat=0)
        PambCF_2 = C_2.getFrozen_PambCf(Pamb=0.0000001, Pc=pc_2, MR=m, eps=e, frozenAtThroat=0)
        F_2 = PambCF_2[0] * n * lam * pc_2 * At * 10 ** 3
        rhoc_2 = C_2.get_Densities(Pc=pc_2, MR=m, eps=e, frozen=1, frozenAtThroat=0)
        ts_2 = ICT_2[1] * rhoc_2[0]/pc_2  * Lstr * 10 ** -3
        pc_2_list.append(pc_2)
        Ivac_2_list.append(ICT_2[0])
        cstr_2_list.append(ICT_2[1])
        F_2_list.append(F_2)
        rhoc_2_list.append(rhoc_2[0])
        ts_2_list.append(ts_2)
    else:
        pc_2_list.append(0)
        Ivac_2_list.append(0)
        cstr_2_list.append(0)
        F_2_list.append(0)
        rhoc_2_list.append(0)
        ts_2_list.append(0)
print(pc_2_list)
print(F_2_list)
#print(ts_2_list)

#メモ
#メモ
#MRは混合比
#epsは開口比
#Pcは燃焼室圧力
#frozen=1は凍結流，frozen=0は平衡流
#frozenAtThroat=0は燃焼室で凍結，frozenAtThroat=1はスロートで凍結