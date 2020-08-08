import time
from subprocess import Popen
from bin.crossection import crossection_strike_dip
from bin.crossection import crossection_strike_line
from bin.crossection import crossection_dip_line
from bin.layout import set_pos
from bin.reformat_data import from_sdigb
# baca parameter input (tambah jenis input data dari SDIGB (default atau hypodd)) reformat datetime satu variabel
# baca data output ke datatmp (tambah output waktu start dan end) cari konversi waktu ke detik, start time - 2 jam
parameter='data\/parameter.inp'
fileoutput='bin\/animasi.bat'
datagempa='data\/hypocenter.dat'
tmpdata='tmp\/tmpdata.dat'
title=''; area=1; input=0; fps=10
lon_center=0; lat_center=0; radius_center=0
left_lon=0; right_lon=0; bot_lat=0; up_lat=0
jm=15
dur=0
tzsign=''; tzone=0; tzname='UTC'
start_time=0; stop_time=0
lat=0; lon=0; depth=0; mag=0; mtype=''
strike1=0; strike2=0; dip1=0; dip2=0; slip1=0; slip2=0
cslength=0; cswidth=0
maxelev=0; maxdepth=0
plot_topo='NO'
print('Epicenter Animation Generator')
print('by eQ H')
print('--------------------------------------------------------')
print('')
print(str(title))
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
	if len(baris[i])>0 and baris[i][0]=='Durasi_Animasi':
		dur=int(baris[i+1][0])
	if len(baris[i])>0 and baris[i][0]=='Frame_per_second':
		fps=int(baris[i+1][0])
	if len(baris[i])>0 and baris[i][0]=='Input_Data':
		input=int(baris[i+1][0])
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
	i = i+1
if input==0:
	print('Input data SDIGB')
	## refromat data
	start_time, time_sec=from_sdigb(datagempa, tmpdata, tzsign, tzone, tzname)
elif input==1:
	print('Input data hypoDD')
else:
	print('Input data default [SDIGB]')
stop_time=time_sec
# hitung batasan peta
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
# (Diameter Peta / 2 (degree))
# mapoffs=int(math.ceil(float(cslength)/222.7))
# rl=float(lon)+mapoffs
# ll=float(lon)-mapoffs
# ul=float(lat)+mapoffs
# bl=float(lat)-mapoffs
## tentukan posisi inset, logo, waktu, dan kredit
ll_inset, rl_inset, bl_inset, ul_inset, logo_x, logo_y, timepos_x, timepos_y, creditpos_x, creditpos_y = set_pos(ll, rl, bl, ul, jm)
if dur > 300:
	print('durasi animasi > 5menit, butuh waktu lama rendering.')
	print('stop proses (ctrl+c) dan kecilkan Durasi_Animasi pada parameter.inp untuk mempercepat rendering.')
