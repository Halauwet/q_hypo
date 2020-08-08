import os
import time
import math
from subprocess import Popen
from bin.crossection import crossection_strike_dip, crossection_strike_line, crossection_dip_line
from bin.layout import set_pos, set_legend, mag_scale
from bin.reformat_data import *  # REFORMAT GANTI DENGAN MODUL "DATA_RFW"

parameter = 'parameter.inp'
fileoutput = os.path.join('bin', 'plot.bat')
legend = os.path.join('bin', 'legenda.bat')
datagempa = os.path.join('data', 'hypocenter.dat')
datadirasakan = os.path.join('data', 'dirasakan.dat')
tmpdata = os.path.join('tmp', 'tmpdata.dat')
tmpdirasakan = os.path.join('tmp', 'tmpdirasakan.dat')

# Parameter Legenda + psscale depth
num_M = 5  # jumlah magnitudo pada legend
min_M = 3  # minimun magnitudo
legenda = os.path.join('tmp', 'legenda')

title = ''
fromdate = ''
todate = ''
datasource = ''
area = 1
inp_type = 0
fps = 10
lon_center = 0
lat_center = 0
radius_center = 0
left_lon = 0
right_lon = 0
bot_lat = 0
up_lat = 0
jm = 15
dur = 0
tzsign = ''
tzone = 0
tzname = 'UTC'
periode = ''
ot_start = 0
ot_stop = 0
start_time = 0
stop_time = 0
jumlah_event = 0
jumlah_dirasakan = 0
lat = 0
lon = 0
depth = 0
mag = 0
mtype = ''
epic_size = 0.3
strike1 = 0
strike2 = 0
dip1 = 0
dip2 = 0
slip1 = 0
slip2 = 0
cslength = 0
cswidth = 0
maxelev = 0
maxdepth = 0
M_scale = 'quadrat'  # option: linear or quadrat
M_linear_size = 0.044  # set linear mag multiplier (same as legend.bat value)
plot_animasi = 'NO'  # TODO: change option using flag
plot_crossect = 'NO'
plot_dirasakan = 'NO'
plot_topo = 'NO'
dpi = 512

print('Epicenter Animation Generator')
print('by eQ H')
print('--------------------------------------------------------')
print('')

file = open(parameter, 'r')
baris = file.readlines()
for i in range(len(baris)):
    baris[i] = baris[i].split()
file.close()

i = 0
while i < len(baris):

    if len(baris[i]) > 0 and baris[i][0] == 'Title':
        title = ' '.join(baris[i + 1])

    if len(baris[i]) > 0 and baris[i][0] == 'Plot_Area':
        area = int(baris[i + 3][0])
        if area == 0:
            lon_center = ('%.4f' % float(baris[i + 4][0]))
            lat_center = ('%.4f' % float(baris[i + 4][1]))
            radius_center = int(baris[i + 4][2])
        else:
            left_lon = ('%.4f' % float(baris[i + 4][0]))
            right_lon = ('%.4f' % float(baris[i + 4][1]))
            bot_lat = ('%.4f' % float(baris[i + 4][2]))
            up_lat = ('%.4f' % float(baris[i + 4][3]))

    if len(baris[i]) > 0 and baris[i][0] == 'From_Date':
        fromdate = ' '.join(baris[i + 1])

    if len(baris[i]) > 0 and baris[i][0] == 'To_Date':
        todate = ' '.join(baris[i + 1])

    if len(baris[i]) > 0 and baris[i][0] == 'Input_Data':
        inp_type = int(baris[i + 1][0])

    if len(baris[i]) > 0 and baris[i][0] == 'Plot_Animasi' and baris[i + 1][0] == 'Y' or \
            len(baris[i]) > 0 and baris[i][0] == 'Plot_Animasi' and baris[i + 1][0] == 'y':
        plot_animasi = 'YES'

    if len(baris[i]) > 0 and baris[i][0] == 'Plot_Dirasakan' and baris[i + 1][0] == 'Y' or len(baris[i]) > 0 and \
            baris[i][0] == 'Plot_Dirasakan' and baris[i + 1][0] == 'y':
        plot_dirasakan = 'YES'

    if len(baris[i]) > 0 and baris[i][0] == 'Durasi_Animasi':
        dur = int(baris[i + 1][0])

    if len(baris[i]) > 0 and baris[i][0] == 'Frame_per_second':
        fps = int(baris[i + 1][0])

    if len(baris[i]) > 0 and baris[i][0] == 'Convert':
        tzsign = baris[i + 1][0]
        tzone = int(baris[i + 1][1])
        tzname = baris[i + 1][2]

    if len(baris[i]) > 0 and baris[i][0] == 'Frekuensi_waktu':
        periode = baris[i + 1][0]

    if len(baris[i]) > 0 and baris[i][0] == 'Plot_Crosssection?' and baris[i + 1][0] == 'Y' or len(baris[i]) > 0 and \
            baris[i][0] == 'Plot_Crosssection?' and baris[i + 1][0] == 'y':
        plot_crossect = 'YES'

    if len(baris[i]) > 0 and baris[i][0] == 'Mainshock_Hypocenter':
        lon = ('%.4f' % float(baris[i + 1][0]))
        lat = ('%.4f' % float(baris[i + 1][1]))
        depth = ('%.2f' % float(baris[i + 1][2]))

    if len(baris[i]) > 0 and baris[i][0] == 'Mag_Symbol':
        M_scale = baris[i + 1][0]
        M_linear_size = ('%.4f' % float(baris[i + 2][0]))

    if len(baris[i]) > 0 and baris[i][0] == 'Magnitude':
        mag = ('%.1f' % float(baris[i + 1][0]))
        mtype = baris[i + 1][1]
        if M_scale == 'linear':
            epic_size = float(mag) * float(M_linear_size)
        elif M_scale == 'quadrat':
            # Editted layout 140520
            epic_size = 0.7 * mag_scale(float(mag), M_scale, float(M_linear_size))
        else:
            print()
            print('Periksa tipe ukuran simbol magnitudo (linear or quadrat)')
            print()

    if len(baris[i]) > 0 and baris[i][0] == 'Nodal':
        strike1 = baris[i + 1][0]
        dip1 = baris[i + 1][1]
        slip1 = baris[i + 1][2]
        strike2 = baris[i + 2][0]
        dip2 = baris[i + 2][1]
        slip2 = baris[i + 2][2]

    if len(baris[i]) > 0 and baris[i][0] == 'Crossection_Length':
        cslength = int(baris[i + 1][0])
        cswidth = cslength / 2
    # cslength = panjang patahan; cswidth = 1/2 panjang patahan ke kiri + 1/2 panjang patahan ke kanan)

    if len(baris[i]) > 0 and baris[i][0] == 'Max':
        maxdepth = baris[i + 1][0]

    if len(baris[i]) > 0 and baris[i][0] == '#Max':
        maxdepth = int(math.ceil(float(depth) * 2 / 50)) * 50

    if len(baris[i]) > 0 and baris[i][0] == 'Plot_Elevation' and baris[i + 1][0] == 'Y' or len(baris[i]) > 0 and \
            baris[i][0] == 'Plot_Elevation' and baris[i + 1][0] == 'y':
        plot_topo = 'YES'
        maxelev = baris[i + 1][1]

    if len(baris[i]) > 0 and baris[i][0] == 'Data_source':
        datasource = ' '.join(baris[i + 1])

    i += 1

print(title)
print('')
if inp_type == 0:
    # refromat data
    # if plot_dirasakan=='YES':
    ot_start, ot_stop, jumlah_dirasakan = sdigb_to_geoq(datadirasakan, tmpdirasakan, tzsign, tzone, tzname)
    ot_start, ot_stop, jumlah_event = sdigb_to_geoq(datagempa, tmpdata, tzsign, tzone, tzname)

elif inp_type == 1:
    if plot_dirasakan == 'YES':
        ot_stop, ot_start, jumlah_dirasakan = hypodd_to_geoq(datadirasakan, tmpdirasakan, tzsign, tzone, tzname)
    ot_stop, ot_start, jumlah_event = hypodd_to_geoq(datagempa, tmpdata, tzsign, tzone, tzname)

elif inp_type == 2:
    if plot_dirasakan == 'YES':
        ot_start, ot_stop, jumlah_dirasakan = ascii_to_geoq(datadirasakan, tmpdirasakan, tzsign, tzone, tzname)
    ot_start, ot_stop, jumlah_event = ascii_to_geoq(datagempa, tmpdata, tzsign, tzone, tzname)

else:

    print('Input data default')
    if plot_dirasakan == 'YES':
        ot_start, ot_stop, jumlah_dirasakan = sdigb_to_geoq(datadirasakan, tmpdirasakan, tzsign, tzone, tzname)
    ot_start, ot_stop, jumlah_event = sdigb_to_geoq(datagempa, tmpdata, tzsign, tzone, tzname)

eq_period = ot_stop - ot_start
# HITUNG Frekuensi Gempa/periode waktu
# lblperiode='Periode kurang'

if periode == 'hari':
    tab_data = '$4'
    lblperiode = 'Tanggal (UTC)'
elif periode == 'bulan':
    tab_data = '$3'
    lblperiode = 'Bulan'
elif periode == 'tahun':
    tab_data = '$2'
    lblperiode = 'Tahun'
else:
    lblperiode = 'Periode kurang'  # TODO: plot time period histogram using timeseries

if ot_start > ot_stop:
    n = ot_start
    ot_start = ot_stop
    ot_stop = n
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
if dur > 300:
    print()
    print('durasi animasi > 5menit, butuh waktu lama rendering.')
    print('stop proses (ctrl+c) dan kecilkan Durasi_Animasi pada parameter.inp untuk mempercepat rendering.')
    print()

if plot_animasi == 'YES':
    if plot_crossect == 'NO':
        if dur <= 12:
            print()
            print('Durasi terlalu singkat. Tambah durasi')
            print()
        dur = dur - 8.3
    else:
        dur = dur - 3
    time_sampling = int((ot_stop - ot_start) / (dur * fps))
    time_delay = int(100 / fps)
    if plot_crossect == 'NO':
        start_time = int(ot_start - 0.5 * fps * time_sampling)
        stop_time = int(ot_stop + 0.1 * fps * time_sampling)
    else:
        start_time = int(ot_start - 2 * fps * time_sampling)
        stop_time = int(ot_stop + 1 * fps * time_sampling)
    # set transparansi
    transp_max = 70
    transp_step = 20 / fps
    print('Plot video animasi')
    print('video start_time: ' + str(start_time))
    print('video stop_time: ' + str(stop_time))
    print('sampling_tpf: ' + str(time_sampling))
    print('fps: ' + str(fps))
else:
    print('Plot seismicity map')
