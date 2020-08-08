import math
# python function by eQ
#
# tentukan bidang potong crosssection tegak lurus strike dan dip 2D bidang 360 derajad
# str = crosssection tegak lurus strike
# dp = dip dalam bidang 360 derajad (dip_360)
# jika strike, maka crosssection (>270=str-90; <90=str+270; >90-<270=str+90, dip minus (Aki-Richards))
#
# using:
# str, dp, az = crossection_strike_dip(strike, dip)
def crossection_strike_dip(strike, dip):
	if int(strike)>360:
		sys.exit("error, strike can not more than 360")
	elif int(strike)==360 or int(strike)==0:
		str=270
		dp=90+int(dip)
		az=180
	elif int(strike)>270:
		str=int(strike)-90
		dp=90+int(dip)
		az=int(strike)-180
	elif int(strike)>=180:
		str=int(strike)+90
		dp=270-int(dip)
		az=strike
	elif int(strike)>=90:
		str=int(strike)+90
		dp=270-int(dip)
		az=strike
	elif int(strike)>=0:
		str=int(strike)+270
		dp=90+int(dip)
		az=int(strike)+180
	else:
		sys.exit("error, strike can not less than 0")
	return str, dp, az
# hitung line crosssection strike (x0,y0 - x2,y2)
# (x0,y0 = startline (kiri); x1,y1 = epic; x2,y2 = endline(kanan)
# lengthdeg = 1/2 panjang patahan dalam degree
# csstr1 & csstr2 garis crosssect (90 deg from strike) dari epic ke arah berlawanan sepanjang 1/2 panjang patahan
# using:
# startlon, startlat, endlon, endlat = crossection_strike_line(main_lon, main_lat, crossection_strike, crossection_length)
def crossection_strike_line (main_lon, main_lat, crossection_strike, crossection_length):
	x1=float(main_lon)
	y1=float(main_lat)
	lengthdeg=crossection_length/222.7
	csstr1=crossection_strike
	if crossection_strike>180:
		csstr2=crossection_strike-180
	else:
		csstr2=crossection_strike+180
	x0=math.sin(math.radians(csstr1))*lengthdeg+x1
	y0=math.cos(math.radians(csstr1))*lengthdeg+y1
	x2=math.sin(math.radians(csstr2))*lengthdeg+x1
	y2=math.cos(math.radians(csstr2))*lengthdeg+y1
	return x0, y0, x2, y2
# hitung line crosssectionec dip
# (x0,y0 = startline (atas); x1,y1 = hipocenter; x2,y2 = endline(bawah)
# using:
# start_x, start_z, end_x, end_z = crossection_dip_line(main_depth, max_depth, dip, dip_360)
def crossection_dip_line(main_depth, max_depth, dip, dip_360):
	x1=0
	y0=0
	y1=-float(main_depth)
	y2=-float(max_depth)
	ang=int(dip)
	if dip_360 >180:
		x0=(abs(y0-y1)/math.tan(math.radians(ang))+x1)
		x2=(abs(y1-y2)/math.tan(math.radians(ang))-x1)*-1
	else:
		x0=(abs(y0-y1)/math.tan(math.radians(ang))-x1)*-1
		x2=(abs(y1-y2)/math.tan(math.radians(ang))+x1)
	return x0, y0, x2, y2