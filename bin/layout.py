import math

# python function by eQ
#
# set layout gambar dari batasan koordinat
#
# using:
# ll_inset, rl_inset, bl_inset, ul_inset, logo_y1, logo_y2, logo_y3 timepos_x, timepos_y, creditpos_x, creditpos_y = set_pos(left_lon, right_lon, bottom_lat, up_lat, jm, tinggi_map)

def set_pos(left_lon, right_lon, bottom_lat, up_lat, jm):
	# besar inset tambah 75% ke kiri dan kanan; 50% ke atas dan bawah
	if right_lon-left_lon < 2:
		ll_inset=left_lon-(1.6*(right_lon-left_lon))
		rl_inset=right_lon+(1.6*(right_lon-left_lon))
		bl_inset=bottom_lat-(1.3*(up_lat-bottom_lat))
		ul_inset=up_lat+(1.3*(up_lat-bottom_lat))
	elif right_lon-left_lon < 5:
		ll_inset=left_lon-(1.3*(right_lon-left_lon))
		rl_inset=right_lon+(1.3*(right_lon-left_lon))
		bl_inset=bottom_lat-(1*(up_lat-bottom_lat))
		ul_inset=up_lat+(1*(up_lat-bottom_lat))
	elif right_lon-left_lon < 8:
		ll_inset=left_lon-(0.9*(right_lon-left_lon))
		rl_inset=right_lon+(0.9*(right_lon-left_lon))
		bl_inset=bottom_lat-(0.7*(up_lat-bottom_lat))
		ul_inset=up_lat+(0.7*(up_lat-bottom_lat))
	else:
		ll_inset=left_lon-(0.7*(right_lon-left_lon))
		rl_inset=right_lon+(0.7*(right_lon-left_lon))
		bl_inset=bottom_lat-(1/3*(up_lat-bottom_lat))
		ul_inset=up_lat+(1/3*(up_lat-bottom_lat))
	# posisi skala peta tengah bawah
	skala_x=left_lon+(right_lon-left_lon)/2
	skala_y=bottom_lat+(up_lat-bottom_lat)/20
	skala_z=math.floor((right_lon-left_lon)*10/4)*10
	# posisi logo -Dx kiri atas (0.5 cm dari kiri)
	tinggi_map=abs(up_lat-bottom_lat)/abs(right_lon-left_lon)*jm
	logo_y1=up_lat-(up_lat-bottom_lat)/5.5
	logo_y2=up_lat-(up_lat-bottom_lat)/4.5
	logo_y3=up_lat-(up_lat-bottom_lat)/3.5
	# hitung posisi kompas peta kiri atas
	kompas_x=left_lon+(right_lon-left_lon)/30
	kompas_y=up_lat-(up_lat-bottom_lat)/20
	# posisi waktu kanan atas
	timepos_x=float(right_lon-((right_lon-left_lon)/30))
	timepos_y=float(up_lat-((up_lat-bottom_lat)/20))
	# posisi credit kanan bawah
	creditpos_x=float(right_lon-((right_lon-left_lon)/30))
	creditpos_y=float(bottom_lat+((up_lat-bottom_lat)/50))
	return ll_inset, rl_inset, bl_inset, ul_inset, logo_y1, logo_y2, logo_y3, kompas_x, kompas_y, skala_x, skala_y, skala_z, timepos_x, timepos_y, creditpos_x, creditpos_y, tinggi_map

# using:
# M_size = mag_scale(mag, M_scale)
def mag_scale(mag, M_scale, multiplier):
	if M_scale=='linear':
		M_size=mag*multiplier #skala linear
	elif M_scale=='quadrat':
		M_size=(mag*multiplier)**2 #skala kuadrat
	return float(M_size)

# using:
# R, J = set_legend(jx, num_M, min_M, file_legend)
# format file legenda: x_symbol, y_symbol, diameter_symbol, y_annotasi, text_annotasi
def set_legend(jx, num_M, min_M, file_legend, M_scale, multiplier):
	jy=jx/2
	R='0/'+str(jx)+'/0/'+str(jx/2)
	J=str(jx)+'/'+str(jx/2)
	i=0
	lebar=0
	while i < num_M:
		mag=i+min_M
		lebar=lebar+mag_scale(mag, M_scale, multiplier) #hitung lebar semua diameter magnitudo
		i+=1
	spasi=(jx-lebar)/(num_M+1) #spasi dibagi banyak legend
	legend=open(file_legend,'w')
	i=0
	space=0
	while i < num_M:
		mag=i+min_M
		mag_max=min_M+num_M
		space=space+spasi+mag_scale(mag, M_scale, multiplier)
		legend.write(str(space-1/2*mag_scale(mag, M_scale, multiplier))+' '+str(0+(jx/8))+' '+str(mag_scale(mag, M_scale, multiplier))+' '+str((0+jy/4)+1/2*mag_scale(mag_max, M_scale, multiplier))+' M'+str(i+min_M)+'\n')	#tulis x_symbol, y_symbol, dst ke file_legend
		i+=1
	legend.close()
	return R, J