if plot_crossect == 'YES':
    # tentukan bidang potong crosssection tegak lurus strike dan dip 2D bidang 360 derajad
    str1, dp1, az1 = crossection_strike_dip(strike1, dip1)
    str2, dp2, az2 = crossection_strike_dip(strike2, dip2)
    # hitung line crosssection strike (startlon1,startlat1 - endlon1,endlat1)
    startlon1, startlat1, endlon1, endlat1 = crossection_strike_line(lon, lat, str1, cslength)
    file = open('tmp/LINE_AB', 'w')
    file.write('%s %s\n%s %s' % (str(startlon1), str(startlat1), str(endlon1), str(endlat1)) + '\n')
    file.close()
    file = open('tmp/TEXT_A', 'w')
    file.write('%s %s A' % (str(startlon1), str(startlat1)) + '\n')
    file.close()
    file = open('tmp/TEXT_B', 'w')
    file.write('%s %s B' % (str(endlon1), str(endlat1)) + '\n')
    file.close()
    startlon2, startlat2, endlon2, endlat2 = crossection_strike_line(lon, lat, str2, cslength)
    file = open('tmp/LINE_CD', 'w')
    file.write('%s %s\n%s %s' % (str(startlon2), str(startlat2), str(endlon2), str(endlat2)) + '\n')
    file.close()
    file = open('tmp/TEXT_C', 'w')
    file.write('%s %s C' % (str(startlon2), str(startlat2)) + '\n')
    file.close()
    file = open('tmp/TEXT_D', 'w')
    file.write('%s %s D' % (str(endlon2), str(endlat2)) + '\n')
    file.close()
    # hitung line crosssection dip
    xab0, y0, xab2, y2 = crossection_dip_line(depth, maxdepth, dip1, dp1)
    file = open('tmp/DIP_AB', 'w')
    file.write(str(xab0) + ' ' + str(y0) + '\n' + str(xab2) + ' ' + str(y2))
    file.close()
    xcd0, y0, xcd2, y2 = crossection_dip_line(depth, maxdepth, dip2, dp2)
    file = open('tmp/DIP_CD', 'w')
    file.write(str(xcd0) + ' ' + str(y0) + '\n' + str(xcd2) + ' ' + str(y2))
    file.close()
    # hitung batasan peta
    # (Diameter Peta / 2 (degree))
    # if startlon1 < ll or startlon2 < ll or endlon1 > rl or endlon2 > rl or startlat1 > ul or startlat2 > ul or
    # endlat1 < bl or endlat2 < bl:
    print('Map area automatic from mainshock')
    mapoffs = int(math.ceil(float(cslength) / 222.7))
    rl = float(lon) + mapoffs
    ll = float(lon) - mapoffs
    ul = float(lat) + mapoffs
    bl = float(lat) - mapoffs
else:
    if area == 0:
        ll = float(lon_center) - radius_center
        rl = float(lon_center) + radius_center
        bl = float(lat_center) - radius_center
        ul = float(lat_center) + radius_center
    else:
        ll = float(left_lon)
        rl = float(right_lon)
        bl = float(bot_lat)
        ul = float(up_lat)
