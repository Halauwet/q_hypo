import time
import math
from subprocess import Popen
from bin.crossection import crossection_strike_dip, crossection_strike_line, crossection_dip_line
from bin.layout import set_pos
from bin.reformat_data import from_sdigb, from_hypodd, from_ascii
# baca parameter input (tambah jenis input data dari SDIGB (default atau hypodd)) reformat datetime satu variabel
# baca data output ke datatmp (tambah output waktu start dan end) cari konversi waktu ke detik, start time - 2 jam
parameter='parameter_map.inp'
fileoutput='bin\/plot.bat'
legend='bin\/legenda.bat'
datagempa='data\/hypocenter.dat'
tmpdata='tmp\/tmpdata.dat'
title=''; fromdate=''; todate=''; datasource=''; area=1; input=0; fps=10
lon_center=0; lat_center=0; radius_center=0
left_lon=0; right_lon=0; bot_lat=0; up_lat=0
jm=15
dur=0
tzsign=''; tzone=0; tzname='UTC'
ot_start=0; ot_stop=0; start_time=0; stop_time=0
lat=0; lon=0; depth=0; mag=0; mtype=''; epic_size=0.3
strike1=0; strike2=0; dip1=0; dip2=0; slip1=0; slip2=0
cslength=0; cswidth=0
maxelev=0; maxdepth=0
mag_size=2 #set mag multiplier same as legend.bat value
plot_animasi='NO'
plot_crossect='NO'
plot_topo='NO'
print('Epicenter Animation Generator')
print('by eQ H')
print('--------------------------------------------------------')
print('')
# baca isi file input dan buka file output
file=open(parameter,'r') 
baris=file.readlines()
for i in range(len(baris)):
	baris[i]=baris[i].split()
file.close()
i = 0
while i < len(baris):
	if len(baris[i])>0 and baris[i][0]=='Title':
		title=' '.join(baris[i+1])
	if len(baris[i])>0 and baris[i][0]=='Plot_Area':
		area=int(baris[i+3][0])
		if area==0:
			lon_center=(('%.4f')%float(baris[i+4][0]))
			lat_center=(('%.4f')%float(baris[i+4][1]))
			radius_center=int(baris[i+4][2])
		else:
			left_lon=(('%.4f')%float(baris[i+4][0]))
			right_lon=(('%.4f')%float(baris[i+4][1]))
			bot_lat=(('%.4f')%float(baris[i+4][2]))
			up_lat=(('%.4f')%float(baris[i+4][3]))
	if len(baris[i])>0 and baris[i][0]=='From_Date':
		fromdate=' '.join(baris[i+1])
	if len(baris[i])>0 and baris[i][0]=='To_Date':
		todate=' '.join(baris[i+1])
	if len(baris[i])>0 and baris[i][0]=='Input_Data':
		input=int(baris[i+1][0])
	if len(baris[i])>0 and baris[i][0]=='Plot_Animasi' and baris[i+1][0]=='Y' or len(baris[i])>0 and baris[i][0]=='Plot_Animasi' and baris[i+1][0]=='y':
		plot_animasi='YES'
	if len(baris[i])>0 and baris[i][0]=='Durasi_Animasi':
		dur=int(baris[i+1][0])
	if len(baris[i])>0 and baris[i][0]=='Frame_per_second':
		fps=int(baris[i+1][0])
	if len(baris[i])>0 and baris[i][0]=='Convert':
		tzsign=baris[i+1][0]
		tzone=int(baris[i+1][1])
		tzname=baris[i+1][2]
	if len(baris[i])>0 and baris[i][0]=='Plot_Crosssection?' and baris[i+1][0]=='Y' or len(baris[i])>0 and baris[i][0]=='Plot_Crosssection?' and baris[i+1][0]=='y':
		plot_crossect='YES'
	if len(baris[i])>0 and baris[i][0]=='Mainshock_Hypocenter':
		lon=(('%.4f')%float(baris[i+1][0]))
		lat=(('%.4f')%float(baris[i+1][1]))
		depth=(('%.2f')%float(baris[i+1][2]))
	if len(baris[i])>0 and baris[i][0]=='Magnitudo':
		mag=(('%.1f')%float(baris[i+1][0]))
		epic_size=(float(mag)*0.1)**float(mag_size)
		mtype=baris[i+1][1]
	if len(baris[i])>0 and baris[i][0]=='Nodal':
		strike1=baris[i+1][0]
		dip1=baris[i+1][1]
		slip1=baris[i+1][2]
		strike2=baris[i+2][0]
		dip2=baris[i+2][1]
		slip2=baris[i+2][2]
	if len(baris[i])>0 and baris[i][0]=='Crossection_Length':
		cslength=int(baris[i+1][0])
		cswidth=cslength / 2
		# cslength = panjang patahan; cswidth = 1/2 panjang patahan ke kiri + 1/2 panjang patahan ke kanan)
	if len(baris[i])>0 and baris[i][0]=='Max':
		maxdepth=baris[i+1][0]
	if len(baris[i])>0 and baris[i][0]=='#Max':
		maxdepth=int(math.ceil(float(depth) * 2 / 50))*50
	if len(baris[i])>0 and baris[i][0]=='Plot_Elevation' and baris[i+1][0]=='Y' or len(baris[i])>0 and baris[i][0]=='Plot_Elevation' and baris[i+1][0]=='y':
		plot_topo='YES'
		maxelev=baris[i+1][1]
	if len(baris[i])>0 and baris[i][0]=='Data_source':
		datasource=' '.join(baris[i+1])
	i = i+1
print(title)
print('')
if input==0:
	# refromat data
	ot_start, time_sec=from_sdigb(datagempa, tmpdata, tzsign, tzone, tzname)
	ot_stop=time_sec
