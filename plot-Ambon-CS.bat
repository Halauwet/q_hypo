@echo off
REM echo EQ Map Generator
REM echo by eQ H
REM echo.--------------------------------------------------------
REM Parameter Gempa
set title=Animasi Aktifitas Gempabumi Ambon-Kairatu
set title2=Menggunakan Jaringan Seismograf Lokal (ITB, BNPB, BMKG)
set mainlat=-3.5490
set mainlon=128.3800
set maindepth=10.00
set mainmag=7.2
set typemag=Mw
set maxelev=2
set maxdepth=40
set x1=127.44666666666666
set y1=-2.649
set x2=128.38
set y2=-4.449
set z2=50
REM Set Parameter Peta
set ps=animasi.ps
set D=../inc/depth-shallow.cpt
set L=../tmp/legenda
set epic=%mainlon%/%mainlat%
set tmpdata=../tmp/tmpdata.dat
set tmpdirasakan=../tmp/tmpdirasakan.dat
set station=../data/station.sel
set focal=../data/psmeca.dat
set output=../output/animasi.mp4
set indo=../inc/indonesia.nc
set topo=../inc/my_etopo.cpt
set fault=../inc/fault_moluccas.gmt
set subduction=../inc/subduksi_moluccas.gmt
REM Plot Area
set llon=127.38
set rlon=129.38
set blat=-4.5489999999999995
set ulat=-2.549
set R=%llon%/%rlon%/%blat%/%ulat%
set R_inset=124.78/131.98/-6.5489999999999995/-0.5490000000000004
REM set R1=%AC%/%BD%/-%maxdepth%/0
REM set R2=0/%length%/-%maxelev%/%maxelev%
REM set R3=0/%length%/-%maxdepth%/0

REM set starttime=1571337552
REM set tpf=72480
REM set stoptime=1576412133

set starttime=1571194475
set stoptime=1576098579
REM time sampling per frame (second)
set tpf=9808
REM frame per second (ffmpeg)
set fps=10
REM time delay every frame (gm)
set delay=10
set replay=0
REM Proyeksi
set proyeksi1=../tmp/projection1.tmp
set proyeksi2=../tmp/projection2.tmp
set proyeksi3=../tmp/projection3.tmp
set lineAB=../tmp/LINE_AB
set lineCD=../tmp/LINE_CD
set lineEF=../tmp/LINE_EF
set dip_AB=../tmp/DIP_AB
set dip_CD=../tmp/DIP_CD
set dip_EF=../tmp/DIP_EF
set text_A=../tmp/TEXT_A
set text_B=../tmp/TEXT_B
set text_C=../tmp/TEXT_C
set text_D=../tmp/TEXT_D
set text_E=../tmp/TEXT_E
set text_F=../tmp/TEXT_F
set track=../tmp/track
set trackAB=../tmp/trackAB
set trackCD=../tmp/trackCD
set trackEF=../tmp/trackEF
set sealevel=../tmp/sealevel.line

REM Cross Section
set startlon1=128.38
set startlat1=-3.8582276605298607
set endlon1=128.38
set endlat1=-3.139772339470139
set length1=80
set width1=40
set R1AB=0/%length1%/-%maxdepth%/0
set R2AB=0/%length1%/-%maxelev%/%maxelev%

set startlon2=127.941474
set startlat2=-3.795530
set endlon2=128.570326
set endlat2=-3.332903
set length2=87
set width2=43.5
set R1CD=0/%length2%/-%maxdepth%/0
set R2CD=0/%length2%/-%maxelev%/%maxelev%

set startlon3=128.042573
set startlat3=-3.837432
set endlon3=128.625003
set endlat3=-3.419693
set length3=80
set width3=40
set R1EF=0/%length3%/-%maxdepth%/0
set R2EF=0/%length3%/-%maxelev%/%maxelev%

echo %startlon1% %startlat1% > %lineAB%
echo %endlon1% %endlat1% >> %lineAB%
echo %startlon1% %startlat1% A > %text_A%
echo %endlon1% %endlat1% B > %text_B%
echo %startlon2% %startlat2% > %lineCD%
echo %endlon2% %endlat2% >> %lineCD%
echo %startlon2% %startlat2% C > %text_C%
echo %endlon2% %endlat2% D > %text_D%
echo %startlon3% %startlat3% > %lineEF%
echo %endlon3% %endlat3% >> %lineEF%
echo %startlon3% %startlat3% E > %text_E%
echo %endlon3% %endlat3% F > %text_F%

