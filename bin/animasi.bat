@echo off
REM echo EQ Map Generator
REM echo by eQ H
REM echo.--------------------------------------------------------
REM Parameter Gempa
set title=South Halmahera EQ July 14, 2019
set mainlat=-0.6492
set mainlon=128.0039
set maindepth=17.67
set mainmag=7.2
set typemag=Mw
set strike1=124
set strike2=34
set dip1=85
set dip2=88
set slip1=2
set slip2=175
REM length=panjang cross section
set length=250
set width=125.0
set AC=-%width%
set BD=%width%
set maxelev=0
set maxdepth=50
set x1=126.13723333333333
set y1=1.1508
set x2=128.0039
set y2=-2.4492
set z2=100
set str1=214
set str2=304
set azm1=124
set azm2=214
set startlat1=-1.5798663365009449
set startlon1=127.37615762969156
set startlat2=-0.02145762969157261
set startlon2=127.07323366349904
set endlat1=0.281466336500945
set endlon1=128.6316423703084
set endlat2=-1.276942370308427
set endlon2=128.93456633650092
REM Set Parameter Peta
set ps=animasi.ps
set D=../inc/depth.cpt
set L=../inc/legend
set epic=%mainlon%/%mainlat%
set tmpdata=../tmp/tmpdata.dat
set station=../data/station.sel
set focal=../data/psmeca.dat
set output=../output/animasi.mp4
set indo=../inc/indonesia.nc
set topo=../inc/my_etopo.cpt
set fault=../inc/fault_moluccas.gmt
set subduction=../inc/subduksi_moluccas.gmt
REM Plot Area
set llon=126.00389999999999
set rlon=130.0039
set blat=-2.6492
set ulat=1.3508
set R=%llon%/%rlon%/%blat%/%ulat%
set R_inset=120.80389999999998/135.20389999999998/-6.6492/5.3508
set R2=%AC%/%BD%/-%maxdepth%/0
set R3=0/%length%/-%maxdepth%/0
set R4=0/%length%/-%maxelev%/%maxelev%
set starttime=1563046385
set stoptime=1563413288
REM time sampling per frame (second)
set tpf=1111
REM frame per second (ffmpeg)
set fps=10
REM time delay every frame (gm)
set delay=10
set replay=0
REM Proyeksi
set proyeksi1=../tmp/projection1.tmp
set proyeksi2=../tmp/projection2.tmp
set lineAB=../tmp/LINE_AB
set lineCD=../tmp/LINE_CD
set dip_AB=../tmp/DIP_AB
set dip_CD=../tmp/DIP_CD
set text_A=../tmp/TEXT_A
set text_B=../tmp/TEXT_B
set text_C=../tmp/TEXT_C
set text_D=../tmp/TEXT_D
set track=../tmp/track
set trackAB=../tmp/trackAB
set trackCD=../tmp/trackCD
set sealevel=../tmp/sealevel.line
:TOPOCPT
if exist %topo% (
echo topo OK
goto :DEPTHCPT
) else (
echo generate %topo%
makecpt -Z -Cetopo1 > %topo%
)
:DEPTHCPT
if exist %D% (
echo depthcpt OK
goto :LEGEND
) else (
echo generate %D%
run cptdepth.bat
)
:LEGEND
run legenda.bat
:PROJECT
gawk "{print $4, $5, $6, $7, $8}" %tmpdata% | project -C%epic% -A%azm1% -Fxyzpqrs -Q > %proyeksi1%
gawk "{print $4, $5, $6, $7, $8}" %tmpdata% | project -C%epic% -A%azm2% -Fxyzpqrs -Q > %proyeksi2%
:prepare
if exist frame\ (
echo deleting temporary frame
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
pscoast -JM8c -R%R% -Dh -B1::WSne -G245/245/200 -S150/255/255 -W0.25p,black -Lg%x2%/%y2%+c-1+w%z2%k+l+ab+jBC -Tdg%x1%/%y1%+w1.2+f1+jLT --MAP_ANNOT_MIN_SPACING=0.1p --FONT_TITLE=6 --FONT_ANNOT_PRIMARY=6 --FONT_LABEL=6 -K -Y8 > %ps%
psxy %fault% -JM -R -Wthin -O -K >> %ps%
psxy %subduction% -JM -R -Wthin -Sf0.8i/0.08i+l+t -Gblack -O -K >> %ps%
REM Data
gawk -F" " "{print $2, $3}" %station% | psxy -J -R%R% -St0.3c -Wthin,black -Gblue -O -K >> %ps%
gawk -F" " "{print  $2, $3, $1}" %station% | pstext -J -R -F+f8p,Helvetica+jLT -O -K >> %ps%
gawk "{if ($8>%starttime%-%tpf% && $8<=%starttime%) print $4,$5,$6,$7*0.044}" %tmpdata% | psxy -R -JM -Sc -C%D% -Wthin -O -K >> %ps%
gawk "{if ($8>%starttime%-%tpf%-%tpf% && $8<=%starttime%-%tpf%) print $4,$5,$6,$7*0.044}" %tmpdata% | psxy -R -JM -Sc -C%D% -Wthin -O -t5 -K >> %ps%
gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%) print $4,$5,$6,$7*0.044}" %tmpdata% | psxy -R -JM -Sc -C%D% -Wthin -O -t10 -K >> %ps%
gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.044}" %tmpdata% | psxy -R -JM -Sc -C%D% -Wthin -O -t15 -K >> %ps%
gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.044}" %tmpdata% | psxy -R -JM -Sc -C%D% -Wthin -O -t20 -K >> %ps%
gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.044}" %tmpdata% | psxy -R -JM -Sc -C%D% -Wthin -O -t25 -K >> %ps%
gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.044}" %tmpdata% | psxy -R -JM -Sc -C%D% -Wthin -O -t30 -K >> %ps%
gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.044}" %tmpdata% | psxy -R -JM -Sc -C%D% -Wthin -O -t35 -K >> %ps%
gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.044}" %tmpdata% | psxy -R -JM -Sc -C%D% -Wthin -O -t40 -K >> %ps%
gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.044}" %tmpdata% | psxy -R -JM -Sc -C%D% -Wthin -O -t45 -K >> %ps%
gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.044}" %tmpdata% | psxy -R -JM -Sc -C%D% -Wthin -O -t50 -K >> %ps%
gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.044}" %tmpdata% | psxy -R -JM -Sc -C%D% -Wthin -O -t55 -K >> %ps%
gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.044}" %tmpdata% | psxy -R -JM -Sc -C%D% -Wthin -O -t60 -K >> %ps%
gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.044}" %tmpdata% | psxy -R -JM -Sc -C%D% -Wthin -O -t65 -K >> %ps%
REM gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.044}" %tmpdata% | psxy -R -JM -Sc -C%D% -Wthin -O -t70 -K >> %ps%
REM gawk "{if ($8>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $8<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $4,$5,$6,$7*0.044}" %tmpdata% | psxy -R -JM -Sc -C%D% -Wthin -O -t75 -K >> %ps%
gawk "{if ($8<%starttime%) print $4,$5,$6,$7*0.044}" %tmpdata% | psxy -R -JM -Sc -C%D% -Wthin -O -t70 -K >> %ps%
gawk "{print 128.0039,-0.6492,$3,$4,$5,$6,$7,$8,$9,$10,0,0,$13}" %focal% | psmeca -R -J -Sm0.31679999999999997/-1 -Z%D% -T0 -C -O -K >> %ps%
REM Cross Section Line AB (NP1)
psxy %lineAB% -J -R -O -K >> %ps%
pstext %text_A% -J -R -F+f8p,Helvetica+jCM -N -O -K >> %ps%
pstext %text_B% -J -R -F+f8p,Helvetica+jCM -N -O -K >> %ps%
REM Cross Section Line CD (NP2)
psxy %lineCD% -J -R -O -K >> %ps%
pstext %text_C% -J -R -F+f8p,Helvetica+jCM -N -O -K >> %ps%
pstext %text_D% -J -R -F+f8p,Helvetica+jCM -N -O -K >> %ps%
gawk "BEGIN {print strftime(\"%%d-%%m-%%Y %%H:%%M:%%S UTC\",%starttime%);}" | gawk "{print 129.87056666666666,1.1508,$0}" | pstext -R -JM -F+f6,Helvetica+jRT -O -K >> %ps%
echo 129.87056666666666 -2.5692 @@eqhalauwet | pstext -R -JM -F+f8,ZapfChancery-MediumItalic+jRB -O -K >> %ps%
REM Inset
pscoast -R%R_inset% -JM2 -Dh -W0.25p,black -Gwhite -S150/255/255 -B5::wsNE --MAP_FRAME_TYPE=plain --FONT_ANNOT_PRIMARY=8p -O -K >> %ps%
REM psxy ../inc/subduksi_moluccas.gmt -JM -R -W0.2 -Sf0.2c/0.03c+l+t -Gblack -O -K >> %ps%
REM psxy ../inc/fault_moluccas.gmt -JM -R -W0.2 -O -K >> %ps%
echo %llon% %blat% > ../tmp/box
echo %llon% %ulat% >> ../tmp/box
echo %rlon% %ulat% >> ../tmp/box
echo %rlon% %blat% >> ../tmp/box
echo %llon% %blat% >> ../tmp/box
psxy -R -JM ../tmp/box -Wthin,red -O -K >> %ps%
REM Parameter Peta
psbasemap -R0/1/0/1 -JX8/8 -B+t"" -X8.5 -Y0.6 -O -K >> %ps%
echo 0.5 0.94 %title% | pstext -J -R -F+f12p,Helvetica+jCM -O -K >> %ps%
echo 0.5 0.83 %typemag% %mainmag% | pstext -J -R -F+f10p,Helvetica+jCM -O -K>> %ps%
gawk "{print 0.5,0.68,$3,$4,$5,$6,$7,$8,$9,$10,0,0,$13}" %focal% | psmeca -R -J -Sm0.7/-1 -C -Z%D% -T0 -N -O -K >> %ps%
echo 0.5 0.51 Fault plane1:  strike=%strike1%  dip=%dip1%  slip=%slip1% | pstext -J -R -F+f8p,Helvetica+jCM -O -K >> %ps%
echo 0.5 0.40 Fault plane2:  strike=%strike2%  dip=%dip2%  slip=%slip2% | pstext -J -R -F+f8p,Helvetica+jCM -O -K >> %ps%
pslegend %L% -J -Dx0.25/0.1+w7.5/0.85i+jLB+l1.7 -O -K >> %ps%
REM box crossection
set boxwidht=8
set boxheight=3.5
set boxelev=1
REM boxelev = boxheight / 5
set boxoverlap=3
REM boxoverlap = boxheight - (1/2 * boxelev)
:CROSS_AB
psbasemap -JX%boxwidht%/%boxheight% -R%R2% -BWSne+t"Fault plane 1" -Bxa50+l"Distance (km)" -Bya20f20+l"Depth (km)" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -X-8.5 -Y-6 >> %ps%
echo %AC% 0 A | pstext -J -R -F+f10p,Helvetica+jRB -N -O -K >> %ps%
echo %BD% 0 B | pstext -J -R -F+f10p,Helvetica+jLB -N -O -K >> %ps%
gawk "{if ($5>%starttime%-%tpf% && $5<=%starttime%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi1% | psxy -R -J -Sc -C%D% -Wthin -O -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf% && $5<=%starttime%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi1% | psxy -R -J -Sc -C%D% -Wthin -O -t5 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi1% | psxy -R -J -Sc -C%D% -Wthin -O -t10 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi1% | psxy -R -J -Sc -C%D% -Wthin -O -t15 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi1% | psxy -R -J -Sc -C%D% -Wthin -O -t20 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi1% | psxy -R -J -Sc -C%D% -Wthin -O -t25 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi1% | psxy -R -J -Sc -C%D% -Wthin -O -t30 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi1% | psxy -R -J -Sc -C%D% -Wthin -O -t35 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi1% | psxy -R -J -Sc -C%D% -Wthin -O -t40 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi1% | psxy -R -J -Sc -C%D% -Wthin -O -t45 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi1% | psxy -R -J -Sc -C%D% -Wthin -O -t50 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi1% | psxy -R -J -Sc -C%D% -Wthin -O -t55 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi1% | psxy -R -J -Sc -C%D% -Wthin -O -t60 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi1% | psxy -R -J -Sc -C%D% -Wthin -O -t65 -K >> %ps%
REM gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi1% | psxy -R -J -Sc -C%D% -Wthin -O -t70 -K >> %ps%
REM gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi1% | psxy -R -J -Sc -C%D% -Wthin -O -t75 -K >> %ps%
gawk "{if ($5<%starttime%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi1% | psxy -R -J -Sc -C%D% -Wthin -O -t70 -K >> %ps%
psxy %dip_AB% -J -R -Wthin,black -O -K >> %ps%
gawk "{print 128.0039,-0.6492,-$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13}" %focal% | pscoupe -J -R%R3% -Sm0.31679999999999997/0/0 -T -Aa%startlon1%/%startlat1%/%endlon1%/%endlat1%/90/%width%/0/600 -Z%D% -E255 -N -O -K >> %ps%
:CROSS_CD
psbasemap -JX%boxwidht%/%boxheight% -R%R2% -BeSnw+t"Fault plane 2" -Bxa50+l"Distance (km)" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -X8.5 >> %ps%
echo %AC% 0 C | pstext -J -R -F+f10p,Helvetica+jRB -N -O -K >> %ps%
echo %BD% 0 D | pstext -J -R -F+f10p,Helvetica+jLB -N -O -K >> %ps%
gawk "{if ($5>%starttime%-%tpf% && $5<=%starttime%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi2% | psxy -R -J -Sc -C%D% -Wthin -O -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf% && $5<=%starttime%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi2% | psxy -R -J -Sc -C%D% -Wthin -O -t5 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi2% | psxy -R -J -Sc -C%D% -Wthin -O -t10 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi2% | psxy -R -J -Sc -C%D% -Wthin -O -t15 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi2% | psxy -R -J -Sc -C%D% -Wthin -O -t20 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi2% | psxy -R -J -Sc -C%D% -Wthin -O -t25 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi2% | psxy -R -J -Sc -C%D% -Wthin -O -t30 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi2% | psxy -R -J -Sc -C%D% -Wthin -O -t35 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi2% | psxy -R -J -Sc -C%D% -Wthin -O -t40 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi2% | psxy -R -J -Sc -C%D% -Wthin -O -t45 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi2% | psxy -R -J -Sc -C%D% -Wthin -O -t50 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi2% | psxy -R -J -Sc -C%D% -Wthin -O -t55 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi2% | psxy -R -J -Sc -C%D% -Wthin -O -t60 -K >> %ps%
gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi2% | psxy -R -J -Sc -C%D% -Wthin -O -t65 -K >> %ps%
REM gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi2% | psxy -R -J -Sc -C%D% -Wthin -O -t70 -K >> %ps%
REM gawk "{if ($5>%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf% && $5<=%starttime%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%-%tpf%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi2% | psxy -R -J -Sc -C%D% -Wthin -O -t75 -K >> %ps%
gawk "{if ($5<%starttime%) print $7, $3*(-1.0), $3, $4*0.044}" %proyeksi2% | psxy -R -J -Sc -C%D% -Wthin -O -t70 -K >> %ps%
psxy %dip_CD% -J -R -Wthin,black -O -K >> %ps%
gawk "{print 128.0039,-0.6492,-$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13}" %focal% | pscoupe -J -R%R3% -Sm0.31679999999999997/0/0 -T -Aa%startlon2%/%startlat2%/%endlon2%/%endlat2%/90/%width%/0/600 -Z%D% -E255 -N -O -K >> %ps%
echo on
gawk "{if ($8<%starttime%) print $7}" %tmpdata% | if length>0 (
gawk "{if ($8<%starttime%) print $7}" %tmpdata% | pshistogram -JX6/5.5 -W0.5+l -Bx+lMagnitude -By+l"Number of earthquakes" -BESwn --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 -Gblue -L1 -X8.5 -O -K >> %ps%
gawk "{if ($8<%starttime%) print $6}" %tmpdata% | pshistogram -JX6/5.5 -W2+l -Z4 -Bx+l"Depth (km)" -By+l"Log(Number of earthquakes)" -BESwn --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 -Gblue -L0.5 -Y7.5 -O -K >> %ps%
echo mantap
)
echo 0 0 @@eqhalauwet | pstext -R -JM -F+f8,ZapfChancery-MediumItalic+jRB -X8 -Y-8 -O >> %ps%
psconvert %ps% -Tg -E256 -P -A -Fframe/frame-%framenumber%
goto loopplot
:finishplot
ffmpeg -framerate %fps% -i frame/frame-%%d.png -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p %output%
REM gm convert -delay %delay% -loop %replay% frame/frame-*.png %output%
del gmt.history psconvert* Aa* %ps%
REM rd /S /Q frame