elif input==1:
	ot_stop, time_sec=from_hypodd(datagempa, tmpdata, tzsign, tzone, tzname)
	ot_start=time_sec
elif input==2:
	ot_start, time_sec=from_ascii(datagempa, tmpdata, tzsign, tzone, tzname)
	ot_stop=time_sec
else:
	print('Input data default')
	ot_start, time_sec=from_sdigb(datagempa, tmpdata, tzsign, tzone, tzname)
	ot_stop=time_sec
eq_period=ot_stop-ot_start
# HITUNG Frekuensi Gempa/periode waktu
lblperiode='Periode kurang'
# if eq_period < 9000:
	# lblperiode='Periode kurang'
# elif eq_period < 18000:
	# lblperiode='Periode 30 menit'
	
# elif eq_period < 54000:
	# lblperiode='Jam'
	
# elif eq_period < 108000:
	# lblperiode='Periode 3 jam'
		
# elif eq_period < 216000:
	# lblperiode='Periode 6 jam'
		
# elif eq_period < 432000:
	# lblperiode='Periode 12 jam'
	
# else:
	# lblperiode='Hari'
print('Plot seismicity map')
if plot_crossect=='YES':
	# tentukan bidang potong crosssection tegak lurus strike dan dip 2D bidang 360 derajad
	str1, dp1, az1 = crossection_strike_dip(strike1, dip1)
	str2, dp2, az2 = crossection_strike_dip(strike2, dip2)
	# hitung line crosssection strike (startlon1,startlat1 - endlon1,endlat1)
	startlon1, startlat1, endlon1, endlat1 = crossection_strike_line(lon, lat, str1, cslength)
	file=open('tmp/LINE_AB','w')
	file.write('%s %s\n%s %s' %(str(startlon1),str(startlat1),str(endlon1),str(endlat1))+'\n')
	file.close()
	file=open('tmp/TEXT_A','w')
	file.write('%s %s A' %(str(startlon1),str(startlat1))+'\n')
	file.close()
	file=open('tmp/TEXT_B','w')
	file.write('%s %s B' %(str(endlon1),str(endlat1))+'\n')
	file.close()
	startlon2, startlat2, endlon2, endlat2 = crossection_strike_line(lon, lat, str2, cslength)
	file=open('tmp/LINE_CD','w')
	file.write('%s %s\n%s %s' %(str(startlon2),str(startlat2),str(endlon2),str(endlat2))+'\n')
	file.close()
	file=open('tmp/TEXT_C','w')
	file.write('%s %s C' %(str(startlon2),str(startlat2))+'\n')
	file.close()
	file=open('tmp/TEXT_D','w')
	file.write('%s %s D' %(str(endlon2),str(endlat2))+'\n')
	file.close()
	# hitung line crosssection dip
	xab0, y0, xab2, y2 = crossection_dip_line(depth, maxdepth, dip1, dp1)
	file=open('tmp/DIP_AB','w')
	file.write(str(xab0)+' '+str(y0)+'\n'+str(xab2)+' '+str(y2))
	file.close()
	xcd0, y0, xcd2, y2 = crossection_dip_line(depth, maxdepth, dip2, dp2)
	file=open('tmp/DIP_CD','w')
	file.write(str(xcd0)+' '+str(y0)+'\n'+str(xcd2)+' '+str(y2))
	file.close()
	# hitung batasan peta
	# (Diameter Peta / 2 (degree))
	# if startlon1 < ll or startlon2 < ll or endlon1 > rl or endlon2 > rl or startlat1 > ul or startlat2 > ul or endlat1 < bl or endlat2 < bl:
	print('Map area automatic from mainshock') 
	mapoffs=int(math.ceil(float(cslength)/222.7))
	rl=float(lon)+mapoffs
	ll=float(lon)-mapoffs
	ul=float(lat)+mapoffs
	bl=float(lat)-mapoffs
else:
	if area==0:
		ll=float(lon_center)-radius_center
		rl=float(lon_center)+radius_center
		bl=float(lat_center)-radius_center
		ul=float(lat_center)+radius_center
	else:
		ll=float(left_lon)
		rl=float(right_lon)
		bl=float(bot_lat)
		ul=float(up_lat)