:TOPOCPT
if exist %topo% (
goto :DEPTHCPT
) else (
echo generate %topo%
makecpt -Z -Cetopo1 > %topo%
REM makecpt -Cred,yellow,green -T0,60,300,700 -Z0/500  > %topo%
)
:DEPTHCPT
if exist %D% (
goto :PROJECT
) else (
echo generate %D%
run cptdepth_std.bat
)
:PROJECT
REM gawk "{print $6, $7, $8, $9, $10}" %tmpdata% | project  -L-5/5 -C%epic% -A%azm1% -Fxyzpqrs -Q > %proyeksi1%
REM gawk "{print $6, $7, $8, $9, $10}" %tmpdata% | project  -L-5/5 -C%epic% -A%azm2% -Fxyzpqrs -Q > %proyeksi2%

gawk "{print $6, $7, $8, $9, $10}" %tmpdata% | project  -W-5/5 -C%startlon1%/%startlat1% -E%endlon1%/%endlat1% -Fxyzpqrs -Q > %proyeksi1%
gawk "{print $6, $7, $8, $9, $10}" %tmpdata% | project  -W-5/5 -C%startlon2%/%startlat2% -E%endlon2%/%endlat2% -Fxyzpqrs -Q > %proyeksi2%
gawk "{print $6, $7, $8, $9, $10}" %tmpdata% | project  -W-5/5 -C%startlon3%/%startlat3% -E%endlon3%/%endlat3% -Fxyzpqrs -Q > %proyeksi3%


project -C%startlon1%/%startlat1% -E%endlon1%/%endlat1% -G.5 -Q > %track%
grdtrack %track% -G%indo% | gawk "{print $3, $4/1000 }" > %trackAB%
project -C%startlon2%/%startlat2% -E%endlon2%/%endlat2% -G.5 -Q > %track%
grdtrack %track% -G%indo% | gawk "{print $3, $4/1000 }" > %trackCD%
project -C%startlon3%/%startlat3% -E%endlon3%/%endlat3% -G.5 -Q > %track%
grdtrack %track% -G%indo% | gawk "{print $3, $4/1000 }" > %trackEF%
:prepare
if exist frame\ (
rd /S /Q frame
)
mkdir frame
set /a framenumber = -1
:loopplot
set /a framenumber = %framenumber% + 1
set /a starttime= %starttime% + %tpf%
if %starttime% GTR %stoptime% goto finishplot
goto plot
:plot
REM Peta Dasar
pscoast -JM8c -R%R% -Dh -B1::WSne -G245/245/200 -S150/255/255 -W0.2p,black -Lg%x2%/%y2%+c-1+w%z2%k+l+ab+jBC -Tdg%x1%/%y1%+w1.2+f1+jLT --MAP_ANNOT_MIN_SPACING=0.1p --FONT_TITLE=10 --FONT_LABEL=9 --FONT_ANNOT_PRIMARY=8 --MAP_FRAME_TYPE=plain -K -Y8 > %ps%
psxy %fault% -JM -R -W0.4 -O -K >> %ps%
psxy %subduction% -JM -R -W0.4 -Sf0.8i/0.08i+r+t -Gblack -O -K >> %ps%
REM Data
gawk -F" " "{print $2, $3}" %station% | psxy -J -R%R% -St0.3c -W0.2,black -Gblue -O -K >> %ps%
gawk -F" " "{print  $2, $3, $1}" %station% | pstext -J -R -F+f8p,Helvetica+jLT -O -K >> %ps%
gawk "{if ($10>%starttime%-%tpf% && $10<=%starttime%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf% && $10<=%starttime%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t2.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t4.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t6.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t8.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t10.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t12.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t14.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t16.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t18.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t20.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t22.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t24.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t26.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t28.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t30.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t32.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t34.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t36.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t38.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t40.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t42.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t44.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t46.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t48.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t50.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t52.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t54.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t56.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t58.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t60.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t62.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t64.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t66.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.15 -O -t68.0 -K >> %ps%
gawk "{if ($10<%starttime%) print $6,$7,$8,$9*0.0300}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.155 -O -t70 -K >> %ps%
REM gawk "{print 128.3800,-3.5490,10.00,$4,$5,$6,$7,$8,$9,$10,0,0,$13}" %focal% | psmeca -R -J -Sm0.216/-1 -Z%D% -T0 -C -O -K >> %ps%
REM Cross Section Line AB
psxy %lineAB% -J -R -W0.6,blue -O -K >> %ps%
pstext %text_A% -J -R -F+f8p,Helvetica+jCM -N -O -K >> %ps%
pstext %text_B% -J -R -F+f8p,Helvetica+jCM -N -O -K >> %ps%
REM Cross Section Line CD
psxy %lineCD% -J -R -W0.6,blue -O -K >> %ps%
pstext %text_C% -J -R -F+f8p,Helvetica+jCM -N -O -K >> %ps%
pstext %text_D% -J -R -F+f8p,Helvetica+jCM -N -O -K >> %ps%