time_sampling=int((stop_time-start_time)/(dur*fps))
time_delay=int(100/fps)
start_time=int(start_time-1.5*fps*time_sampling)
stop_time=int(stop_time+1.5*fps*time_sampling)
print('start_time:'+str(start_time)+', stop_time:'+str(stop_time)+', sampling_tpf'+str(time_sampling)+', time_delay:'+str(time_delay))
## tentukan bidang potong crosssection tegak lurus strike dan dip 2D bidang 360 derajad
str1, dp1, az1 = crossection_strike_dip(strike1, dip1)
str2, dp2, az2 = crossection_strike_dip(strike2, dip2)
print('Koordinat = %f %f %f' %(float(lat),float(lon),float(depth)))
print('Magnitudo = %s' %(mag))
print('Nodal Plane 1 = %3i %2i %3i' %(int(strike1),int(dip1),int(slip1)))
print('Nodal Plane 2 = %3i %2i %3i' %(int(strike2),int(dip2),int(slip2)))
print('Batas koordinat= %3.2f %3.2f %2.2f %2.2f' %(rl,ll,ul,bl))
print('Crosssection A-B = %s' %(str1))
print('Crosssection C-B = %s' %(str2))
print('DIP Crosssection A-B = %s' %(dp1))
print('DIP Crosssection C-B = %s' %(dp2))
print('Plot Topography line = %s' %(plot_topo))
## hitung line crosssection strike (startlon1,startlat1 - endlon1,endlat1)
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
# hitung rasio range long/lat & posisi simbol peta
x1=ll+(rl-ll)/7
x2=ll+(rl-ll)/7
y1=ul-(ul-bl)/5
y2=bl+(ul-bl)/12
file=open(fileoutput,'w')
file.write('@echo off'+'\n')
file.write('echo EQ Map Generator'+'\n')
file.write('echo by eQ H'+'\n')
file.write('echo.--------------------------------------------------------'+'\n')
file.write('set ps=animasi.ps'+'\n')
file.write('set llon='+str(ll)+'\n')
file.write('set rlon='+str(rl)+'\n')
file.write('set blat='+str(bl)+'\n')
file.write('set ulat='+str(ul)+'\n')
file.write('set R=%llon%/%rlon%/%blat%/%ulat%'+'\n')
file.write('set R_inset='+str(ll_inset)+'/'+str(rl_inset)+'/'+str(bl_inset)+'/'+str(ul_inset)+'\n')
file.write('set D=../inc/depth.cpt'+'\n')
file.write('set tmpdata=../tmp/tmpdata.dat'+'\n')
file.write('set output=../output/animasi.mp4'+'\n')
file.write('set starttime='+str(start_time)+'\n')
file.write('set stoptime='+str(stop_time)+'\n')
file.write('REM time sampling per frame (second)'+'\n')
file.write('set tpf='+str(time_sampling)+'\n')
file.write('REM frame per second (ffmpeg)'+'\n')
file.write('set fps='+str(fps)+'\n')
file.write('REM time delay every frame (gm)'+'\n')
file.write('set delay='+str(time_delay)+'\n')
file.write('set replay=0'+'\n')
file.write(':depthcpt'+'\n')
file.write('if exist %D% ('+'\n')
file.write('echo depthcpt OK'+'\n')
file.write('goto :prepare'+'\n')
file.write(') else ('+'\n')
file.write('echo generate %D%'+'\n')
file.write('run cptdepth.bat'+'\n')
file.write(')'+'\n')
file.write(':prepare'+'\n')
file.write('if exist frame\ ('+'\n')
file.write('echo deleting temporary frame'+'\n')
file.write('rd /S /Q frame'+'\n')
file.write(')'+'\n')
file.write('mkdir frame'+'\n')
file.write('set /a framenumber = -1'+'\n')
file.write(':loopplot'+'\n')
file.write('set /a framenumber = %framenumber% + 1'+'\n')
file.write('set /a starttime= %starttime% + %tpf%'+'\n')
file.write('if %starttime% GTR %stoptime% goto finishplot'+'\n')
file.write('goto plot'+'\n')
file.write(':plot'+'\n')
file.write('REM MEMBUAT PETA SEISMISITAS'+'\n')
file.write('pscoast -R%R% -JM'+str(jm)+' -Dh -B2::WSne -G245/245/200 -S150/255/255 -W0.25p,black -K > %ps%'+'\n')
file.write('psxy ../inc/subduksi_moluccas.gmt -JM -R -Wthin -Sf0.8i/0.08i+l+t -Gblack -O -K >> %ps%'+'\n')
file.write('psxy ../inc/fault_moluccas.gmt -JM -R -Wthin -O -K >> %ps%'+'\n')
file.write('gawk "{if ($8>%starttime%-%tpf% && $8<=%starttime%) print $4,$5,$6,$7*0.03}" %tmpdata% | psxy -R -JM -Sci -C%D% -Wthin -O -K >> %ps%'+'\n')
file.write('gawk "{if ($8>%starttime%-%tpf%-%tpf% && $8<=%starttime%-%tpf%) print $4,$5,$6,$7*0.03}" %tmpdata% | psxy -R -JM -Sci -C%D% -Wthin -O -t5 -K >> %ps%'+'\n')
file.write('gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%) print $4,$5,$6,$7*0.03}" %tmpdata% | psxy -R -JM -Sci -C%D% -Wthin -O -t10 -K >> %ps%'+'\n')
file.write('gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.03}" %tmpdata% | psxy -R -JM -Sci -C%D% -Wthin -O -t15 -K >> %ps%'+'\n')
file.write('gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.03}" %tmpdata% | psxy -R -JM -Sci -C%D% -Wthin -O -t20 -K >> %ps%'+'\n')
file.write('gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.03}" %tmpdata% | psxy -R -JM -Sci -C%D% -Wthin -O -t25 -K >> %ps%'+'\n')
file.write('gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.03}" %tmpdata% | psxy -R -JM -Sci -C%D% -Wthin -O -t30 -K >> %ps%'+'\n')
file.write('gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.03}" %tmpdata% | psxy -R -JM -Sci -C%D% -Wthin -O -t35 -K >> %ps%'+'\n')
file.write('gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.03}" %tmpdata% | psxy -R -JM -Sci -C%D% -Wthin -O -t40 -K >> %ps%'+'\n')
file.write('gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.03}" %tmpdata% | psxy -R -JM -Sci -C%D% -Wthin -O -t45 -K >> %ps%'+'\n')
file.write('gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.03}" %tmpdata% | psxy -R -JM -Sci -C%D% -Wthin -O -t50 -K >> %ps%'+'\n')
file.write('gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.03}" %tmpdata% | psxy -R -JM -Sci -C%D% -Wthin -O -t55 -K >> %ps%'+'\n')
file.write('gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.03}" %tmpdata% | psxy -R -JM -Sci -C%D% -Wthin -O -t60 -K >> %ps%'+'\n')
file.write('gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.03}" %tmpdata% | psxy -R -JM -Sci -C%D% -Wthin -O -t65 -K >> %ps%'+'\n')
file.write('gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.03}" %tmpdata% | psxy -R -JM -Sci -C%D% -Wthin -O -t70 -K >> %ps%'+'\n')
file.write('gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.03}" %tmpdata% | psxy -R -JM -Sci -C%D% -Wthin -O -t75 -K >> %ps%'+'\n')
file.write('gawk "{if ($8<%starttime%) print $4,$5,$6,$7*0.03}" %tmpdata% | psxy -R -JM -Sci -C%D% -Wthin -O -t80 -K >> %ps%'+'\n')
file.write('gawk "BEGIN {print strftime(\\"%%d-%%m-%%Y %%H:%%M:%%S '+tzname+'\\",%starttime%);}" | gawk "{print '+str(timepos_x)+','+str(timepos_y)+',$0}" | pstext -R -JM -F+f8,Helvetica -O -K >> %ps%'+'\n')
file.write('echo '+str(creditpos_x)+' '+str(creditpos_y)+' @@eqhalauwet | pstext -R -JM -F+f9,ZapfChancery-MediumItalic -O -K >> %ps%'+'\n')
file.write('psimage ../inc/logo.png -Dx0/0+w2.3c -X'+logo_x+' -Y'+logo_y+' -K -O >> %ps%'+'\n')
file.write('pscoast -R%R_inset% -JM4 -Dh -W0.25p,black -Gwhite -S150/255/255 -B5::wsNE --MAP_FRAME_TYPE=plain --FONT_ANNOT_PRIMARY=8p -X-'+logo_x+' -Y-'+logo_y+' -O -K >> %ps%'+'\n')
file.write('REM psxy ../inc/subduksi_moluccas.gmt -JM -R -W0.2 -Sf0.2c/0.03c+l+t -Gblack -O -K >> %ps%'+'\n')
file.write('REM psxy ../inc/fault_moluccas.gmt -JM -R -W0.2 -O -K >> %ps%'+'\n')
file.write('echo %llon% %blat% > ../tmp/box'+'\n')
file.write('echo %llon% %ulat% >> ../tmp/box'+'\n')
file.write('echo %rlon% %ulat% >> ../tmp/box'+'\n')
file.write('echo %rlon% %blat% >> ../tmp/box'+'\n')
file.write('echo %llon% %blat% >> ../tmp/box'+'\n')
file.write('psxy -R -JM ../tmp/box -Wthin,red -O >> %ps%'+'\n')
file.write('psconvert %ps% -Tg -E256 -P -A -Fframe/frame-%framenumber%'+'\n')
file.write('goto loopplot'+'\n')
file.write(':finishplot'+'\n')
file.write('ffmpeg -framerate %fps% -i frame/frame-%%d.png -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p %output%'+'\n')
file.write('REM gm convert -delay %delay% -loop %replay% frame/frame-*.png %output%'+'\n')
file.write('REM del %tmpdata% gmt.history animasi.bat ../tmp/box %ps% '+'\n')
file.write('REM rd /S /Q frame'+'\n')
file.close()
print("__________________________")
print("")
print("Writting code . . .")
time.sleep(1)
print("")
print("Generating video . . . ")
print("")
p = Popen(["animasi.bat"], shell=True, cwd=r'bin')
stdout, stderr = p.communicate()
time.sleep(3)
print("__________________________")
print("Animation Generated on output/animasi.mp4")
print("")
time.sleep(0.5)
print("Closing application . . . ")
time.sleep(2)