# print(ll, rl, bl, ul, jm, cslength)
# tentukan posisi inset, logo, waktu, dan kredit
ll_inset, rl_inset, bl_inset, ul_inset, logo_y1, logo_y2, kompas_x, kompas_y, skala_x, skala_y, skala_z, timepos_x, timepos_y, creditpos_x, creditpos_y, tinggi_map = set_pos(ll, rl, bl, ul, jm)
if plot_crossect=='YES':
	print('')
	print('CROSS SECTION PARAMETER:')
	print('Koordinat Epicenter= %f %f %f' %(float(lat),float(lon),float(depth)))
	print('Magnitudo = %s' %(mag))
	print('Nodal Plane 1 = %3i %2i %3i' %(int(strike1),int(dip1),int(slip1)))
	print('Nodal Plane 2 = %3i %2i %3i' %(int(strike2),int(dip2),int(slip2)))
	print('Batas koordinat= %3.2f %3.2f %2.2f %2.2f' %(rl,ll,ul,bl))
	print('Crosssection A-B = %s' %(str1))
	print('Crosssection C-B = %s' %(str2))
	print('DIP Crosssection A-B = %s' %(dp1))
	print('DIP Crosssection C-B = %s' %(dp2))
	print('Plot Topography line = %s' %(plot_topo))
	file=open(legend,'w')
	file.write('echo G -0.05>%L%'+'\n')
	file.write('echo N 5 >>%L%'+'\n')
	file.write('::echo V 0 1p>>%L%'+'\n')
	file.write('echo L 8 4 C Depth (km)>>%L%'+'\n')
	file.write('echo L 8 4 C "M = 3">>%L%'+'\n')
	file.write('echo L 8 4 C "M = 4">>%L%'+'\n')
	file.write('echo L 8 4 C "M = 5">>%L%'+'\n')
	file.write('echo L 8 4 C "M = \\076 5">>%L%'+'\n')
	file.write('::echo V 0 1p>>%L%'+'\n')
	file.write('::echo D 0 1p>>%L%'+'\n')
	file.write('::echo V 0 1p>>%L%'+'\n')
	file.write('echo L 8 4 C \\074 60>>%L%'+'\n')
	file.write('echo S 0.5 c '+str(mag_size*3)+' red 0.5p 0.1>>%L%'+'\n')
	file.write('echo S 0.5 c '+str(mag_size*4)+' red 0.5p 0.1>>%L%'+'\n')
	file.write('echo S 0.5 c '+str(mag_size*5)+' red 0.5p 0.1>>%L%'+'\n')
	file.write('echo S 0.5 c '+str(mag_size*6)+' red 0.5p 0.1>>%L%'+'\n')
	file.write('echo L 8 4 C 60 - 300>>%L%'+'\n')
	file.write('echo S 0.5 c '+str(mag_size*3)+' yellow 0.5p 0.1>>%L%'+'\n')
	file.write('echo S 0.5 c '+str(mag_size*4)+' yellow 0.5p 0.1>>%L%'+'\n')
	file.write('echo S 0.5 c '+str(mag_size*5)+' yellow 0.5p 0.1>>%L%'+'\n')
	file.write('echo S 0.5 c '+str(mag_size*6)+' yellow 0.5p 0.1>>%L%'+'\n')
	file.write('echo L 8 4 C \\076 300>>%L%'+'\n')
	file.write('echo S 0.5 c '+str(mag_size*3)+' green 0.5p 0.1>>%L%'+'\n')
	file.write('echo S 0.5 c '+str(mag_size*4)+' green 0.5p 0.1>>%L%'+'\n')
	file.write('echo S 0.5 c '+str(mag_size*5)+' green 0.5p 0.1>>%L%'+'\n')
	file.write('echo S 0.5 c '+str(mag_size*6)+' green 0.5p 0.1>>%L%'+'\n')
	file.write('echo G 0.4>>%L%'+'\n')
	file.write('::echo V 0 1p>>%L%'+'\n')
	file.write('::echo D 0 1p>>%L%'+'\n')
	file.write('::echo V 0 1p>>%L%'+'\n')
	file.close()
	file=open(fileoutput,'w')
	file.write('@echo off'+'\n')
	file.write('REM echo EQ Map Generator'+'\n')
	file.write('REM echo by eQ H'+'\n')
	file.write('REM echo.--------------------------------------------------------'+'\n')
	file.write('REM Parameter Gempa'+'\n')
	file.write('set title='+title+'\n')
	file.write('set mainlat='+str(lat)+'\n')
	file.write('set mainlon='+str(lon)+'\n')
	file.write('set maindepth='+str(depth)+'\n')
	file.write('set mainmag='+str(mag)+'\n')
	file.write('set typemag='+mtype+'\n')
	file.write('set strike1='+strike1+'\n')
	file.write('set strike2='+strike2+'\n')
	file.write('set dip1='+dip1+'\n')
	file.write('set dip2='+dip2+'\n')
	file.write('set slip1='+slip1+'\n')
	file.write('set slip2='+slip2+'\n')
	file.write('REM length=panjang cross section'+'\n')
	file.write('set length='+str(cslength)+'\n')
	file.write('set width='+str(cswidth)+'\n')
	file.write('set AC=-%width%'+'\n')
	file.write('set BD=%width%'+'\n')
	file.write('set maxelev='+str(maxelev)+'\n')
	file.write('set maxdepth='+str(maxdepth)+'\n')
	file.write('set x1='+str(kompas_x)+'\n')
	file.write('set y1='+str(kompas_y)+'\n')
	file.write('set x2='+str(skala_x)+'\n')
	file.write('set y2='+str(skala_y)+'\n')
	file.write('set z2='+str(skala_z)+'\n')
	file.write('set str1='+str(str1)+'\n')
	file.write('set str2='+str(str2)+'\n')
	file.write('set azm1='+str(az1)+'\n')
	file.write('set azm2='+str(az2)+'\n')
	file.write('set startlat1='+str(startlat1)+'\n')
	file.write('set startlon1='+str(startlon1)+'\n')
	file.write('set startlat2='+str(startlat2)+'\n')
	file.write('set startlon2='+str(startlon2)+'\n')
	file.write('set endlat1='+str(endlat1)+'\n')
	file.write('set endlon1='+str(endlon1)+'\n')
	file.write('set endlat2='+str(endlat2)+'\n')
	file.write('set endlon2='+str(endlon2)+'\n')
	file.write('REM Set Parameter Peta'+'\n')
	file.write('set ps=animasi.ps'+'\n')
	file.write('set D=../inc/depth.cpt'+'\n')
	file.write('set L=../inc/legend'+'\n')
	file.write('set epic=%mainlon%/%mainlat%'+'\n')
	file.write('set tmpdata=../tmp/tmpdata.dat'+'\n')
	file.write('set station=../data/station.sel'+'\n')
	file.write('set focal=../data/psmeca.dat'+'\n')
	file.write('set output=../output/animasi.mp4'+'\n')
	file.write('set indo=../inc/indonesia.nc'+'\n')
	file.write('set topo=../inc/my_etopo.cpt'+'\n')
	file.write('set fault=../inc/fault_moluccas.gmt'+'\n')
	file.write('set subduction=../inc/subduksi_moluccas.gmt'+'\n')
	# file.write('set trench_a=../inc/trench-a.gmt'+'\n')
	# file.write('set trench_b=../inc/trench-b.gmt'+'\n')
	# file.write('set thrust=../inc/thrust.gmt'+'\n')
	# file.write('set transform=../inc/transform.gmt'+'\n')
	file.write('REM Plot Area'+'\n')
	file.write('set llon='+str(ll)+'\n')
	file.write('set rlon='+str(rl)+'\n')
	file.write('set blat='+str(bl)+'\n')
	file.write('set ulat='+str(ul)+'\n')
	file.write('set R=%llon%/%rlon%/%blat%/%ulat%'+'\n')
	file.write('set R_inset='+str(ll_inset)+'/'+str(rl_inset)+'/'+str(bl_inset)+'/'+str(ul_inset)+'\n')
	file.write('set R2=%AC%/%BD%/-%maxdepth%/0'+'\n')
	file.write('set R3=0/%length%/-%maxdepth%/0'+'\n')
	file.write('set R4=0/%length%/-%maxelev%/%maxelev%'+'\n')
	file.write('set starttime='+str(start_time)+'\n')
	file.write('set stoptime='+str(stop_time)+'\n')
	file.write('REM Proyeksi'+'\n')
	file.write('set proyeksi1=../tmp/projection1.tmp'+'\n')
	file.write('set proyeksi2=../tmp/projection2.tmp'+'\n')
	file.write('set lineAB=../tmp/LINE_AB'+'\n')
	file.write('set lineCD=../tmp/LINE_CD'+'\n')
	file.write('set dip_AB=../tmp/DIP_AB'+'\n')
	file.write('set dip_CD=../tmp/DIP_CD'+'\n')
	file.write('set text_A=../tmp/TEXT_A'+'\n')
	file.write('set text_B=../tmp/TEXT_B'+'\n')
	file.write('set text_C=../tmp/TEXT_C'+'\n')
	file.write('set text_D=../tmp/TEXT_D'+'\n')
	file.write('set track=../tmp/track'+'\n')
	file.write('set trackAB=../tmp/trackAB'+'\n')
	file.write('set trackCD=../tmp/trackCD'+'\n')
	file.write('set sealevel=../tmp/sealevel.line'+'\n')
	file.write(':TOPOCPT'+'\n')
	file.write('if exist %topo% ('+'\n')
	# file.write('echo topo OK'+'\n')
	file.write('goto :DEPTHCPT'+'\n')
	file.write(') else ('+'\n')
	file.write('echo generate %topo%'+'\n')
	file.write('makecpt -Z -Cetopo1 > %topo%'+'\n')
	file.write(')'+'\n')
	file.write(':DEPTHCPT'+'\n')
	file.write('if exist %D% ('+'\n')
	# file.write('echo depthcpt OK'+'\n')
	file.write('goto :LEGEND'+'\n')
	file.write(') else ('+'\n')
	file.write('echo generate %D%'+'\n')
	file.write('run cptdepth.bat'+'\n')
	file.write(')'+'\n')
	file.write(':LEGEND'+'\n')
	file.write('run legenda.bat'+'\n')
	file.write(':PROJECT'+'\n')
	file.write('gawk "{print $4, $5, $6, $7, $8}" %tmpdata% | project -C%epic% -A%azm1% -Fxyzpqrs -Q > %proyeksi1%'+'\n')
	file.write('gawk "{print $4, $5, $6, $7, $8}" %tmpdata% | project -C%epic% -A%azm2% -Fxyzpqrs -Q > %proyeksi2%'+'\n')
	if plot_topo=='YES':
		file.write('project -C%startlon1%/%startlat1% -E%endlon1%/%endlat1% -G.5 -Q > %track%'+'\n')
		file.write('grdtrack %track% -G%indo% | gawk "{print $3, $4 }" > %trackAB%'+'\n')
		file.write('project -C%startlon2%/%startlat2% -E%endlon2%/%endlat2% -G.5 -Q > %track%'+'\n')
		file.write('grdtrack %track% -G%indo% | gawk "{print $3, $4 }" > %trackCD%'+'\n')
	file.write(':plot'+'\n')
	file.write('REM Peta Dasar'+'\n')
	file.write('pscoast -JM8c -R%R% -Dh -B1::WSne -G245/245/200 -S150/255/255 -W0.25p,black -Lg%x2%/%y2%+c-1+w%z2%k+l+ab+jBC -Tdg%x1%/%y1%+w1.2+f1+jLT --MAP_ANNOT_MIN_SPACING=0.1p --FONT_TITLE=10 --FONT_LABEL=9 --FONT_ANNOT_PRIMARY=8 -K -Y8 > %ps%'+'\n')
	file.write('psxy %fault% -JM -R -Wthin -O -K >> %ps%'+'\n')
	file.write('psxy %subduction% -JM -R -Wthin -Sf0.8i/0.08i+l+t -Gblack -O -K >> %ps%'+'\n')
	file.write('REM Data'+'\n')
	file.write('gawk -F" " "{print $2, $3}" %station% | psxy -J -R%R% -St0.3c -Wthin,black -Gblue -O -K >> %ps%'+'\n')
	file.write('gawk -F" " "{print  $2, $3, $1}" %station% | pstext -J -R -F+f8p,Helvetica+jLT -O -K >> %ps%'+'\n')
	file.write('gawk "{print $4,$5,$6,$7*'+str(mag_size)+'}" %tmpdata% | psxy -R -JM -Sc -C%D% -Wthin -O -K >> %ps%'+'\n')
	file.write('gawk "{print '+lon+','+lat+','+depth+',$4,$5,$6,$7,$8,$9,$10,0,0,$13}" %focal% | psmeca -R -J -Sm'+str(epic_size)+'/-1 -Z%D% -T0 -C -O -K >> %ps%'+'\n')
	file.write('REM Cross Section Line AB (NP1)'+'\n')
	file.write('psxy %lineAB% -J -R -O -K >> %ps%'+'\n')
	file.write('pstext %text_A% -J -R -F+f8p,Helvetica+jCM -N -O -K >> %ps%'+'\n')
	file.write('pstext %text_B% -J -R -F+f8p,Helvetica+jCM -N -O -K >> %ps%'+'\n')
	file.write('REM Cross Section Line CD (NP2)'+'\n')
	file.write('psxy %lineCD% -J -R -O -K >> %ps%'+'\n')
	file.write('pstext %text_C% -J -R -F+f8p,Helvetica+jCM -N -O -K >> %ps%'+'\n')
	file.write('pstext %text_D% -J -R -F+f8p,Helvetica+jCM -N -O -K >> %ps%'+'\n')
	# file.write('echo '+str(creditpos_x)+' '+str(creditpos_y)+' @@eqhalauwet | pstext -R -JM -F+f8,ZapfChancery-MediumItalic+jRB -O -K >> %ps%'+'\n')
	file.write('REM Inset'+'\n')
	file.write('pscoast -R%R_inset% -JM2 -Dh -W0.25p,black -Gwhite -S150/255/255 -B5::wsNE --MAP_FRAME_TYPE=plain --FONT_ANNOT_PRIMARY=5 -O -K >> %ps%'+'\n')
	file.write('REM psxy ../inc/subduksi_moluccas.gmt -JM -R -W0.2 -Sf0.2c/0.03c+l+t -Gblack -O -K >> %ps%'+'\n')
	file.write('REM psxy ../inc/fault_moluccas.gmt -JM -R -W0.2 -O -K >> %ps%'+'\n')
	file.write('echo %llon% %blat% > ../tmp/box'+'\n')
	file.write('echo %llon% %ulat% >> ../tmp/box'+'\n')
	file.write('echo %rlon% %ulat% >> ../tmp/box'+'\n')
	file.write('echo %rlon% %blat% >> ../tmp/box'+'\n')
	file.write('echo %llon% %blat% >> ../tmp/box'+'\n')
	file.write('psxy -R -JM ../tmp/box -Wthin,red -O -K >> %ps%'+'\n')
	file.write('REM Parameter Peta'+'\n')
	file.write('psbasemap -R0/1/0/1 -JX8/8 -B+t"" -X8.5 -Y0.6 -O -K >> %ps%'+'\n')
	file.write('echo 0.5 0.94 %title% | pstext -J -R -F+f11p,Helvetica+jCM -O -K >> %ps%'+'\n')
	file.write('echo 0.5 0.83 %typemag% %mainmag% | pstext -J -R -F+f10p,Helvetica+jCM -O -K>> %ps%'+'\n')
	file.write('gawk "{print 0.5,0.68,$3,$4,$5,$6,$7,$8,$9,$10,0,0,$13}" %focal% | psmeca -R -J -Sm0.7/-1 -C -Z%D% -T0 -N -O -K >> %ps%'+'\n')
	file.write('echo 0.5 0.51 Fault plane1:  strike=%strike1%  dip=%dip1%  slip=%slip1% | pstext -J -R -F+f8p,Helvetica+jCM -O -K >> %ps%'+'\n')
	file.write('echo 0.5 0.40 Fault plane2:  strike=%strike2%  dip=%dip2%  slip=%slip2% | pstext -J -R -F+f8p,Helvetica+jCM -O -K >> %ps%'+'\n')
	file.write('pslegend %L% -J -Dx0.25/0.1+w7.5/0.85i+jLB+l1.7 -O -K >> %ps%'+'\n')
	file.write('REM box crossection'+'\n')
	file.write('set boxwidht=8'+'\n')
	file.write('set boxheight=3.5'+'\n')
	file.write('set boxelev=1'+'\n')
	file.write('REM boxelev = boxheight / 5'+'\n')
	file.write('set boxoverlap=3'+'\n')
	file.write('REM boxoverlap = boxheight - (1/2 * boxelev)'+'\n')
	if plot_topo=='YES':
		file.write(':CROSS_AB'+'\n')
		file.write('psxy %trackAB% -R%R4% -JX%boxwidht%/%boxelev% -B::/a%maxelev%f1000:"Elev (m)":We --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 -W3p -X-8.5 -Y-3 -O -K >> %ps%'+'\n')
		file.write('echo 0 %maxelev% A | pstext -J -R -F+f10p,Helvetica+jRB -N -O -K >> %ps%'+'\n')
		file.write('echo %length% %maxelev% B | pstext -J -R -F+f10p,Helvetica+jLB -N -O -K >> %ps%'+'\n')
		file.write('echo 0 0 > %sealevel%'+'\n')
		file.write('echo %length% 0 >> %sealevel%'+'\n')
		file.write('psxy %sealevel% -J -R -W1,89/89/171 -O -K >> %ps%'+'\n')
		file.write('psbasemap -JX%boxwidht%/%boxheight% -R%R2% -Bxa50+l"Distance (km)" -Bya20f20+l"Depth (km)" -BWSne+t"Cross Section Fault Plane 1" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y-%boxoverlap% >> %ps%'+'\n')
		file.write('gawk "{print $7, $3*(-1.0), $3, $4*'+str(mag_size)+'}" %proyeksi1% | psxy -R -J -Sc -C%D% -Wthin -O -K >> %ps%'+'\n')
		file.write('psxy %dip_AB% -J -R -Wthin,black -O -K >> %ps%'+'\n')
		file.write('gawk "{print '+lon+','+lat+',-'+depth+',$4,$5,$6,$7,$8,$9,$10,0,0,$13}" %focal% | pscoupe -J -R%R3% -Sm'+str(epic_size)+'/0/0 -T -Aa%startlon1%/%startlat1%/%endlon1%/%endlat1%/90/%width%/0/600 -Z%D% -E255 -N -O -K >> %ps%'+'\n')
		file.write(':CROSS_CD'+'\n')
		file.write('psxy %trackCD% -R%R4% -JX%boxwidht%/%boxelev% -B::/a%maxelev%f1000:"Elev (m)":ew --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 -W3p -X8.5 -Y%boxoverlap% -O -K >> %ps%'+'\n')
		file.write('echo 0 %maxelev% C | pstext -J -R -F+f10p,Helvetica+jRB -N -O -K >> %ps%'+'\n')
		file.write('echo %length% %maxelev% D | pstext -J -R -F+f10p,Helvetica+jLB -N -O -K >> %ps%'+'\n')
		file.write('echo 0 0 > %sealevel%'+'\n')
		file.write('echo %length% 0 >> %sealevel%'+'\n')
		file.write('psxy %sealevel% -J -R -W1,89/89/171 -O -K >> %ps%'+'\n')
		file.write('psbasemap -JX%boxwidht%/%boxheight% -R%R2% -Bxa50+l"Distance (km)" -Bya20f20+l"Depth (km)" -BeSnw+t"Cross Section Fault Plane 2" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y-%boxoverlap%>> %ps%'+'\n')
		file.write('gawk "{print $7, $3*(-1.0), $3, $4*'+str(mag_size)+'}" %proyeksi2% | psxy -R -J -Sc -C%D% -Wthin -O -K >> %ps%'+'\n')
		file.write('psxy %dip_CD% -J -R -Wthin,black -O -K >> %ps%'+'\n')
		file.write('gawk "{print '+lon+','+lat+',-'+depth+',$4,$5,$6,$7,$8,$9,$10,0,0,$13}" %focal% | pscoupe -J -R%R3% -Sm'+str(epic_size)+'/0/0 -T -Aa%startlon2%/%startlat2%/%endlon2%/%endlat2%/90/%width%/0/600 -Z%D% -E255 -N -O -K >> %ps%'+'\n')
	else:
		file.write(':CROSS_AB'+'\n')
		file.write('psbasemap -JX%boxwidht%/%boxheight% -R%R2% -BWSne+t"Cross Section Fault Plane 1" -Bxa50+l"Distance (km)" -Bya20f20+l"Depth (km)" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -X-8.5 -Y-6 >> %ps%'+'\n')
		file.write('echo %AC% 0 A | pstext -J -R -F+f10p,Helvetica+jRB -N -O -K >> %ps%'+'\n')
		file.write('echo %BD% 0 B | pstext -J -R -F+f10p,Helvetica+jLB -N -O -K >> %ps%'+'\n')
		file.write('gawk "{print $7, $3*(-1.0), $3, $4*'+str(mag_size)+'}" %proyeksi1% | psxy -R -J -Sc -C%D% -Wthin -O -K >> %ps%'+'\n')
		file.write('psxy %dip_AB% -J -R -Wthin,black -O -K >> %ps%'+'\n')
		file.write('gawk "{print '+lon+','+lat+',-'+depth+',$4,$5,$6,$7,$8,$9,$10,$11,$12,$13}" %focal% | pscoupe -J -R%R3% -Sm'+str(epic_size)+'/0/0 -T -Aa%startlon1%/%startlat1%/%endlon1%/%endlat1%/90/%width%/0/600 -Z%D% -E255 -N -O -K >> %ps%'+'\n')
		file.write(':CROSS_CD'+'\n')
		file.write('psbasemap -JX%boxwidht%/%boxheight% -R%R2% -BeSnw+t"Cross Section Fault Plane 2" -Bxa50+l"Distance (km)" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -X8.5 >> %ps%'+'\n')
		file.write('echo %AC% 0 C | pstext -J -R -F+f10p,Helvetica+jRB -N -O -K >> %ps%'+'\n')
		file.write('echo %BD% 0 D | pstext -J -R -F+f10p,Helvetica+jLB -N -O -K >> %ps%'+'\n')
		file.write('gawk "{print $7, $3*(-1.0), $3, $4*'+str(mag_size)+'}" %proyeksi2% | psxy -R -J -Sc -C%D% -Wthin -O -K >> %ps%'+'\n')
		file.write('psxy %dip_CD% -J -R -Wthin,black -O -K >> %ps%'+'\n')
		file.write('gawk "{print '+lon+','+lat+',-'+depth+',$4,$5,$6,$7,$8,$9,$10,$11,$12,$13}" %focal% | pscoupe -J -R%R3% -Sm'+str(epic_size)+'/0/0 -T -Aa%startlon2%/%startlat2%/%endlon2%/%endlat2%/90/%width%/0/600 -Z%D% -E255 -N -O -K >> %ps%'+'\n')
	if lblperiode=='Periode kurang':
		tinggi_graph=(13.5-1.7)/2
		graf_yoffset=tinggi_graph+1.6
		file.write('psbasemap -JX6/'+str(tinggi_graph)+' -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -X8.5 >> %ps%'+'\n')
		file.write('psbasemap -JX6/'+str(tinggi_graph)+' -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y'+str(graf_yoffset)+' >> %ps%'+'\n')
		file.write('gawk "{print $7}" %tmpdata% | pshistogram -JX6/'+str(tinggi_graph)+' -W0.5+l -Gblue -L0.5 -Y-'+str(graf_yoffset)+' -BESwn -Bx+lMagnitude -By+l"Number of earthquakes" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> %ps%'+'\n')
		file.write('gawk "{print $6}" %tmpdata% | pshistogram -JX6/'+str(tinggi_graph)+' -W2+l -Gblue -L0.5 -Y'+str(graf_yoffset)+' -BESwn -Bx+l"Depth (km)" -By+l"Number of earthquakes" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> %ps%'+'\n')
		file.write('echo 0.9 -0.15 "by: @@eqhalauwet" | pstext -R -Bg1x -J -F+f9,ZapfChancery-MediumItalic+jLT -Y-'+str(graf_yoffset)+' -N -O >> %ps%'+'\n')
	else:
		graf_yoffset=4.95
		file.write('psbasemap -JX5/%boxheight% -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -X8.5 >> %ps%'+'\n')
		file.write('psbasemap -JX5/%boxheight% -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y'+str(graf_yoffset)+' >> %ps%'+'\n')
		file.write('psbasemap -JX5/%boxheight% -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y'+str(graf_yoffset)+' >> %ps%'+'\n')
		file.write('gawk "{print $7}" %tmpdata% | pshistogram -JX5/%boxheight% -W0.5+l -Gblue -L0.5 -Y-'+str(graf_yoffset*2)+' -BESwn -Bx+lMagnitude -By+l"Number of earthquakes" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> %ps%'+'\n')
		file.write('gawk "{print $6}" %tmpdata% | pshistogram -JX5/%boxheight% -W2+l -Gblue -L0.5 -Y'+str(graf_yoffset)+' -BESwn -Bx+l"Depth (km)" -By+l"Number of earthquakes" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> %ps%'+'\n')
		####
		file.write('gawk "{print $6}" %tmpdata% | pshistogram -JX5/%boxheight% -W5+l -Gblue -L0.5 -Y'+str(graf_yoffset)+' -BESwn -Bx+l"Depth (km)" -By+l"Number of earthquakes" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> %ps%'+'\n')
		file.write('echo 0.9 -0.24 "by: @@eqhalauwet" | pstext -R -Bg1x -J -F+f9,ZapfChancery-MediumItalic+jLT -Y-'+str(graf_yoffset*2)+' -N -O >> %ps%'+'\n')
	file.write('psconvert %ps% -Tj -E256 -P -A -F../output/plot.jpg'+'\n')
	file.write('del gmt.history psconvert* Aa* %ps%'+'\n')
	file.close()