REM Cross Section Line EF
psxy %lineEF% -J -R -W0.6,blue -O -K >> %ps%
pstext %text_E% -J -R -F+f8p,Helvetica+jCM -N -O -K >> %ps%
pstext %text_F% -J -R -F+f8p,Helvetica+jCM -N -O -K >> %ps%
gawk "BEGIN {print strftime(\"%%d-%%m-%%Y %%H:%%M:%%S WIT\",%starttime%);}" | gawk "{print 129.31333333333333,-2.649,$0}" | pstext -R -JM -F+f7,Helvetica+jRT -O -K >> %ps%
REM Inset
pscoast -R%R_inset% -JM2 -Dh -W0.2p,black -Gwhite -S150/255/255 -B5::wsNE --MAP_FRAME_TYPE=plain --FONT_ANNOT_PRIMARY=5 -O -K >> %ps%
REM psxy %subduction% -JM -R%R_inset% -W0.29 -Sf0.2c/0.03c+r+t -Gblack -O -K >> %ps%
REM psxy %fault% -JM -R%R_inset% -W0.29 -O -K >> %ps%
echo %llon% %blat% > ../tmp/box
echo %llon% %ulat% >> ../tmp/box
echo %rlon% %ulat% >> ../tmp/box
echo %rlon% %blat% >> ../tmp/box
echo %llon% %blat% >> ../tmp/box
psxy -R%R_inset% -JM ../tmp/box -W0.5,red -O -K >> %ps%
REM Parameter Peta
psbasemap -R0/1/0/1 -JX8/8 -B+n -X10 -O -K >> %ps%
echo ^> 0.5 0.9 0.6 8 c > ../tmp/judul
echo %title% >> ../tmp/judul
pstext ../tmp/judul -R -J -F+f11p,AvantGarde-DemiOblique+jCM -M -O -K >> %ps%
echo ^> 0.5 0.79 0.6 8 c > ../tmp/judul
echo %title2% >> ../tmp/judul
pstext ../tmp/judul -R -J -F+f7p,AvantGarde-DemiOblique+jCM -M -O -K >> %ps%
REM echo 0.5 0.655 Data 18 Oktober s/d 15 Desember 2019 | pstext -J -R -F+f8p,Helvetica+jCM -O -K>> %ps%
REM echo 0.5 0.58 hingga | pstext -J -R -F+f8p,Helvetica+jCM -O -K>> %ps%
REM echo 0.5 0.515 15 Desember 2019 | pstext -J -R -F+f8p,Helvetica+jCM -O -K>> %ps%
REM echo 0.5 0.36 Data sementara untuk hiposenter dengan uncertainty @_\074@_ 5km | pstext -J -R -F+f8p,Helvetica-BoldOblique+jCM -O -K >> %ps%
REM REM echo 0.5 0.36 Data sementara untuk keseluruhan hiposenter | pstext -J -R -F+f8p,Helvetica-BoldOblique+jCM -O -K >> %ps%
REM echo 0.5 0.30 Jumlah gempa: 715 kejadian | pstext -J -R -F+f8p,Helvetica-BoldOblique+jCM -O -K >> %ps%
REM psimage ../logo/logo-maluku.png -Dx1.4/0.3+w0.7c+jCB -O -K >> %ps%
REM psimage ../logo/logo-itb.png -Dx2.7/0.4+w0.74c+jCB -O -K >> %ps%
REM psimage ../logo/logo-bnpb.png -Dx4/0.2+w0.7c+jCB -O -K >> %ps%
REM psimage ../logo/logo-bmkg.png -Dx5.3/0.3+w0.67c+jCB -O -K >> %ps%
REM psimage ../logo/logo-kodampattimura.png -Dx6.6/0.3+w0.7c+jCB -O -K >> %ps%


REM gawk "{print 0.5,0.55,$3,$4,$5,$6,$7,$8,$9,$10,0,0,$13}" %focal% | psmeca -R -J -Sm0.7/-1 -C -Z%D% -T0 -N -O -K >> %ps%
REM echo 0.5 0.4 Fault plane1:  strike=%strike1%  dip=%dip1%  slip=%slip1% | pstext -J -R -F+f8p,Helvetica+jCM -O -K >> %ps%
REM echo 0.5 0.3 Fault plane2:  strike=%strike2%  dip=%dip2%  slip=%slip2% | pstext -J -R -F+f8p,Helvetica+jCM -O -K >> %ps%