# print(ll, rl, bl, ul, jm, cslength)
# tentukan posisi inset, logo, waktu, dan kredit
ll_inset, rl_inset, bl_inset, ul_inset, logo_y1, logo_y2, logo_y3, kompas_x, kompas_y, skala_x, skala_y, skala_z, \
timepos_x, timepos_y, creditpos_x, creditpos_y, tinggi_map = set_pos(ll, rl, bl, ul, jm)
if plot_crossect == 'YES':
    print('')
    print('CROSS SECTION PARAMETER:')
    print('Koordinat Epicenter= %f %f %f' % (float(lat), float(lon), float(depth)))
    print('Magnitudo = %s' % mag)
    print('Nodal Plane 1 = %3i %2i %3i' % (int(strike1), int(dip1), int(slip1)))
    print('Nodal Plane 2 = %3i %2i %3i' % (int(strike2), int(dip2), int(slip2)))
    print('Batas koordinat= %3.2f %3.2f %2.2f %2.2f' % (rl, ll, ul, bl))
    print('Crosssection A-B = %s' % str1)
    print('Crosssection C-B = %s' % str2)
    print('DIP Crosssection A-B = %s' % dp1)
    print('DIP Crosssection C-B = %s' % dp2)
    print('Plot Topography line = %s' % plot_topo)
    file = open(legend, 'w')
    file.write('echo G -0.05>%L%' + '\n')
    file.write('echo N 5 >>%L%' + '\n')
    file.write('::echo V 0 1p>>%L%' + '\n')
    file.write('echo L 8 4 C Depth (km)>>%L%' + '\n')
    file.write('echo L 8 4 C "M = 3">>%L%' + '\n')
    file.write('echo L 8 4 C "M = 4">>%L%' + '\n')
    file.write('echo L 8 4 C "M = 5">>%L%' + '\n')
    file.write('echo L 8 4 C "M = \\076 5">>%L%' + '\n')
    file.write('::echo V 0 1p>>%L%' + '\n')
    file.write('::echo D 0 1p>>%L%' + '\n')
    file.write('::echo V 0 1p>>%L%' + '\n')
    file.write('echo L 8 4 C \\074 60>>%L%' + '\n')
    file.write('echo S 0.5 c ' + str(mag_scale(3, M_scale, float(M_linear_size))) + ' red 0.5p 0.1>>%L%' + '\n')
    file.write('echo S 0.5 c ' + str(mag_scale(4, M_scale, float(M_linear_size))) + ' red 0.5p 0.1>>%L%' + '\n')
    file.write('echo S 0.5 c ' + str(mag_scale(5, M_scale, float(M_linear_size))) + ' red 0.5p 0.1>>%L%' + '\n')
    file.write('echo S 0.5 c ' + str(mag_scale(6, M_scale, float(M_linear_size))) + ' red 0.5p 0.1>>%L%' + '\n')
    file.write('echo L 8 4 C 60 - 300>>%L%' + '\n')
    file.write('echo S 0.5 c ' + str(mag_scale(3, M_scale, float(M_linear_size))) + ' yellow 0.5p 0.1>>%L%' + '\n')
    file.write('echo S 0.5 c ' + str(mag_scale(4, M_scale, float(M_linear_size))) + ' yellow 0.5p 0.1>>%L%' + '\n')
    file.write('echo S 0.5 c ' + str(mag_scale(5, M_scale, float(M_linear_size))) + ' yellow 0.5p 0.1>>%L%' + '\n')
    file.write('echo S 0.5 c ' + str(mag_scale(6, M_scale, float(M_linear_size))) + ' yellow 0.5p 0.1>>%L%' + '\n')
    file.write('echo L 8 4 C \\076 300>>%L%' + '\n')
    file.write('echo S 0.5 c ' + str(mag_scale(3, M_scale, float(M_linear_size))) + ' green 0.5p 0.1>>%L%' + '\n')
    file.write('echo S 0.5 c ' + str(mag_scale(4, M_scale, float(M_linear_size))) + ' green 0.5p 0.1>>%L%' + '\n')
    file.write('echo S 0.5 c ' + str(mag_scale(5, M_scale, float(M_linear_size))) + ' green 0.5p 0.1>>%L%' + '\n')
    file.write('echo S 0.5 c ' + str(mag_scale(6, M_scale, float(M_linear_size))) + ' green 0.5p 0.1>>%L%' + '\n')
    file.write('echo G 0.4>>%L%' + '\n')
    file.write('::echo V 0 1p>>%L%' + '\n')
    file.write('::echo D 0 1p>>%L%' + '\n')
    file.write('::echo V 0 1p>>%L%' + '\n')
    file.close()
    
    file = open(fileoutput, 'w')
    file.write('@echo off' + '\n')
    file.write('REM echo EQ Map Generator' + '\n')
    file.write('REM echo by eQ H' + '\n')
    file.write('REM echo.--------------------------------------------------------' + '\n')
    file.write('REM Parameter Gempa' + '\n')
    file.write('set title=' + title + '\n')
    file.write('set mainlat=' + str(lat) + '\n')
    file.write('set mainlon=' + str(lon) + '\n')
    file.write('set maindepth=' + str(depth) + '\n')
    file.write('set mainmag=' + str(mag) + '\n')
    file.write('set typemag=' + mtype + '\n')
    file.write('set strike1=' + strike1 + '\n')
    file.write('set strike2=' + strike2 + '\n')
    file.write('set dip1=' + dip1 + '\n')
    file.write('set dip2=' + dip2 + '\n')
    file.write('set slip1=' + slip1 + '\n')
    file.write('set slip2=' + slip2 + '\n')
    file.write('REM length=panjang cross section' + '\n')
    file.write('set length=' + str(cslength) + '\n')
    file.write('set width=' + str(cswidth) + '\n')
    file.write('set AC=-%width%' + '\n')
    file.write('set BD=%width%' + '\n')
    file.write('set maxelev=' + str(maxelev) + '\n')
    file.write('set maxdepth=' + str(maxdepth) + '\n')
    file.write('set x1=' + str(kompas_x) + '\n')
    file.write('set y1=' + str(kompas_y) + '\n')
    file.write('set x2=' + str(skala_x) + '\n')
    file.write('set y2=' + str(skala_y) + '\n')
    file.write('set z2=' + str(skala_z) + '\n')
    file.write('set str1=' + str(str1) + '\n')
    file.write('set str2=' + str(str2) + '\n')
    file.write('set azm1=' + str(az1) + '\n')
    file.write('set azm2=' + str(az2) + '\n')
    file.write('set startlat1=' + str(startlat1) + '\n')
    file.write('set startlon1=' + str(startlon1) + '\n')
    file.write('set startlat2=' + str(startlat2) + '\n')
    file.write('set startlon2=' + str(startlon2) + '\n')
    file.write('set endlat1=' + str(endlat1) + '\n')
    file.write('set endlon1=' + str(endlon1) + '\n')
    file.write('set endlat2=' + str(endlat2) + '\n')
    file.write('set endlon2=' + str(endlon2) + '\n')
    file.write('REM Set Parameter Peta' + '\n')
    file.write('set ps=animasi.ps' + '\n')
    file.write('set D=../inc/depth.cpt' + '\n')
    file.write('set L=../tmp/legenda' + '\n')
    file.write('set epic=%mainlon%/%mainlat%' + '\n')
    file.write('set tmpdata=../tmp/tmpdata.dat' + '\n')
    file.write('set tmpdirasakan=../tmp/tmpdirasakan.dat' + '\n')
    file.write('set station=../data/station.sel' + '\n')
    file.write('set focal=../data/psmeca.dat' + '\n')
    file.write('set output=../output/animasi.mp4' + '\n')
    file.write('set indo=../inc/indonesia.nc' + '\n')
    file.write('set topo=../inc/my_etopo.cpt' + '\n')
    file.write('set fault=../inc/fault_moluccas.gmt' + '\n')
    file.write('set subduction=../inc/subduksi_moluccas.gmt' + '\n')
    # file.write('set trench_a=../inc/trench-a.gmt'+'\n')
    # file.write('set trench_b=../inc/trench-b.gmt'+'\n')
    # file.write('set thrust=../inc/thrust.gmt'+'\n')
    # file.write('set transform=../inc/transform.gmt'+'\n')
    file.write('REM Plot Area' + '\n')
    file.write('set llon=' + str(ll) + '\n')
    file.write('set rlon=' + str(rl) + '\n')
    file.write('set blat=' + str(bl) + '\n')
    file.write('set ulat=' + str(ul) + '\n')
    file.write('set R=%llon%/%rlon%/%blat%/%ulat%' + '\n')
    file.write('set R_inset=' + str(ll_inset) + '/' + str(rl_inset) + '/' + str(bl_inset) + '/' + str(ul_inset) + '\n')
    file.write('set R2=%AC%/%BD%/-%maxdepth%/0' + '\n')
    file.write('set R3=0/%length%/-%maxdepth%/0' + '\n')
    file.write('set R4=0/%length%/-%maxelev%/%maxelev%' + '\n')
    file.write('set starttime=' + str(start_time) + '\n')
    file.write('set stoptime=' + str(stop_time) + '\n')
    if plot_animasi == 'YES':
        file.write('REM time sampling per frame (second)' + '\n')
        file.write('set tpf=' + str(time_sampling) + '\n')
        file.write('REM frame per second (ffmpeg)' + '\n')
        file.write('set fps=' + str(fps) + '\n')
        file.write('REM time delay every frame (gm)' + '\n')
        file.write('set delay=' + str(time_delay) + '\n')
        file.write('set replay=0' + '\n')
    file.write('REM Proyeksi' + '\n')
    file.write('set proyeksi1=../tmp/projection1.tmp' + '\n')
    file.write('set proyeksi2=../tmp/projection2.tmp' + '\n')
    file.write('set lineAB=../tmp/LINE_AB' + '\n')
    file.write('set lineCD=../tmp/LINE_CD' + '\n')
    file.write('set dip_AB=../tmp/DIP_AB' + '\n')
    file.write('set dip_CD=../tmp/DIP_CD' + '\n')
    file.write('set text_A=../tmp/TEXT_A' + '\n')
    file.write('set text_B=../tmp/TEXT_B' + '\n')
    file.write('set text_C=../tmp/TEXT_C' + '\n')
    file.write('set text_D=../tmp/TEXT_D' + '\n')
    file.write('set track=../tmp/track' + '\n')
    file.write('set trackAB=../tmp/trackAB' + '\n')
    file.write('set trackCD=../tmp/trackCD' + '\n')
    file.write('set sealevel=../tmp/sealevel.line' + '\n')
    file.write(':TOPOCPT' + '\n')
    file.write('if exist %topo% (' + '\n')
    # file.write('echo topo OK'+'\n')
    file.write('goto :DEPTHCPT' + '\n')
    file.write(') else (' + '\n')
    file.write('echo generate %topo%' + '\n')
    file.write('makecpt -Z -Cetopo1 > %topo%' + '\n')
    file.write('REM makecpt -Cred,yellow,green -T0,60,300,700 -Z0/500  > %topo%' + '\n')
    file.write(')' + '\n')
    file.write(':DEPTHCPT' + '\n')
    file.write('if exist %D% (' + '\n')
    # file.write('echo depthcpt OK'+'\n')
    file.write('goto :PROJECT' + '\n')
    file.write(') else (' + '\n')
    file.write('echo generate %D%' + '\n')
    file.write('run cptdepth_std.bat' + '\n')
    file.write(')' + '\n')
    # file.write(':LEGEND'+'\n')
    # file.write('run legenda.bat'+'\n')
    file.write(':PROJECT' + '\n')
    file.write(
        'gawk "{print $6, $7, $8, $9, $10}" %tmpdata% | project  -L-5/5 -C%epic% -A%azm1% -Fxyzpqrs '
        '-Q > %proyeksi1%' + '\n')
    file.write(
        'gawk "{print $6, $7, $8, $9, $10}" %tmpdata% | project  -L-5/5 -C%epic% -A%azm2% -Fxyzpqrs '
        '-Q > %proyeksi2%' + '\n')
    if plot_topo == 'YES':
        file.write('project -C%startlon1%/%startlat1% -E%endlon1%/%endlat1% -G.5 -Q > %track%' + '\n')
        file.write('grdtrack %track% -G%indo% | gawk "{print $3, $4/1000 }" > %trackAB%' + '\n')
        file.write('project -C%startlon2%/%startlat2% -E%endlon2%/%endlat2% -G.5 -Q > %track%' + '\n')
        file.write('grdtrack %track% -G%indo% | gawk "{print $3, $4/1000 }" > %trackCD%' + '\n')
    if plot_animasi == 'YES':
        file.write(':prepare' + '\n')
        file.write('if exist frame\\ (' + '\n')
        # file.write('echo deleting temporary frame'+'\n')
        file.write('rd /S /Q frame' + '\n')
        file.write(')' + '\n')
        file.write('mkdir frame' + '\n')
        file.write('set /a framenumber = -1' + '\n')
        file.write(':loopplot' + '\n')
        file.write('set /a framenumber = %framenumber% + 1' + '\n')
        file.write('set /a starttime= %starttime% + %tpf%' + '\n')
        file.write('if %starttime% GTR %stoptime% goto finishplot' + '\n')
        file.write('goto plot' + '\n')
    file.write(':plot' + '\n')
    file.write('REM Peta Dasar' + '\n')
    file.write(
        'pscoast -JM8c -R%R% -Dh -B1::WSne -G245/245/200 -S150/255/255 -W0.2p,black -Lg%x2%/%y2%+c-1+w%z2%k+l+ab+jBC '
        '-Tdg%x1%/%y1%+w1.2+f1+jLT --MAP_ANNOT_MIN_SPACING=0.1p --FONT_TITLE=10 --FONT_LABEL=9 '
        '--FONT_ANNOT_PRIMARY=8 -K -Y8 > %ps%' + '\n')
    file.write('psxy %fault% -JM -R -W0.4 -O -K >> %ps%' + '\n')
    file.write('psxy %subduction% -JM -R -W0.4 -Sf0.8i/0.08i+r+t -Gblack -O -K >> %ps%' + '\n')
    file.write('REM Data' + '\n')
    file.write('gawk -F" " "{print $2, $3}" %station% | psxy -J -R%R% -St0.3c -W0.2,black -Gblue -O -K >> %ps%' + '\n')
    file.write('gawk -F" " "{print  $2, $3, $1}" %station% | pstext -J -R -F+f8p,Helvetica+jLT -O -K >> %ps%' + '\n')
    mag_col = '$9'
    if M_scale == 'linear':
        M_size = mag_col + '*' + str(M_linear_size)
    elif M_scale == 'quadrat':
        M_size = str('(' + mag_col + '*' + str(M_linear_size) + ')^2')
    else:
        print()
        print('Periksa tipe ukuran simbol magnitudo (linear or quadrat)')
        print()
    if plot_animasi == 'YES':
        i = 0
        strstep = ''
        while i < transp_max:
            if i == 0:
                file.write(
                    'gawk "{if ($10>%starttime%-%tpf% && $10<=%starttime%) print $6,$7,$8,' + M_size + '}" %tmpdata% | '
                    'psxy -R -JM -Sc -C%D% -W0.2 -O -K >> %ps%' + '\n')
            else:
                strstep = strstep + '-%tpf%'
                file.write(
                    'gawk "{if ($10>%starttime%-%tpf%' + strstep + ' && $10<=%starttime%' + strstep + ') '
                    'print $6,$7,$8,' + M_size + '}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.2 -O -t' +
                    str(i) + ' -K >> %ps%' + '\n')
            i += transp_step
        file.write('gawk "{if ($10<%starttime%) print $6,$7,$8,' + M_size + '}" %tmpdata% | psxy -R -JM -Sc -C%D% '
                   '-W0.25 -O -t' + str(transp_max) + ' -K >> %ps%' + '\n')
    else:
        file.write(
            'gawk "{print $6,$7,$8,' + M_size + '}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.2 -O -K >> %ps%' + '\n')
    file.write('gawk "{print ' + lon + ',' + lat + ',' + depth + ',$4,$5,$6,$7,$8,$9,$10,0,0,$13}" %focal% | psmeca '
               '-R -J -Sm' + str(epic_size) + '/-1 -Z%D% -T0 -C -O -K >> %ps%' + '\n')
    file.write('REM Cross Section Line AB (NP1)' + '\n')
    file.write('psxy %lineAB% -J -R -W0.3 -O -K >> %ps%' + '\n')
    file.write('pstext %text_A% -J -R -F+f8p,Helvetica+jCM -N -O -K >> %ps%' + '\n')
    file.write('pstext %text_B% -J -R -F+f8p,Helvetica+jCM -N -O -K >> %ps%' + '\n')
    file.write('REM Cross Section Line CD (NP2)' + '\n')
    file.write('psxy %lineCD% -J -R -W0.3 -O -K >> %ps%' + '\n')
    file.write('pstext %text_C% -J -R -F+f8p,Helvetica+jCM -N -O -K >> %ps%' + '\n')
    file.write('pstext %text_D% -J -R -F+f8p,Helvetica+jCM -N -O -K >> %ps%' + '\n')
    if plot_animasi == 'YES':
        file.write('gawk "BEGIN {print strftime(\\"%%d-%%m-%%Y %%H:%%M:%%S ' + tzname + '\\",%starttime%);}" | '
                   'gawk "{print ' + str(timepos_x) + ',' + str(timepos_y) + ',$0}" | '
                   'pstext -R -JM -F+f6,Helvetica+jRT -O -K >> %ps%' + '\n')
    # file.write('echo '+str(creditpos_x)+' '+str(creditpos_y)+' @@eqhalauwet |
    # pstext -R -JM -F+f8,ZapfChancery-MediumItalic+jRB -O -K >> %ps%'+'\n')
    file.write('REM Inset' + '\n')
    file.write('pscoast -R%R_inset% -JM2 -Dh -W0.2p,black -Gwhite -S150/255/255 -B5::wsNE --MAP_FRAME_TYPE=plain '
               '--FONT_ANNOT_PRIMARY=5 -O -K >> %ps%' + '\n')
    file.write('REM psxy %subduction% -JM -R%R_inset% -W0.29 -Sf0.2c/0.03c+r+t -Gblack -O -K >> %ps%' + '\n')
    file.write('REM psxy %fault% -JM -R%R_inset% -W0.29 -O -K >> %ps%' + '\n')
    file.write('echo %llon% %blat% > ../tmp/box' + '\n')
    file.write('echo %llon% %ulat% >> ../tmp/box' + '\n')
    file.write('echo %rlon% %ulat% >> ../tmp/box' + '\n')
    file.write('echo %rlon% %blat% >> ../tmp/box' + '\n')
    file.write('echo %llon% %blat% >> ../tmp/box' + '\n')
    file.write('psxy -R%R_inset% -JM ../tmp/box -W0.5,red -O -K >> %ps%' + '\n')
    file.write('REM Parameter Peta' + '\n')
    file.write('psbasemap -R0/1/0/1 -JX8/8 -Bx -X8.5 -Y1 -O -K >> %ps%' + '\n')
    file.write('echo ^> 0.5 0.9 0.6 8 c > ../tmp/judul' + '\n')
    file.write('echo %title% >> ../tmp/judul' + '\n')
    file.write('pstext ../tmp/judul -R -J -F+f11p,AvantGarde-DemiOblique+jCM -M -O -K >> %ps%' + '\n')
    file.write('echo 0.5 0.7 %typemag% %mainmag% | pstext -J -R -F+f10p,Helvetica+jCM -O -K>> %ps%' + '\n')
    file.write('gawk "{print 0.5,0.55,$3,$4,$5,$6,$7,$8,$9,$10,0,0,$13}" %focal% | psmeca -R -J -Sm0.7/-1 -C -Z%D% '
               '-T0 -N -O -K >> %ps%' + '\n')
    file.write('echo 0.5 0.4 Fault plane1:  strike=%strike1%  dip=%dip1%  slip=%slip1% | pstext -J -R '
               '-F+f8p,Helvetica+jCM -O -K >> %ps%' + '\n')
    file.write('echo 0.5 0.3 Fault plane2:  strike=%strike2%  dip=%dip2%  slip=%slip2% | pstext -J -R '
               '-F+f8p,Helvetica+jCM -O -K >> %ps%' + '\n')
    # Plot Legenda
    jx_legend = 5  # lebar legenda
    R, J = set_legend(jx_legend, num_M, min_M, legenda, M_scale, float(M_linear_size))
    file.write('psbasemap -R' + R + ' -JX' + J + ' -Bx --FONT_ANNOT_PRIMARY=6 -O -K -X' + str((8 - jx_legend) / 2) +
               ' -Y-1.4 >> %ps%' + '\n')
    file.write('psscale -Dg' + str(jx_legend / 2) + '/' + str(jx_legend / 3) + '+w' + str(jx_legend * 0.7) + '/' +
               str(jx_legend / 16) + '+e+macl+h+jCB -J -R -Bx100+l"Kedalaman (km)" -G0/500 -I1 '
               '--MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=6 --FONT_LABEL=6 -C%D% -N -O -K >> %ps%' + '\n')
    file.write('psxy %L% -R -J -Sc -W0.35 -O -K >> %ps%' + '\n')
    file.write('gawk "{print $1,$4,$5}" %L% | pstext -J -R -F+f6p,Helvetica,black+jCB -O -K >> %ps%' + '\n')
    # file.write('pslegend %L% -J -Dx0.25/0.1+w7.5/0.85i+jLB+l1.7 -O -K >> %ps%'+'\n')
    file.write('REM box crossection' + '\n')
    file.write('set boxwidht=8' + '\n')
    file.write('set boxheight=3.5' + '\n')
    file.write('set boxelev=1' + '\n')
    file.write('REM boxelev = boxheight / 5' + '\n')
    file.write('set boxoverlap=3' + '\n')
    file.write('REM boxoverlap = boxheight - (1/2 * boxelev)' + '\n')
    mag_col = '$4'
    if M_scale == 'linear':
        M_size = mag_col + '*' + str(M_linear_size)
    elif M_scale == 'quadrat':
        M_size = str('(' + mag_col + '*' + str(M_linear_size) + ')^2')
    else:
        print()
        print('Periksa tipe ukuran simbol magnitudo (linear or quadrat)')
        print()
    if plot_topo == 'YES':
        file.write(':CROSS_AB' + '\n')
        file.write(
            'psxy %trackAB% -R%R4% -JX%boxwidht%/%boxelev% -BWe -Bya%maxelev%f1+l"Elev (km)" --FONT_ANNOT_PRIMARY=8 '
            '--FONT_LABEL=9 -W3p -X-' + str(
                8.5 + (8 - jx_legend) / 2) + ' -Y-2 -O -K >> %ps%' + '\n')
        file.write('echo 0 %maxelev% A | pstext -J -R -F+f10p,Helvetica+jRB -N -O -K >> %ps%' + '\n')
        file.write('echo %length% %maxelev% B | pstext -J -R -F+f10p,Helvetica+jLB -N -O -K >> %ps%' + '\n')
        file.write('echo 0 0 > %sealevel%' + '\n')
        file.write('echo %length% 0 >> %sealevel%' + '\n')
        file.write('psxy %sealevel% -J -R -W1,89/89/171 -O -K >> %ps%' + '\n')
        file.write(
            'psbasemap -JX%boxwidht%/%boxheight% -R%R2% -Bxa20+l"Distance (km)" -Bya20f20+l"Depth (km)" '
            '-BWSne+t"Cross Section Fault Plane 1" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 '
            '--FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y-%boxoverlap% >> %ps%' + '\n')
        if plot_animasi == 'YES':
            i = 0
            strstep = ''
            while i < transp_max:
                if i == 0:
                    file.write(
                        'gawk "{if ($5>%starttime%-%tpf% && $5<=%starttime%) print $7, $3*(-1.0), $3, ' + M_size + '}" '
                        '%proyeksi1% | psxy -R -J -Sc -C%D% -W0.2 -O -K >> %ps%' + '\n')
                else:
                    strstep = strstep + '-%tpf%'
                    file.write(
                        'gawk "{if ($5>%starttime%-%tpf%' + strstep + ' && $5<=%starttime%' + strstep + ') '
                        'print $7, $3*(-1.0), $3, ' + M_size + '}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.2 -O -t' +
                        str(i) + ' -K >> %ps%' + '\n')
                i += transp_step
            file.write(
                'gawk "{if ($5<%starttime%) print $7, $3*(-1.0), $3, ' + M_size + '}" %proyeksi1% | '
                'psxy -R -J -Sc -C%D% -W0.2 -O -t' + str(transp_max) + ' -K >> %ps%' + '\n')
        else:
            file.write(
                'gawk "{print $7, $3*(-1.0), $3, ' + M_size + '}" %proyeksi1% | psxy -R -J -Sc -C%D% '
                '-W0.2 -O -K >> %ps%' + '\n')
        file.write('psxy %dip_AB% -J -R -Wthin,black -O -K >> %ps%' + '\n')
        file.write(
            'gawk "{print ' + lon + ',' + lat + ',-' + depth + ',$4,$5,$6,$7,$8,$9,$10,0,0,$13}" %focal% | '
            'pscoupe -J -R%R3% -Sm' + str(epic_size) + '/0/0 -T '
            '-Aa%startlon1%/%startlat1%/%endlon1%/%endlat1%/90/%width%/0/600 -Z%D% -E255 -N -O -K >> %ps%' + '\n')
        file.write(':CROSS_CD' + '\n')
        file.write(
            'psxy %trackCD% -R%R4% -JX%boxwidht%/%boxelev% -Bew -Bya%maxelev%f1 --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 '
            '-W3p -X8.5 -Y%boxoverlap% -O -K >> %ps%' + '\n')
        file.write('echo 0 %maxelev% C | pstext -J -R -F+f10p,Helvetica+jRB -N -O -K >> %ps%' + '\n')
        file.write('echo %length% %maxelev% D | pstext -J -R -F+f10p,Helvetica+jLB -N -O -K >> %ps%' + '\n')
        file.write('echo 0 0 > %sealevel%' + '\n')
        file.write('echo %length% 0 >> %sealevel%' + '\n')
        file.write('psxy %sealevel% -J -R -W1,89/89/171 -O -K >> %ps%' + '\n')
        file.write(
            'psbasemap -JX%boxwidht%/%boxheight% -R%R2% -Bxa20+l"Distance (km)" -BeSnw+t"Cross Section Fault Plane 2" '
            '--MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K '
            '-Y-%boxoverlap%>> %ps%' + '\n')
        if plot_animasi == 'YES':
            i = 0
            strstep = ''
            while i < transp_max:
                if i == 0:
                    file.write(
                        'gawk "{if ($5>%starttime%-%tpf% && $5<=%starttime%) print $7, $3*(-1.0), $3, ' + M_size + '}"'
                        ' %proyeksi2% | psxy -R -J -Sc -C%D% -W0.2 -O -K >> %ps%' + '\n')
                else:
                    strstep = strstep + '-%tpf%'
                    file.write(
                        'gawk "{if ($5>%starttime%-%tpf%' + strstep + ' && $5<=%starttime%' + strstep + ') print '
                        '$7, $3*(-1.0), $3, ' + M_size + '}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.2 -O -t' + str(
                            i) + ' -K >> %ps%' + '\n')
                i += transp_step
            file.write(
                'gawk "{if ($5<%starttime%) print $7, $3*(-1.0), $3, ' + M_size + '}" %proyeksi2% | psxy -R -J -Sc '
                '-C%D% -W0.2 -O -t' + str(
                    transp_max) + ' -K >> %ps%' + '\n')
        else:
            file.write(
                'gawk "{print $7, $3*(-1.0), $3, ' + M_size + '}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.2 -O -K >> '
                '%ps%' + '\n')
        file.write('psxy %dip_CD% -J -R -Wthin,black -O -K >> %ps%' + '\n')
        file.write(
            'gawk "{print ' + lon + ',' + lat + ',-' + depth + ',$4,$5,$6,$7,$8,$9,$10,0,0,$13}" %focal% | pscoupe -J '
            '-R%R3% -Sm' + str(epic_size) + '/0/0 -T -Aa%startlon2%/%startlat2%/%endlon2%/%endlat2%/90/%width%/0/600 '
            '-Z%D% -E255 -N -O -K >> %ps%' + '\n')
    else:
        file.write(':CROSS_AB' + '\n')
        file.write(
            'psbasemap -JX%boxwidht%/%boxheight% -R%R2% -BWSne+t"Cross Section Fault Plane 1" -Bxa20+l"Distance (km)" '
            '-Bya20f20+l"Depth (km)" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 '
            '--FONT_TITLE=10 -O -K -X-' + str(8.5 + (8 - jx_legend) / 2) + ' -Y-5 >> %ps%' + '\n')
        file.write('echo %AC% 1 A | pstext -J -R -F+f10p,Helvetica+jRB -N -O -K >> %ps%' + '\n')
        file.write('echo %BD% 1 B | pstext -J -R -F+f10p,Helvetica+jLB -N -O -K >> %ps%' + '\n')
        if plot_animasi == 'YES':
            i = 0
            strstep = ''
            while i < transp_max:
                if i == 0:
                    file.write(
                        'gawk "{if ($5>%starttime%-%tpf% && $5<=%starttime%) print $7, $3*(-1.0), $3, ' + M_size + '}" '
                        '%proyeksi1% | psxy -R -J -Sc -C%D% -W0.2 -O -K >> %ps%' + '\n')
                else:
                    strstep = strstep + '-%tpf%'
                    file.write(
                        'gawk "{if ($5>%starttime%-%tpf%' + strstep + ' && $5<=%starttime%' + strstep + ') '
                        'print $7, $3*(-1.0), $3, ' + M_size + '}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.2 -O -t' +
                        str(i) + ' -K >> %ps%' + '\n')
                i += transp_step
            file.write(
                'gawk "{if ($5<%starttime%) print $7, $3*(-1.0), $3, ' + M_size + '}" %proyeksi1% | psxy -R -J -Sc '
                '-C%D% -W0.2 -O -t' + str(transp_max) + ' -K >> %ps%' + '\n')
        else:
            file.write(
                'gawk "{print $7, $3*(-1.0), $3, ' + M_size + '}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.2 -O -K'
                ' >> %ps%' + '\n')
        file.write('psxy %dip_AB% -J -R -Wthin,black -O -K >> %ps%' + '\n')
        file.write(
            'gawk "{print ' + lon + ',' + lat + ',-' + depth + ',$4,$5,$6,$7,$8,$9,$10,$11,$12,$13}" %focal% | '
            'pscoupe -J -R%R3% -Sm' + str(epic_size) + '/0/0 -T '
            '-Aa%startlon1%/%startlat1%/%endlon1%/%endlat1%/90/%width%/0/600 -Z%D% -E255 -N -O -K >> %ps%' + '\n')
        file.write(':CROSS_CD' + '\n')
        file.write(
            'psbasemap -JX%boxwidht%/%boxheight% -R%R2% -BeSnw+t"Cross Section Fault Plane 2" -Bxa20+l"Distance (km)" '
            '--MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -X8.5 '
            '>> %ps%' + '\n')
        file.write('echo %AC% 0 C | pstext -J -R -F+f10p,Helvetica+jRB -N -O -K >> %ps%' + '\n')
        file.write('echo %BD% 0 D | pstext -J -R -F+f10p,Helvetica+jLB -N -O -K >> %ps%' + '\n')
        if plot_animasi == 'YES':
            i = 0
            strstep = ''
            while i < transp_max:
                if i == 0:
                    file.write(
                        'gawk "{if ($5>%starttime%-%tpf% && $5<=%starttime%) print $7, $3*(-1.0), $3, ' + M_size + '}" '
                        '%proyeksi2% | psxy -R -J -Sc -C%D% -W0.2 -O -K >> %ps%' + '\n')
                else:
                    strstep = strstep + '-%tpf%'
                    file.write(
                        'gawk "{if ($5>%starttime%-%tpf%' + strstep + ' && $5<=%starttime%' + strstep + ') '
                        'print $7, $3*(-1.0), $3, ' + M_size + '}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.2 -O -t' +
                        str(i) + ' -K >> %ps%' + '\n')
                i += transp_step
            file.write(
                'gawk "{if ($5<%starttime%) print $7, $3*(-1.0), $3, ' + M_size + '}" %proyeksi2% | psxy -R -J -Sc '
                '-C%D% -W0.2 -O -t' + str(transp_max) + ' -K >> %ps%' + '\n')
        else:
            file.write(
                'gawk "{print $7, $3*(-1.0), $3, ' + M_size + '}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.2 -O -K '
                '>> %ps%' + '\n')
        file.write('psxy %dip_CD% -J -R -Wthin,black -O -K >> %ps%' + '\n')
        file.write(
            'gawk "{print ' + lon + ',' + lat + ',-' + depth + ',$4,$5,$6,$7,$8,$9,$10,$11,$12,$13}" %focal% | '
            'pscoupe -J -R%R3% -Sm' + str(epic_size) + '/0/0 -T '
            '-Aa%startlon2%/%startlat2%/%endlon2%/%endlat2%/90/%width%/0/600 -Z%D% -E255 -N -O -K >> %ps%' + '\n')
    if lblperiode == 'Periode kurang':
        tinggi_graph = (13.5 - 1.7) / 2
        graf_yoffset = tinggi_graph + 1.6
        file.write('psbasemap -JX6/' + str(
            tinggi_graph) + ' -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 '
                            '--FONT_TITLE=10 -O -K -X8.5 >> %ps%' + '\n')
        if plot_animasi == 'YES':
            file.write('gawk "{if ($10<=%starttime%) print $9}" %tmpdata% | pshistogram -JX6/' + str(tinggi_graph) +
                       ' -W0.5+b -Gblue -L -BESwn -Bx+lMagnitude -By+l"Jumlah Gempabumi" '
                       '--MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 '
                       '--FONT_TITLE=10 -O -K >> %ps%' + '\n')
        else:
            file.write('gawk "{print $9}" %tmpdata% | pshistogram -JX6/' + str(tinggi_graph) +
                       ' -W0.5+b -Gblue -L -BESwn -Bx+lMagnitude -By+l"Jumlah Gempabumi" '
                       '--MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 '
                       '--FONT_TITLE=10 -O -K >> %ps%' + '\n')
        file.write('psbasemap -JX6/' + str(tinggi_graph) + ' -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p '
                   '--FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y' + str(graf_yoffset) +
                   ' >> %ps%' + '\n')
        if plot_animasi == 'YES':
            file.write('gawk "{if ($10<=%starttime%) print $6}" %tmpdata% | pshistogram -JX6/' + str(tinggi_graph) +
                       ' -W20+b -Gblue -Z4 -L -BESwn -Bx+l"Kedalaman (km)" -By+l"Log(Jumlah Gempabumi)" '
                       '--MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 '
                       '-O -K >> %ps%' + '\n')
        else:
            file.write('gawk "{print $8}" %tmpdata% | pshistogram -JX6/' + str(tinggi_graph) +
                       ' -W20+b -Gblue -Z4 -L -BESwn -Bx+l"Kedalaman (km)" -By+l"Log(Jumlah Gempabumi)" '
                       '--MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K '
                       '>> %ps%' + '\n')
        file.write(
            'echo 0.9 -0.15 "by: @@eqhalauwet" | pstext -R -Bg1x -J -F+f9,ZapfChancery-MediumItalic+jLT -Y-' + str(
                graf_yoffset) + ' -N -O >> %ps%' + '\n')
    else:
        graf_yoffset = 4.95
        file.write(
            'psbasemap -JX5/%boxheight% -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 '
            '--FONT_LABEL=9 --FONT_TITLE=10 -O -K -X8.5 >> %ps%' + '\n')
        if plot_animasi == 'YES':
            file.write(
                'gawk "{if ($10<=%starttime%) print $9}" %tmpdata% | pshistogram -JX5/%boxheight% -W0.5+b -Gblue -L '
                '-BESwn -Bx+lMagnitude -By+l"Jumlah Gempabumi" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 '
                '--FONT_LABEL=9 --FONT_TITLE=10 -O -K >> %ps%' + '\n')
        else:
            file.write(
                'gawk "{print $9}" %tmpdata% | pshistogram -JX5/%boxheight% -W0.5+b -Gblue -L -BESwn -Bx+lMagnitude '
                '-By+l"Jumlah Gempabumi" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 '
                '--FONT_TITLE=10 -O -K >> %ps%' + '\n')
        file.write(
            'psbasemap -JX5/%boxheight% -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 '
            '--FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y' + str(
                graf_yoffset) + ' >> %ps%' + '\n')
        if plot_animasi == 'YES':
            file.write(
                'gawk "{if ($10<=%starttime%) print $8}" %tmpdata% | pshistogram -JX5/%boxheight% -W20+b -Gblue -Z4 '
                '-L -BESwn -Bx+l"Kedalaman (km)" -By+l"Log(Jumlah Gempabumi)" --MAP_ANNOT_MIN_SPACING=0.1p '
                '--FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K  >> %ps%' + '\n')
        else:
            file.write(
                'gawk "{print $8}" %tmpdata% | pshistogram -JX5/%boxheight% -W20+b -Gblue -Z4 -L -BESwn '
                '-Bx+l"Kedalaman (km)" -By+l"Log(Jumlah Gempabumi)" --MAP_ANNOT_MIN_SPACING=0.1p '
                '--FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> %ps%' + '\n')
        file.write(
            'psbasemap -JX5/%boxheight% -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 '
            '--FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y' + str(
                graf_yoffset) + ' >> %ps%' + '\n')
        ####
        if plot_animasi == 'YES':
            file.write(
                'gawk "{if ($10<=%starttime%) print ' + tab_data + '$4}" %tmpdata% | '
                'pshistogram -JX5/%boxheight% -W1+b -Gblue -L -BESwn -Bx+l"' + lblperiode + '" -By+l"Jumlah Gempabumi" '
                '-F --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K  >> '
                                                                                            '%ps%' + '\n')
        else:
            file.write(
                'gawk "{print ' + tab_data + '}" %tmpdata% | pshistogram -JX5/%boxheight% -W1+b -Gblue -L '
                '-BESwn -Bx+l"' + lblperiode + '" -By+l"Jumlah Gempabumi" -F --MAP_ANNOT_MIN_SPACING=0.1p '
                '--FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> %ps%' + '\n')
        file.write(
            'echo 0.9 -0.24 "by: @@eqhalauwet" | pstext -R -Bg1x -J -F+f9,ZapfChancery-MediumItalic+jLT -Y-' + str(
                graf_yoffset * 2) + ' -N -O >> %ps%' + '\n')
    if plot_animasi == 'YES':
        file.write('psconvert %ps% -Tg -E' + str(dpi) + ' -P -A0.2 -Fframe/frame-%framenumber%' + '\n')
        file.write('goto loopplot' + '\n')
        file.write(':finishplot' + '\n')
        file.write(
            'ffmpeg -framerate %fps% -i frame/frame-%%d.png -c:v libx264 -profile:v high -crf 18 -pix_fmt yuv420p -vf '
            '"scale=1080:ceil(ih/(iw/1080*2))*2" %output%' + '\n')
        file.write('REM gm convert -delay %delay% -loop %replay% frame/frame-*.png %output%' + '\n')
    else:
        file.write('psconvert %ps% -Tj -E' + str(dpi) + ' -P -A0.2 -F../output/plot.jpg' + '\n')
    file.write('del gmt.history psconvert* Aa* %ps%' + '\n')
    if plot_animasi == 'YES':
        file.write('rd /S /Q frame' + '\n')
    file.close()
