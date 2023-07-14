from rocketcea.cea_obj import CEA_Obj, add_new_oxidizer

card_str = """
oxid H2O2(L) H 2 O 2  wt%=60.00
h,cal=-44880.0     t(k)=298.15  rho.g/cc=1.407
oxid = WATER H 2.0 O 1.0 wt%= 40.0
h,cal=-68317. t(k)=298.15 rho.g/cc=1.0
"""
add_new_oxidizer( '60_H2O2', card_str )

ispObj = CEA_Obj( oxName='60_H2O2', fuelName='C2H5OH')
str = ispObj.get_full_cea_output( Pc=40.0, MR=7.4, eps=100.0, short_output=1, pc_units='bar', output='siunits')
#str = ispObj.get_full_cea_output( Pc=1000.0, MR=6.0, eps=40.0, frozen=1, frozenAtThroat=1, pc_units='bar')  # 凍結流の場合はこういうオプションをつける
pambcf = ispObj.get_PambCf(Pamb=0.000001, Pc=580.152, MR=6.0, eps=100.0)
vac_cstar_tc = ispObj.get_IvacCstrTc(Pc=580.152, MR=6.0, eps=100.0, frozen=0, frozenAtThroat=0) 
cstar = float(vac_cstar_tc[1])*0.3048
cf = float(pambcf[0])
print(str)
print('cf:%f',cf)
print("cstar:%f[m/s]",cstar)