REM psbasemap -R0/5/0/2.5 -JX5/2.5 -Bx --FONT_ANNOT_PRIMARY=6 -O -K -X1.5 >> %ps%
REM psscale -Dg2.5/1.3+w3.5/0.2125+e+h+jCB -J -R -Bx10+l"Kedalaman (km)" -G0/50 -I1 --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=6 --FONT_LABEL=6 -Gred -N -O -K >> %ps%


REM psxy %L% -R -J -Sc0.1 -W0.35 -O -K >> %ps%
REM gawk "{print $1,$4,$5}" %L% | pstext -J -R -F+f6p,Helvetica,black+jCB -O -K >> %ps%
REM box crossection
set boxwidht=8
set boxheight=3.5
set boxelev=1
REM boxelev = boxheight / 5
set boxoverlap=3
REM boxoverlap = boxheight - (1/2 * boxelev)

:CROSS_EF
psxy %trackEF% -R%R2EF% -JX%boxwidht%/%boxelev% -BWe -Bya%maxelev%f1+l"Elev (km)" --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 -W3p -O -K -Y3 >> %ps%
echo 0 %maxelev% E | pstext -J -R -F+f10p,Helvetica+jRB -N -O -K >> %ps%
echo %length3% %maxelev% F | pstext -J -R -F+f10p,Helvetica+jLB -N -O -K >> %ps%
echo 0 0 > %sealevel%
echo %length3% 0 >> %sealevel%
psxy %sealevel% -J -R -W0.5,blue -O -K >> %ps%
psbasemap -JX%boxwidht%/%boxheight% -R%R1EF% -Bxa20 -Bya20f20+l"Depth (km)" -BWSe+t"Cross Section E-F (width+-5km)" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y-%boxoverlap% >> %ps%
gawk "{if ($5>%starttime%-%tpf% && $5<=%starttime%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf% && $5<=%starttime%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t2.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t4.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t6.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t8.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t10.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t12.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t14.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t16.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t18.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t20.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t22.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t24.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t26.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t28.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t30.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t32.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t34.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t36.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t38.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t40.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t42.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t44.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t46.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t48.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t50.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t52.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t54.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t56.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t58.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t60.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t62.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t64.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t66.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t68.0 -K >> %ps%
gawk "{if ($5<%starttime%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi3% | psxy -R -J -Sc -C%D% -W0.15 -O -t70 -K >> %ps%
REM psxy %dip_EF% -J -R -Wthin,black -O -K >> %ps%
REM gawk "{print 128.3800,-3.5490,-10.00,$4,$5,$6,$7,$8,$9,$10,0,0,$13}" %focal% | pscoupe -J -R%R3EF% -Sm0.216/0/0 -T -Aa%startlon1%/%startlat1%/%endlon1%/%endlat1%/90/%width%/0/600 -Z%D% -E255 -N -O -K >> %ps%