else:
	file=open(fileoutput,'w')
	file.write('@echo off'+'\n')
	file.write('REM echo EQ Map Generator'+'\n')
	file.write('REM echo by eQ H'+'\n')
	file.write('REM echo.--------------------------------------------------------'+'\n')
	file.write('set ps=animasi.ps'+'\n')
	file.write('set title='+title+'\n')
	file.write('set fromdate='+fromdate+'\n')
	file.write('set todate='+todate+'\n')
	file.write('set datasource='+datasource+'\n')
	file.write('set x1='+str(timepos_x)+'\n')
	file.write('set y1='+str(timepos_y)+'\n')
	file.write('set x2='+str(skala_x)+'\n')
	file.write('set y2='+str(skala_y)+'\n')
	file.write('set z2='+str(skala_z)+'\n')
	file.write('set llon='+str(ll)+'\n')
	file.write('set rlon='+str(rl)+'\n')
	file.write('set blat='+str(bl)+'\n')
	file.write('set ulat='+str(ul)+'\n')
	file.write('set R=%llon%/%rlon%/%blat%/%ulat%'+'\n')
	file.write('set R_inset='+str(ll_inset)+'/'+str(rl_inset)+'/'+str(bl_inset)+'/'+str(ul_inset)+'\n')
	file.write('set R2=0/4/0/3'+'\n')
	file.write('set D=../inc/depth.cpt'+'\n')
	file.write('set tmpdata=../tmp/tmpdata.dat'+'\n')
	file.write('set output=../output/animasi.mp4'+'\n')
	file.write('set station=../data/station.sel'+'\n')
	file.write('set starttime='+str(start_time)+'\n')
	file.write('set stoptime='+str(stop_time)+'\n')
	file.write(':depthcpt'+'\n')
	file.write('if exist %D% ('+'\n')
	# file.write('echo depthcpt OK'+'\n')
	file.write('goto :prepare'+'\n')
	file.write(') else ('+'\n')
	file.write('echo generate %D%'+'\n')
	file.write('run cptdepth.bat'+'\n')
	file.write(')'+'\n')
	file.write(':prepare'+'\n')
	file.write('goto plot'+'\n')
	file.write(':plot'+'\n')
	file.write('REM MEMBUAT PETA SEISMISITAS'+'\n')
	file.write('pscoast -R%R% -JM'+str(jm)+' -Dh -B2::WSne -G245/245/200 -S150/255/255 -W0.25p,black -Lg%x2%/%y2%+c-1+w%z2%k+l+ab+jTC -Tdg%x2%/%y2%+w1.2+f1+jBC --MAP_ANNOT_MIN_SPACING=0.1p --FONT_TITLE=10 --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 -K > %ps%'+'\n')
	file.write('psxy ../inc/subduksi_moluccas.gmt -JM -R -Wthin -Sf0.8i/0.08i+l+t -Gblack -O -K >> %ps%'+'\n')
	file.write('psxy ../inc/fault_moluccas.gmt -JM -R -Wthin -O -K >> %ps%'+'\n')
	file.write('REM Data'+'\n')
	file.write('gawk -F" " "{print $2, $3}" %station% | psxy -J -R%R% -St0.3c -Wthin,black -Gblue -O -K >> %ps%'+'\n')
	file.write('gawk -F" " "{print  $2, $3, $1}" %station% | pstext -J -R -F+f8p,Helvetica+jLT -O -K >> %ps%'+'\n')
	file.write('gawk "{print $4,$5,$6,($7*0.1)^'+str(mag_size)+'}" %tmpdata% | psxy -R -JM -Sc -C%D% -Wthin -O -K >> %ps%'+'\n')
	# file.write('echo '+str(creditpos_x)+' '+str(creditpos_y)+' @@eqhalauwet | pstext -R -JM -F+f9,ZapfChancery-MediumItalic+jRB -O -K >> %ps%'+'\n')
	file.write('psimage ../inc/logo.png -R -J -Dg'+str(kompas_x)+'/'+str(kompas_y)+'+w2.3c+jLT -K -O >> %ps%'+'\n')
	file.write('pscoast -R%R_inset% -JM4 -Dh -W0.25p,black -Gwhite -S150/255/255 -B5::wsNE --MAP_FRAME_TYPE=plain --FONT_ANNOT_PRIMARY=6 -O -K >> %ps%'+'\n')
	file.write('REM psxy ../inc/subduksi_moluccas.gmt -JM -R -W0.2 -Sf0.2c/0.03c+l+t -Gblack -O -K >> %ps%'+'\n')
	file.write('REM psxy ../inc/fault_moluccas.gmt -JM -R -W0.2 -O -K >> %ps%'+'\n')
	file.write('echo %llon% %blat% > ../tmp/box'+'\n')
	file.write('echo %llon% %ulat% >> ../tmp/box'+'\n')
	file.write('echo %rlon% %ulat% >> ../tmp/box'+'\n')
	file.write('echo %rlon% %blat% >> ../tmp/box'+'\n')
	file.write('echo %llon% %blat% >> ../tmp/box'+'\n')
	file.write('psxy -R -JM ../tmp/box -Wthin,red -O -K >> %ps%'+'\n')
	if lblperiode=='Periode kurang':
		tinggi_graph=(tinggi_map-1.7)/2
		graf_yoffset=tinggi_graph+1.6
		file.write('psbasemap -JX6/'+str(tinggi_graph)+' -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -X'+str(jm+0.5)+' >> %ps%'+'\n')
		file.write('psbasemap -JX6/'+str(tinggi_graph)+' -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y'+str(graf_yoffset)+' >> %ps%'+'\n')
		file.write('gawk "{print $7}" %tmpdata% | pshistogram -JX6/'+str(tinggi_graph)+' -W0.5+l -Gblue -L0.5 -Y-'+str(graf_yoffset)+' -BESwn -Bx+lMagnitude -By+l"Number of earthquakes" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> %ps%'+'\n')
		file.write('gawk "{print $6}" %tmpdata% | pshistogram -JX6/'+str(tinggi_graph)+' -W2+l -Gblue -L0.5 -Y'+str(graf_yoffset)+' -BESwn -Bx+l"Depth (km)" -By+l"Number of earthquakes" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> %ps%'+'\n')
		file.write('echo 0.9 -0.15 "by: @@eqhalauwet" | pstext -R -Bg1x -J -F+f9,ZapfChancery-MediumItalic+jLT -Y-'+str(graf_yoffset)+' -N -O >> %ps%'+'\n')
	else:
		tinggi_graph=(tinggi_map-2.9)/3
		graf_yoffset=tinggi_graph+1.45
		file.write('psbasemap -JX5/'+str(tinggi_graph)+' -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -X'+str(jm+0.5)+' >> %ps%'+'\n')
		file.write('psbasemap -JX5/'+str(tinggi_graph)+' -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y'+str(graf_yoffset)+' >> %ps%'+'\n')
		file.write('psbasemap -JX5/'+str(tinggi_graph)+' -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y'+str(graf_yoffset)+' >> %ps%'+'\n')
		file.write('gawk "{print $7}" %tmpdata% | pshistogram -JX5/'+str(tinggi_graph)+' -W0.5+l -Gblue -L0.5 -Y-'+str(graf_yoffset*2)+' -BESwn -Bx+lMagnitude -By+l"Number of earthquakes" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> %ps%'+'\n')
		file.write('gawk "{print $6}" %tmpdata% | pshistogram -JX5/'+str(tinggi_graph)+' -W2+l -Gblue -L0.5 -Y'+str(graf_yoffset)+' -BESwn -Bx+l"Depth (km)" -By+l"Number of earthquakes" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> %ps%'+'\n')
		####
		file.write('gawk "{print $6}" %tmpdata% | pshistogram -JX5/'+str(tinggi_graph)+' -W5+l -Gblue -L0.5 -Y'+str(graf_yoffset)+' -BESwn -Bx+l"Depth (km)" -By+l"Number of earthquakes" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> %ps%'+'\n')
		file.write('echo 0.9 -0.24 "by: @@eqhalauwet" | pstext -R -Bg1x -J -F+f9,ZapfChancery-MediumItalic+jLT -Y-'+str(graf_yoffset*2)+' -N -O >> %ps%'+'\n')
	file.write('psconvert %ps% -Tj -E256 -P -A -F../output/plot.jpg'+'\n')
	file.write('del gmt.history psconvert* Aa* %ps%'+'\n')
	file.close()
print("__________________________")
print("")
print("Writting code . . .")
time.sleep(1)
print("")
if plot_animasi=='YES':
	print("Generating video . . . ")
else:
	print("Generating map . . . ")
print("")
p = Popen(["plot.bat"], shell=True, cwd=r'bin')
stdout, stderr = p.communicate()
time.sleep(3)
print("__________________________")
if plot_animasi=='YES':
	print('Animation Generated on "output/animasi.mp4"')
else:
	print('Map Generated on "output/plot.jpg"')
print("")
time.sleep(0.5)
print("Closing application . . . ")
time.sleep(2)