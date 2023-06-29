from rocketcea.cea_obj import CEA_Obj 

ispObj = CEA_Obj( oxName='LOX', fuelName='CH4')
str = ispObj.get_full_cea_output( Pc=100.0, MR=6.0, eps=40.0, short_output=1, pc_units='bar', output='siunits')
# str = ispObj.get_full_cea_output( Pc=1000.0, MR=6.0, eps=40.0, frozen=1, frozenAtThroat=1, pc_units='bar')  # 凍結流の場合はこういうオプションをつける

print(str)