else:
    file = open(fileoutput, 'w')
    file.write('@echo off' + '\n')
    file.write('REM echo EQ Map Generator' + '\n')
    file.write('REM echo by eQ H' + '\n')
    file.write('REM echo.--------------------------------------------------------' + '\n')
    file.write('set ps=animasi.ps' + '\n')
    file.write('set title=' + title + '\n')
    file.write('set fromdate=' + fromdate + '\n')
    file.write('set todate=' + todate + '\n')
    file.write('set datasource=' + datasource + '\n')
    file.write('set x1=' + str(timepos_x) + '\n')
    file.write('set y1=' + str(timepos_y) + '\n')
    file.write('set x2=' + str(skala_x) + '\n')
    file.write('set y2=' + str(skala_y) + '\n')
    file.write('set z2=' + str(skala_z) + '\n')
    file.write('set llon=' + str(ll) + '\n')
    file.write('set rlon=' + str(rl) + '\n')
    file.write('set blat=' + str(bl) + '\n')
    file.write('set ulat=' + str(ul) + '\n')
    file.write('set R=%llon%/%rlon%/%blat%/%ulat%' + '\n')
    file.write('set R_inset=' + str(ll_inset) + '/' + str(rl_inset) + '/' + str(bl_inset) + '/' + str(ul_inset) + '\n')
    file.write('set R2=0/4/0/3' + '\n')
    file.write('set D=../inc/depth.cpt' + '\n')
    file.write('set L=../tmp/legenda' + '\n')
    file.write('set tmpdata=../tmp/tmpdata.dat' + '\n')
    file.write('set tmpdirasakan=../tmp/tmpdirasakan.dat' + '\n')
    file.write('set output=../output/animasi.mp4' + '\n')
    file.write('set station=../data/station.sel' + '\n')
    file.write('set fault=../inc/fault_moluccas.gmt' + '\n')
    file.write('set subduction=../inc/subduksi_moluccas.gmt' + '\n')
    # file.write('set trench_a=../inc/trench-a.gmt'+'\n')
    # file.write('set trench_b=../inc/trench-b.gmt'+'\n')
    # file.write('set thrust=../inc/thrust.gmt'+'\n')
    # file.write('set transform=../inc/transform.gmt'+'\n')
    file.write('set starttime=' + str(start_time) + '\n')
    file.write('set stoptime=' + str(stop_time) + '\n')
    if plot_animasi == 'YES':
        file.write('REM time sampling per frame (second)' + '\n')
        file.write('set tpf=' + str(time_sampling) + '\n')
        file.write('REM frame per second (ffmpeg)' + '\n')
        file.write('set fps=' + str(fps) + '\n')
        file.write('REM time delay every frame (gm)' + '\n')
        file.write('set delay=' + str(time_delay) + '\n')
        file.write('set replay=0' + '\n')
    file.write(':depthcpt' + '\n')
    file.write('if exist %D% (' + '\n')
    # file.write('echo depthcpt OK'+'\n')
    file.write('goto :prepare' + '\n')
    file.write(') else (' + '\n')
    file.write('echo generate %D%' + '\n')
    file.write('run cptdepth_std.bat' + '\n')
    file.write(')' + '\n')
    file.write(':prepare' + '\n')
    if plot_animasi == 'YES':
        lebar = tinggi_map / 0.724
        if lebar >= 21:
            lebar = str(21)
        elif lebar <= 19.41:
            lebar = str(19.412)
        else:
            lebar = str(20.2)
        file.write('if exist frame\\ (' + '\n')
        # file.write('echo deleting temporary frame'+'\n')
        file.write('rd /S /Q frame' + '\n')
        file.write(')' + '\n')
        file.write('mkdir frame' + '\n')
        file.write('set /a framenumber = -1' + '\n')
        file.write('set /a introframe= %framenumber% +' + str(3 * fps) + '\n')
        file.write(':loopintro' + '\n')
        file.write('set /a framenumber = %framenumber% + 1' + '\n')
        file.write('if %framenumber% GTR %introframe% (' + '\n')
        file.write('set /a framenumber = %framenumber% - 1' + '\n')
        file.write('goto loopplot' + '\n')
        file.write(')' + '\n')
        file.write('psimage ../inc/intro.jpg -Dx0/0+w29.622c/' + lebar + 'c -X0 -Y0 -K > %ps%' + '\n')
        file.write('psbasemap -JX29.7/' + lebar + ' -R%R2% -Bx --FONT_ANNOT_PRIMARY=5 -O -K >> %ps%' + '\n')
        file.write('echo ^> 2 1.55 1 28 c > ../tmp/judul' + '\n')
        file.write('echo %title% >> ../tmp/judul' + '\n')
        file.write('pstext ../tmp/judul -R -J -F+f24p,NewCenturySchlbk-Italic,white+jCM -M -O -K >> %ps%' + '\n')
        # file.write('echo 2 1.55 %title% |
        # pstext -R -J -F+f24p,NewCenturySchlbk-Italic,white+jCM -N -O -K >> %ps%'+'\n')
        file.write(
            'echo 2 1.15 %fromdate% | pstext -R -J -F+f18,NewCenturySchlbk-Italic,white+jCB -N -O -K >> %ps%' + '\n')
        file.write('echo 2 0.95 hingga | pstext -R -J -F+f18,NewCenturySchlbk-Italic,white+jCB -N -O -K >> %ps%' + '\n')
        file.write(
            'echo 2 0.75 %todate% | pstext -R -J -F+f18,NewCenturySchlbk-Italic,white+jCB -N -O -K >> %ps%' + '\n')
        file.write(
            'echo 3.9 0.1 Sumber Data: %datasource% | pstext -R -J -F+f11p,NewCenturySchlbk-Italic,white+jRB '
            '-N -O >> %ps%' + '\n')
        file.write('psconvert %ps% -Tg -E' + str(dpi) + ' -P -A0.2 -Fframe/frame-%framenumber%' + '\n')
        file.write('goto loopintro' + '\n')
        file.write(':loopplot' + '\n')
        file.write('set /a framenumber = %framenumber% + 1' + '\n')
        file.write('set /a starttime= %starttime% + %tpf%' + '\n')
        file.write('if %starttime% GTR %stoptime% (' + '\n')
        file.write('set /a framenumber = %framenumber% - 1' + '\n')
        file.write('set /a stopframe= %framenumber% +' + str(4 * fps) + '\n')
        file.write('goto loopoutro' + '\n')
        file.write(')' + '\n')
    file.write('goto plot' + '\n')
    file.write(':plot' + '\n')
    file.write('REM MEMBUAT PETA SEISMISITAS' + '\n')
    file.write('pscoast -R%R% -JM' + str(
        jm) + ' -Dh -B2::WSne -G245/245/200 -S150/255/255 -W0.2p,black -Lg%x2%/%y2%+c-1+w%z2%k+l+ab+jTC '
              '-Tdg%x2%/%y2%+w1.2+f1+jBC --MAP_ANNOT_MIN_SPACING=0.1p --FONT_TITLE=10 --FONT_ANNOT_PRIMARY=8 '
              '--FONT_LABEL=9 -K > %ps%' + '\n')
    file.write('psxy %subduction% -JM -R -W0.51 -Sf0.8i/0.08i+r+t -Gblack -O -K >> %ps%' + '\n')
    file.write('psxy %fault% -JM -R -W0.51 -O -K >> %ps%' + '\n')
    file.write('REM Data' + '\n')
    file.write('gawk -F" " "{print $2, $3}" %station% | psxy -J -R%R% -St0.3c -W0.25,black -Gblue -O -K >> %ps%' + '\n')
    file.write('gawk -F" " "{print  $2, $3, $1}" %station% | pstext -J -R -F+f8p,Helvetica+jLT -O -K >> %ps%' + '\n')
    mag_col = '$9'
    if M_scale == 'linear':
        M_size = mag_col + '*' + str(M_linear_size)
    elif M_scale == 'quadrat':
        M_size = str('(' + mag_col + '*' + str(M_linear_size) + ')^2')
    else:
        print()
        print('Periksa tipe ukuran simbol magnitudo (linear or quadrat)')
        print()
    if plot_animasi == 'YES':
        i = 0
        strstep = ''
        while i < transp_max:
            if i == 0:
                file.write(
                    'gawk "{if ($10>%starttime%-%tpf% && $10<=%starttime%) print $6,$7,$8,' + M_size + '}" %tmpdata% | '
                    'psxy -R -JM -Sc -C%D% -W0.25 -O -K >> %ps%' + '\n')
                if plot_dirasakan == 'YES':
                    file.write(
                        'gawk "{if ($10>%starttime%-%tpf% && $10<=%starttime%) print $6,$7,$8,' + M_size + '}" '
                        '%tmpdirasakan% | psxy -R -JM -Sa -C%D% -W0.5,white -O -K >> %ps%' + '\n')
            else:
                strstep = strstep + '-%tpf%'
                file.write(
                    'gawk "{if ($10>%starttime%-%tpf%' + strstep + ' && $10<=%starttime%' + strstep + ') '
                    'print $6,$7,$8,' + M_size + '}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.25 -O -t' + str(
                        i) + ' -K >> %ps%' + '\n')
                if plot_dirasakan == 'YES':
                    file.write(
                        'gawk "{if ($10>%starttime%-%tpf%' + strstep + ' && $10<=%starttime%' + strstep + ') '
                        'print $6,$7,$8,' + M_size + '}" %tmpdirasakan% | psxy -R -JM -Sa -C%D% -W0.5,white -O -t' +
                        str(i) + ' -K >> %ps%' + '\n')
            i += transp_step
        file.write(
            'gawk "{if ($10<%starttime%) print $6,$7,$8,' + M_size + '}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.25 -O '
            '-t' + str(transp_max) + ' -K >> %ps%' + '\n')
        if plot_dirasakan == 'YES':
            file.write(
                'gawk "{if ($10<%starttime%) print $6,$7,$8,' + M_size + '}" %tmpdirasakan% | psxy -R -JM -Sa '
                '-C%D% -W0.5,white -O -t' + str(transp_max) + ' -K >> %ps%' + '\n')
        file.write(
            'gawk "BEGIN {print strftime(\\"%%d-%%m-%%Y %%H:%%M:%%S ' + tzname + '\\",%starttime%);}" | '
            'gawk "{print ' + str(timepos_x) + ',' + str(timepos_y) + ',$0}" | pstext -R -JM -F+f8,Helvetica+jRT '
            '-O -K >> %ps%' + '\n')
    else:
        file.write(
            'gawk "{print $6,$7,$8,' + M_size + '}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.25 -O -K >> %ps%' + '\n')
        if plot_dirasakan == 'YES':
            file.write(
                'gawk "{print $6,$7,$8,' + M_size + '}" %tmpdirasakan% | '
                'psxy -R -JM -Sa -C%D% -W0.5,white -O -K >> %ps%' + '\n')
    # file.write('echo '+str(creditpos_x)+' '+str(creditpos_y)+' @@eqhalauwet |
    # pstext -R -JM -F+f9,ZapfChancery-MediumItalic+jRB -O -K >> %ps%'+'\n')
    file.write(
        'psimage ../inc/logo.png -R -J -Dg' + str(kompas_x) + '/' + str(kompas_y) + '+w2.3c+jLT -K -O >> %ps%' + '\n')
    file.write(
        'pscoast -R%R_inset% -JM4 -Dh -W0.2p,black -Gwhite -S150/255/255 -B5::wsNE --MAP_FRAME_TYPE=plain '
        '--FONT_ANNOT_PRIMARY=6 -O -K >> %ps%' + '\n')
    # Plot Legenda
    jx_legend = 4  # lebar legenda
    R, J = set_legend(jx_legend, num_M, min_M, legenda, M_scale, float(M_linear_size))
    file.write('psbasemap -R' + R + ' -JX' + J + ' -Bx --FONT_ANNOT_PRIMARY=6 -O -K -X' + str(
        jm - jx_legend) + ' >> %ps%' + '\n')
    file.write('psscale -Dg' + str(jx_legend / 2) + '/' + str(jx_legend / 3) + '+w' + str(jx_legend * 0.8) + '/' + str(
        jx_legend / 16) + '+e+macl+h+jCB -J -R -Bx100+l"Kedalaman (km)" -G0/500 -I1 --MAP_ANNOT_MIN_SPACING=0.1p '
                          '--FONT_ANNOT_PRIMARY=6 --FONT_LABEL=6 -C%D% -O -K >> %ps%' + '\n')
    file.write('psxy %L% -R -J -Sc -W0.35 -O -K >> %ps%' + '\n')
    file.write('gawk "{print $1,$4,$5}" %L% | pstext -J -R -F+f6p,Helvetica,black+jCB -O -K >> %ps%' + '\n')
    file.write('REM psxy %subduction% -JM -R%R_inset% -W0.39 -Sf0.2c/0.03c+r+t -Gblack -O -K >> %ps%' + '\n')
    file.write('REM psxy %fault% -JM -R%R_inset% -W0.39 -O -K >> %ps%' + '\n')
    file.write('echo %llon% %blat% > ../tmp/box' + '\n')
    file.write('echo %llon% %ulat% >> ../tmp/box' + '\n')
    file.write('echo %rlon% %ulat% >> ../tmp/box' + '\n')
    file.write('echo %rlon% %blat% >> ../tmp/box' + '\n')
    file.write('echo %llon% %blat% >> ../tmp/box' + '\n')
    file.write('psxy -R%R_inset% -JM ../tmp/box -W0.6,red -O -K -X-' + str(jm - jx_legend) + '>> %ps%' + '\n')
    if lblperiode == 'Periode kurang':
        tinggi_graph = (tinggi_map - 1.7) / 2
        graf_yoffset = tinggi_graph + 1.6
        file.write('psbasemap -JX6/' + str(
            tinggi_graph) + ' -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 '
                            '--FONT_TITLE=10 -O -K -X' + str(jm + 0.5) + ' >> %ps%' + '\n')
        if plot_animasi == 'YES':
            file.write('gawk "{if ($10<=%starttime%) print $9}" %tmpdata% | pshistogram -JX6/' + str(
                tinggi_graph) + ' -W0.5+b -Gblue -L -BESwn -Bx+lMagnitude -By+l"Jumlah Gempabumi" '
                '--MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> '
                                '%ps%' + '\n')
        else:
            file.write('gawk "{print $9}" %tmpdata% | pshistogram -JX6/' + str(
                tinggi_graph) + ' -W0.5+b -Gblue -L -BESwn -Bx+lMagnitude -By+l"Jumlah Gempabumi" '
                '--MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> '
                                '%ps%' + '\n')
        file.write('psbasemap -JX6/' + str(
            tinggi_graph) + ' -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 '
                            '--FONT_TITLE=10 -O -K -Y' + str(graf_yoffset) + ' >> %ps%' + '\n')
        if plot_animasi == 'YES':
            file.write('gawk "{if ($10<=%starttime%) print $8}" %tmpdata% | pshistogram -JX6/' + str(
                tinggi_graph) + ' -W20+b -Gblue -L -BESwn -Bx+l"Kedalaman (km)" -By+l"Log(Jumlah Gempabumi)" '
                '-Z4 --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> '
                                '%ps%' + '\n')
        else:
            file.write('gawk "{print $8}" %tmpdata% | pshistogram -JX6/' + str(tinggi_graph) + ' -W20+b -Gblue -L '
                       '-BESwn -Bx+l"Kedalaman (km)" -By+l"Log(Jumlah Gempabumi)" -Z4 --MAP_ANNOT_MIN_SPACING=0.1p '
                       '--FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> %ps%' + '\n')
        file.write('echo 0.9 -0.15 "by: @@eqhalauwet" | pstext -R -Bg1x -J -F+f9,ZapfChancery-MediumItalic+jLT -Y-' +
                   str(graf_yoffset) + ' -N -O >> %ps%' + '\n')
    else:
        tinggi_graph = (tinggi_map - 2.9) / 3
        graf_yoffset = tinggi_graph + 1.45
        file.write('psbasemap -JX5/' + str(
            tinggi_graph) + ' -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 '
                            '--FONT_TITLE=10 -O -K -X' + str(
            jm + 0.5) + ' >> %ps%' + '\n')
        if plot_animasi == 'YES':
            file.write('gawk "{if ($10<=%starttime%) print $9}" %tmpdata% | pshistogram -JX5/' + str(tinggi_graph) +
                       ' -W0.5+b -Gblue -L -BESwn -Bx+lMagnitude -By+l"Jumlah Gempabumi" --MAP_ANNOT_MIN_SPACING=0.1p '
                       '--FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> %ps%' + '\n')
        else:
            file.write('gawk "{print $9}" %tmpdata% | pshistogram -JX5/' + str(tinggi_graph) +
                       ' -W0.5+b -Gblue -L -BESwn -Bx+lMagnitude -By+l"Jumlah Gempabumi" --MAP_ANNOT_MIN_SPACING=0.1p '
                       '--FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> %ps%' + '\n')
        file.write('psbasemap -JX5/' + str(tinggi_graph) + ' -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p '
                   '--FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y' +
                   str(graf_yoffset) + ' >> %ps%' + '\n')
        if plot_animasi == 'YES':
            file.write('gawk "{if ($10<=%starttime%) print $8}" %tmpdata% | pshistogram -JX5/' + str(tinggi_graph) +
                       ' -W20+b -Gblue -L -Z4 -BESwn -Bx+l"Kedalaman (km)" -By+l"Log(Jumlah Gempabumi)" '
                       '--MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K  >>'
                       ' %ps%' + '\n')
        else:
            file.write('gawk "{print $8}" %tmpdata% | pshistogram -JX5/' + str(tinggi_graph) + ' -W20+b -Gblue -L -Z4 '
                       '-BESwn -Bx+l"Kedalaman (km)" -By+l"Log(Jumlah Gempabumi)" --MAP_ANNOT_MIN_SPACING=0.1p '
                       '--FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> %ps%' + '\n')
        file.write('psbasemap -JX5/' + str(tinggi_graph) + ' -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p '
                   '--FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y' + str(graf_yoffset) +
                   ' >> %ps%' + '\n')
        if plot_animasi == 'YES':
            ####
            file.write('gawk "{if ($10<=%starttime%) print ' + tab_data + '}" %tmpdata% | pshistogram -JX5/' +
                       str(tinggi_graph) + ' -W1+b -Gblue -L -BESwn -Bx+l"' + lblperiode + '" -By+l"Jumlah Gempabumi" '
                       '-F --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K  '
                       '>> %ps%' + '\n')
        else:
            ####
            file.write('gawk "{print ' + tab_data + '}" %tmpdata% | pshistogram -JX5/' + str(tinggi_graph) + ' '
                       '-W1+b -Gblue -L -BESwn -Bx+l"' + lblperiode + '" -By+l"Jumlah Gempabumi" -F '
                       '--MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 '
                       '--FONT_TITLE=10 -O -K >> %ps%' + '\n')
        file.write('echo 0.9 -0.24 "by: @@eqhalauwet" | pstext -R -Bg1x -J -F+f9,ZapfChancery-MediumItalic+jLT -Y-' +
                   str(graf_yoffset * 2) + ' -N -O >> %ps%' + '\n')
    if plot_animasi == 'YES':
        file.write('psconvert %ps% -Tg -E' + str(dpi) + ' -P -A0.2 -Fframe/frame-%framenumber%' + '\n')
        file.write('goto loopplot' + '\n')
        file.write(':loopoutro' + '\n')
        file.write('set /a framenumber = %framenumber% + 1' + '\n')
        file.write('if %framenumber% GTR %stopframe% goto renderplot' + '\n')
        file.write('pscoast -R%R% -JM' + str(jm) + ' -Dh -B2::WSne -G245/245/200 -S150/255/255 -W0.2p,black '
                   '-Lg%x2%/%y2%+c-1+w%z2%k+l+ab+jTC -Tdg%x2%/%y2%+w1.2+f1+jBC --MAP_ANNOT_MIN_SPACING=0.1p '
                   '--FONT_TITLE=10 --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 -K > %ps%' + '\n')
        file.write('psxy %subduction% -JM -R -W0.51 -Sf0.8i/0.08i+r+t -Gblack -O -K >> %ps%' + '\n')
        file.write('psxy %fault% -JM -R -W0.51 -O -K >> %ps%' + '\n')
        file.write('REM Data' + '\n')
        file.write(
            'gawk -F" " "{print $2, $3}" %station% | psxy -J -R%R% -St0.3c -W0.25,black -Gblue -O -K >> %ps%' + '\n')
        file.write(
            'gawk -F" " "{print  $2, $3, $1}" %station% | pstext -J -R -F+f8p,Helvetica+jLT -O -K >> %ps%' + '\n')
        file.write(
            'gawk "{print $6,$7,$8,' + M_size + '}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.25 -O -K >> %ps%' + '\n')
        if plot_dirasakan == 'YES':
            file.write('gawk "{print $6,$7,$8,' + M_size + '}" %tmpdirasakan% | psxy -R -JM -Sa -C%D% -W0.5,white '
                       '-O -K >> %ps%' + '\n')
        # file.write('echo '+str(creditpos_x)+' '+str(creditpos_y)+' @@eqhalauwet | pstext -R -JM -F+f9,ZapfChancery
        # -MediumItalic+jRB -O -K >> %ps%'+'\n')
        file.write('psimage ../inc/logo.png -R -J -Dg' + str(kompas_x) + '/' + str(
            kompas_y) + '+w2.3c+jLT -K -O >> %ps%' + '\n')
        # file.write('psbasemap -JX29.7/21 -R%R2% -Bx --FONT_ANNOT_PRIMARY=5 -O -K >> %ps%'+'\n')
        file.write('echo ^> ' + str(skala_x) + ' ' + str(logo_y1) + ' 0.4 ' + str(jm - 1) + ' c > ../tmp/judul' + '\n')
        file.write('echo %title% >> ../tmp/judul' + '\n')
        file.write('pstext ../tmp/judul -R -J -F+f12p,NewCenturySchlbk-BoldItalic,black+jCB -Gwhite -M -t20 -O -K '
                   '>> %ps%' + '\n')
        # file.write('echo '+str(skala_x)+' '+str(logo_y1)+' %title% | pstext -R -J
        # -F+f12p,NewCenturySchlbk-BoldItalic,black+jCB -G245/245/200 -N -O -K >> %ps%'+'\n')
        file.write('echo ' + str(skala_x) + ' ' + str(logo_y2) + ' %fromdate% hingga %todate% | pstext -R -J '
                   '-F+f10,NewCenturySchlbk-BoldItalic,black+jCB -Gwhite -N -t20 -O -K >> %ps%' + '\n')
        # if plot_dirasakan=='NO':
        # file.write('echo '+str(skala_x)+' '+str(logo_y3)+' Jumlah gempabumi '+jumlah_event+' kejadian | pstext -R -J
        # -F+f9,NewCenturySchlbk-BoldItalic,black+jCM -Gwhite -N -t20 -O -K >> %ps%'+'\n')
        # else:
        if jumlah_dirasakan == 0:
            file.write('echo ' + str(skala_x) + ' ' + str(logo_y3) + ' Jumlah gempabumi ' + jumlah_event +
                       ' kejadian, tidak ada laporan dirasakan oleh masyarakat | pstext -R -J '
                       '-F+f9,NewCenturySchlbk-BoldItalic,black+jCM -Gwhite -N -t20 -O -K >> %ps%' + '\n')
        else:
            file.write('echo ' + str(skala_x) + ' ' + str(logo_y3) + ' Jumlah gempabumi ' + jumlah_event +
                       ' kejadian, ' + jumlah_dirasakan + ' dilaporkan dirasakan oleh masyarakat | pstext -R -J '
                       '-F+f9,NewCenturySchlbk-BoldItalic,black+jCM -Gwhite -N -t20 -O -K >> %ps%' + '\n')
        file.write(
            'pscoast -R%R_inset% -JM4 -Dh -W0.2p,black -Gwhite -S150/255/255 -B5::wsNE --MAP_FRAME_TYPE=plain '
            '--FONT_ANNOT_PRIMARY=6 -O -K >> %ps%' + '\n')
        # Plot Legenda
        R, J = set_legend(jx_legend, num_M, min_M, legenda, M_scale, float(M_linear_size))
        file.write('psbasemap -R' + R + ' -JX' + J + ' -Bx --FONT_ANNOT_PRIMARY=6 -O -K -X' + str(
            jm - jx_legend) + ' >> %ps%' + '\n')
        file.write('psscale -Dg' + str(jx_legend / 2) + '/' + str(jx_legend / 3) + '+w' + str(jx_legend * 0.8) + '/' +
                   str(jx_legend / 16) + '+e+macl+h+jCB -J -R -Bx100+l"Kedalaman (km)" -G0/500 -I1 '
                   '--MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=6 --FONT_LABEL=6 -C%D% -O -K >> %ps%' + '\n')
        file.write('psxy %L% -R -J -Sc -W0.35 -O -K >> %ps%' + '\n')
        file.write('gawk "{print $1,$4,$5}" %L% | pstext -J -R -F+f6p,Helvetica,black+jCB -O -K >> %ps%' + '\n')
        file.write('REM psxy %subduction% -JM -R%R_inset% -W0.39 -Sf0.2c/0.03c+r+t -Gblack -O -K >> %ps%' + '\n')
        file.write('REM psxy %fault% -JM -R%R_inset% -W0.39 -O -K >> %ps%' + '\n')
        file.write('echo %llon% %blat% > ../tmp/box' + '\n')
        file.write('echo %llon% %ulat% >> ../tmp/box' + '\n')
        file.write('echo %rlon% %ulat% >> ../tmp/box' + '\n')
        file.write('echo %rlon% %blat% >> ../tmp/box' + '\n')
        file.write('echo %llon% %blat% >> ../tmp/box' + '\n')
        file.write('psxy -R%R_inset% -JM ../tmp/box -W0.6,red -O -K -X-' + str(jm - jx_legend) + '>> %ps%' + '\n')
        if lblperiode == 'Periode kurang':
            tinggi_graph = (tinggi_map - 1.7) / 2
            graf_yoffset = tinggi_graph + 1.6
            file.write('psbasemap -JX6/' + str(tinggi_graph) + ' -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p '
                       '--FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -X' + str(jm + 0.5) +
                       ' >> %ps%' + '\n')
            if plot_animasi == 'YES':
                file.write('gawk "{if ($10<=%starttime%) print $9}" %tmpdata% | pshistogram -JX6/' + str(tinggi_graph) +
                           ' -W0.5+b -Gblue -L -BESwn -Bx+lMagnitude -By+l"Jumlah Gempabumi" '
                           '--MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 '
                           '-O -K >> %ps%' + '\n')
            else:
                file.write('gawk "{print $9}" %tmpdata% | pshistogram -JX6/' + str(tinggi_graph) + ' -W0.5+b -Gblue -L '
                           '-BESwn -Bx+lMagnitude -By+l"Jumlah Gempabumi" --MAP_ANNOT_MIN_SPACING=0.1p '
                           '--FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> %ps%' + '\n')
            file.write('psbasemap -JX6/' + str(tinggi_graph) + ' -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p '
                       '--FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y' + str(graf_yoffset) +
                       ' >> %ps%' + '\n')
            if plot_animasi == 'YES':
                file.write('gawk "{if ($10<=%starttime%) print $8}" %tmpdata% | pshistogram -JX6/' + str(tinggi_graph) +
                           ' -W20+b -Gblue -L -BESwn -Bx+l"Kedalaman (km)" -By+l"Log(Jumlah Gempabumi)" -Z4 '
                           '--MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 '
                           '-O -K >> %ps%' + '\n')
            else:
                file.write('gawk "{print $8}" %tmpdata% | pshistogram -JX6/' + str(tinggi_graph) + ' -W20+b -Gblue -L '
                           '-BESwn -Bx+l"Kedalaman (km)" -By+l"Log(Jumlah Gempabumi)" -Z4 --MAP_ANNOT_MIN_SPACING=0.1p '
                           '--FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> %ps%' + '\n')
            file.write('echo 0.9 -0.15 "by: @@eqhalauwet" | pstext -R -Bg1x -J -F+f9,ZapfChancery-MediumItalic+jLT '
                       '-Y-' + str(graf_yoffset) + ' -N -O >> %ps%' + '\n')
        else:
            tinggi_graph = (tinggi_map - 2.9) / 3
            graf_yoffset = tinggi_graph + 1.45
            file.write('psbasemap -JX5/' + str(
                tinggi_graph) + ' -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 '
                                '--FONT_TITLE=10 -O -K -X' + str(
                jm + 0.5) + ' >> %ps%' + '\n')
            if plot_animasi == 'YES':
                file.write('gawk "{if ($10<=%starttime%) print $9}" %tmpdata% | pshistogram -JX5/' + str(tinggi_graph) +
                           ' -W0.5+b -Gblue -L -BESwn -Bx+lMagnitude -By+l"Jumlah Gempabumi" '
                           '--MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K '
                           '>> %ps%' + '\n')
            else:
                file.write('gawk "{print $9}" %tmpdata% | pshistogram -JX5/' + str(tinggi_graph) + ' -W0.5+b -Gblue -L '
                           '-BESwn -Bx+lMagnitude -By+l"Jumlah Gempabumi" --MAP_ANNOT_MIN_SPACING=0.1p '
                           '--FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> %ps%' + '\n')
            file.write('psbasemap -JX5/' + str(tinggi_graph) + ' -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p '
                       '--FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y' + str(graf_yoffset) +
                       ' >> %ps%' + '\n')
            if plot_animasi == 'YES':
                file.write('gawk "{if ($10<=%starttime%) print $8}" %tmpdata% | pshistogram -JX5/' + str(tinggi_graph) +
                           ' -W20+b -Gblue -L -Z4 -BESwn -Bx+l"Kedalaman (km)" -By+l"Log(Jumlah Gempabumi)" '
                           '--MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K  '
                           '>> %ps%' + '\n')
            else:
                file.write('gawk "{print $8}" %tmpdata% | pshistogram -JX5/' + str(tinggi_graph) + ' -W20+b -Gblue -L '
                           '-Z4 -BESwn -Bx+l"Kedalaman (km)" -By+l"Log(Jumlah Gempabumi)" --MAP_ANNOT_MIN_SPACING=0.1p '
                           '--FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> %ps%' + '\n')
            file.write('psbasemap -JX5/' + str(tinggi_graph) + ' -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p '
                       '--FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y' + str(graf_yoffset) +
                       ' >> %ps%' + '\n')
            if plot_animasi == 'YES':
                ####
                file.write('gawk "{if ($10<=%starttime%) print ' + tab_data + '}" %tmpdata% | pshistogram -JX5/' +
                           str(tinggi_graph) + ' -W1+b -Gblue -L -BESwn -Bx+l"' + lblperiode + '" '
                           '-By+l"Jumlah Gempabumi" -F --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 '
                           '--FONT_LABEL=9 --FONT_TITLE=10 -O -K  >> %ps%' + '\n')
            else:
                ####
                file.write('gawk "{print ' + tab_data + '}" %tmpdata% | pshistogram -JX5/' + str(tinggi_graph) +
                           ' -W1+b -Gblue -L -BESwn -Bx+l"' + lblperiode + '" -By+l"Jumlah Gempabumi" -F '
                           '--MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 '
                           '-O -K >> %ps%' + '\n')
            file.write('echo 0.9 -0.24 "by: @@eqhalauwet" | pstext -R -Bg1x -J -F+f9,ZapfChancery-MediumItalic+jLT -Y-'
                       + str(graf_yoffset * 2) + ' -N -O >> %ps%' + '\n')
        file.write('psconvert %ps% -Tg -E' + str(dpi) + ' -P -A0.2 -Fframe/frame-%framenumber%' + '\n')
        file.write('goto loopoutro' + '\n')
        file.write(':renderplot' + '\n')
        file.write('ffmpeg -framerate %fps% -i frame/frame-%%d.png -c:v libx264 -profile:v high -crf 18 -pix_fmt '
                   'yuv420p -vf "scale=1080:ceil(ih/(iw/1080*2))*2" %output%' + '\n')
        file.write('REM gm convert -delay %delay% -loop %replay% frame/frame-*.png %output%' + '\n')
    else:
        file.write('psconvert %ps% -Tj -E' + str(dpi) + ' -P -A0.2 -F../output/plot.jpg' + '\n')
    file.write('del gmt.history psconvert* Aa* %ps%' + '\n')
    if plot_animasi == 'YES':
        file.write('REM rd /S /Q frame' + '\n')
    file.close()

print("__________________________")
print("")
print("Writting code . . .")
time.sleep(1)
print("")
if plot_animasi == 'YES':
    print("Generating video . . . ")
else:
    print("Generating map . . . ")
print("")
p = Popen(["plot.bat"], shell=True, cwd=r'bin')
stdout, stderr = p.communicate()
time.sleep(3)
print("__________________________")
if plot_animasi == 'YES':
    print('Animation Generated on "output/animasi.mp4"')
else:
    print('Map Generated on "output/plot.jpg"')
print("")
time.sleep(0.5)
print("Closing application . . . ")
time.sleep(2)