:CROSS_AB
psxy %trackAB% -R%R2AB% -JX%boxwidht%/%boxelev% -BWe -Bya%maxelev%f1+l"Elev (km)" --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 -W3p -X-10 -Y-2.6 -O -K >> %ps%
echo 0 %maxelev% A | pstext -J -R -F+f10p,Helvetica+jRB -N -O -K >> %ps%
echo %length1% %maxelev% B | pstext -J -R -F+f10p,Helvetica+jLB -N -O -K >> %ps%
echo 0 0 > %sealevel%
echo %length1% 0 >> %sealevel%
psxy %sealevel% -J -R -W0.5,blue -O -K >> %ps%
psbasemap -JX%boxwidht%/%boxheight% -R%R1AB% -Bxa20+l"Distance (km)" -Bya20f20+l"Depth (km)" -BWSe+t"Cross Section A-B (width+-5km)" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y-%boxoverlap% >> %ps%
gawk "{if ($5>%starttime%-%tpf% && $5<=%starttime%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf% && $5<=%starttime%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t2.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t4.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t6.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t8.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t10.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t12.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t14.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t16.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t18.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t20.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t22.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t24.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t26.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t28.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t30.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t32.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t34.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t36.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t38.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t40.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t42.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t44.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t46.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t48.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t50.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t52.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t54.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t56.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t58.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t60.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t62.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t64.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t66.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t68.0 -K >> %ps%
gawk "{if ($5<%starttime%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi1% | psxy -R -J -Sc -C%D% -W0.15 -O -t70 -K >> %ps%
REM psxy %dip_AB% -J -R -Wthin,black -O -K >> %ps%
REM gawk "{print 128.3800,-3.5490,-10.00,$4,$5,$6,$7,$8,$9,$10,0,0,$13}" %focal% | pscoupe -J -R%R3AB% -Sm0.216/0/0 -T -Aa%startlon1%/%startlat1%/%endlon1%/%endlat1%/90/%width%/0/600 -Z%D% -E255 -N -O -K >> %ps%
:CROSS_CD
psxy %trackCD% -R%R2CD% -JX%boxwidht%/%boxelev% -Bew -Bya%maxelev%f1 --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 -W3p -X10 -Y%boxoverlap% -O -K >> %ps%
echo 0 %maxelev% C | pstext -J -R -F+f10p,Helvetica+jRB -N -O -K >> %ps%
echo %length2% %maxelev% D | pstext -J -R -F+f10p,Helvetica+jLB -N -O -K >> %ps%
echo 0 0 > %sealevel%
echo %length2% 0 >> %sealevel%
psxy %sealevel% -J -R -W0.5,blue -O -K >> %ps%
psbasemap -JX%boxwidht%/%boxheight% -R%R1CD% -Bxa20+l"Distance (km)" -BeSw+t"Cross Section C-D (width+-5km)" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y-%boxoverlap%>> %ps%
gawk "{if ($5>%starttime%-%tpf% && $5<=%starttime%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf% && $5<=%starttime%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t2.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t4.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t6.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t8.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t10.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t12.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t14.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t16.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t18.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t20.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t22.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t24.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t26.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t28.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t30.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t32.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t34.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t36.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t38.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t40.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t42.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t44.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t46.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t48.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t50.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t52.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t54.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t56.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t58.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t60.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t62.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t64.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t66.0 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t68.0 -K >> %ps%
gawk "{if ($5<%starttime%) print $6, $3*(-1.0), $3, $4*0.0300}" %proyeksi2% | psxy -R -J -Sc -C%D% -W0.15 -O -t70 -K >> %ps%
REM psxy %dip_CD% -J -R -Wthin,black -O -K >> %ps%
REM gawk "{print 128.3800,-3.5490,-10.00,$4,$5,$6,$7,$8,$9,$10,0,0,$13}" %focal% | pscoupe -J -R%R3CD% -Sm0.216/0/0 -T -Aa%startlon2%/%startlat2%/%endlon2%/%endlat2%/90/%width%/0/600 -Z%D% -E255 -N -O -K >> %ps%
REM psbasemap -JX5/%boxheight% -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -X8.5 >> %ps%
REM gawk "{if ($10<=%starttime%) print $9}" %tmpdata% | pshistogram -JX5/%boxheight% -W0.5+b -Gblue -L -BESwn -Bx+lMagnitude -By+l"Jumlah Gempabumi" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> %ps%
REM psbasemap -JX5/%boxheight% -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y4.95 >> %ps%
REM gawk "{if ($10<=%starttime%) print $8}" %tmpdata% | pshistogram -JX5/%boxheight% -W20+b -Gblue -Z4 -L -BESwn -Bx+l"Kedalaman (km)" -By+l"Log(Jumlah Gempabumi)" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K  >> %ps%
REM psbasemap -JX5/%boxheight% -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y4.95 >> %ps%
REM gawk "{if ($10<=%starttime%) print $4$4}" %tmpdata% | pshistogram -JX5/%boxheight% -W1+b -Gblue -L -BESwn -Bx+l"Tanggal (UTC)" -By+l"Jumlah Gempabumi" -F --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K  >> %ps%
echo 0.9 -0.24 "by: @@eqhalauwet" | pstext -R -Bg1x -J -F+f9,ZapfChancery-MediumItalic+jLT -Y-9.9 -N -O >> %ps%
psconvert %ps% -Tg -E512 -P -A0.8 -Fframe/frame-%framenumber%
goto loopplot
:finishplot
ffmpeg -framerate %fps% -i frame/frame-%%d.png -c:v libx264 -profile:v high -crf 18 -pix_fmt yuv420p -vf scale=w=1080:h=900 %output%
REM ffmpeg -framerate %fps% -i frame/frame-%%d.png -c:v libx264 -profile:v high -crf 18 -pix_fmt yuv420p -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" %output%
REM ffmpeg -framerate %fps% -i frame/frame-%%d.png -c:v libx264 -profile:v high -crf 18 -pix_fmt yuv420p -vf scale=w=1080:h=-1 %output%
REM gm convert -delay %delay% -loop %replay% frame/frame-*.png %output%
del gmt.history psconvert* Aa* %ps%
REM rd /S /Q frame
