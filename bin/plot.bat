@echo off
REM echo EQ Map Generator
REM echo by eQ H
REM echo.--------------------------------------------------------
set ps=animasi.ps
set title=Animasi Aktifitas Gempabumi Wilayah Maluku dan Sekitarnya
set fromdate=22 Mei 2020
set todate=28 Mei 2020
set datasource=BMKG - Pusat Gempa Regional IX Ambon
set x1=134.63333333333333
set y1=-0.5
set x2=129.5
set y2=-9.5
set z2=270
set llon=124.0
set rlon=135.0
set blat=-10.0
set ulat=0.0
set R=%llon%/%rlon%/%blat%/%ulat%
set R_inset=116.3/142.7/-13.333333333333332/3.333333333333333
set R2=0/4/0/3
set D=../inc/depth.cpt
set L=../tmp/legenda
set tmpdata=../tmp/tmpdata.dat
set tmpdirasakan=../tmp/tmpdirasakan.dat
set output=../output/animasi.mp4
set station=../data/station.sel
set fault=../inc/fault_moluccas.gmt
set subduction=../inc/subduksi_moluccas.gmt
set starttime=1590094427
set stoptime=1590712222
REM time sampling per frame (second)
set tpf=27703
REM frame per second (ffmpeg)
set fps=1
REM time delay every frame (gm)
set delay=100
set replay=0
:depthcpt
if exist %D% (
goto :prepare
) else (
echo generate %D%
run cptdepth_std.bat
)
:prepare
if exist frame\ (
rd /S /Q frame
)
mkdir frame
set /a framenumber = -1
set /a introframe= %framenumber% +3
:loopintro
set /a framenumber = %framenumber% + 1
if %framenumber% GTR %introframe% (
set /a framenumber = %framenumber% - 1
goto loopplot
)
psimage ../inc/intro.jpg -Dx0/0+w29.622c/19.412c -X0 -Y0 -K > %ps%
psbasemap -JX29.7/19.412 -R%R2% -Bx --FONT_ANNOT_PRIMARY=5 -O -K >> %ps%
echo ^> 2 1.55 1 28 c > ../tmp/judul
echo %title% >> ../tmp/judul
pstext ../tmp/judul -R -J -F+f24p,NewCenturySchlbk-Italic,white+jCM -M -O -K >> %ps%
echo 2 1.15 %fromdate% | pstext -R -J -F+f18,NewCenturySchlbk-Italic,white+jCB -N -O -K >> %ps%
echo 2 0.95 hingga | pstext -R -J -F+f18,NewCenturySchlbk-Italic,white+jCB -N -O -K >> %ps%
echo 2 0.75 %todate% | pstext -R -J -F+f18,NewCenturySchlbk-Italic,white+jCB -N -O -K >> %ps%
echo 3.9 0.1 Sumber Data: %datasource% | pstext -R -J -F+f11p,NewCenturySchlbk-Italic,white+jRB -N -O >> %ps%
psconvert %ps% -Tg -E512 -P -A0.2 -Fframe/frame-%framenumber%
goto loopintro
:loopplot
set /a framenumber = %framenumber% + 1
set /a starttime= %starttime% + %tpf%
if %starttime% GTR %stoptime% (
set /a framenumber = %framenumber% - 1
set /a stopframe= %framenumber% +4
goto loopoutro
)
goto plot
:plot
REM MEMBUAT PETA SEISMISITAS
pscoast -R%R% -JM15 -Dh -B2::WSne -G245/245/200 -S150/255/255 -W0.2p,black -Lg%x2%/%y2%+c-1+w%z2%k+l+ab+jTC -Tdg%x2%/%y2%+w1.2+f1+jBC --MAP_ANNOT_MIN_SPACING=0.1p --FONT_TITLE=10 --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 -K > %ps%
psxy %subduction% -JM -R -W0.51 -Sf0.8i/0.08i+r+t -Gblack -O -K >> %ps%
psxy %fault% -JM -R -W0.51 -O -K >> %ps%
REM Data
gawk -F" " "{print $2, $3}" %station% | psxy -J -R%R% -St0.3c -W0.25,black -Gblue -O -K >> %ps%
gawk -F" " "{print  $2, $3, $1}" %station% | pstext -J -R -F+f8p,Helvetica+jLT -O -K >> %ps%
gawk "{if ($10>%starttime%-%tpf% && $10<=%starttime%) print $6,$7,$8,$9*0.0440}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.25 -O -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf% && $10<=%starttime%-%tpf%) print $6,$7,$8,$9*0.0440}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.25 -O -t20.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0440}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.25 -O -t40.0 -K >> %ps%
gawk "{if ($10>%starttime%-%tpf%-%tpf%-%tpf%-%tpf% && $10<=%starttime%-%tpf%-%tpf%-%tpf%) print $6,$7,$8,$9*0.0440}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.25 -O -t60.0 -K >> %ps%
gawk "{if ($10<%starttime%) print $6,$7,$8,$9*0.0440}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.25 -O -t70 -K >> %ps%
gawk "BEGIN {print strftime(\"%%d-%%m-%%Y %%H:%%M:%%S WIT\",%starttime%);}" | gawk "{print 134.63333333333333,-0.5,$0}" | pstext -R -JM -F+f8,Helvetica+jRT -O -K >> %ps%
psimage ../inc/logo.png -R -J -Dg124.36666666666666/-0.5+w2.3c+jLT -K -O >> %ps%
pscoast -R%R_inset% -JM4 -Dh -W0.2p,black -Gwhite -S150/255/255 -B5::wsNE --MAP_FRAME_TYPE=plain --FONT_ANNOT_PRIMARY=6 -O -K >> %ps%
psbasemap -R0/4/0/2.0 -JX4/2.0 -Bx --FONT_ANNOT_PRIMARY=6 -O -K -X11 >> %ps%
psscale -Dg2.0/1.3333333333333333+w3.2/0.25+e+macl+h+jCB -J -R -Bx100+l"Kedalaman (km)" -G0/500 -I1 --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=6 --FONT_LABEL=6 -C%D% -O -K >> %ps%
psxy %L% -R -J -Sc -W0.35 -O -K >> %ps%
gawk "{print $1,$4,$5}" %L% | pstext -J -R -F+f6p,Helvetica,black+jCB -O -K >> %ps%
REM psxy %subduction% -JM -R%R_inset% -W0.39 -Sf0.2c/0.03c+r+t -Gblack -O -K >> %ps%
REM psxy %fault% -JM -R%R_inset% -W0.39 -O -K >> %ps%
echo %llon% %blat% > ../tmp/box
echo %llon% %ulat% >> ../tmp/box
echo %rlon% %ulat% >> ../tmp/box
echo %rlon% %blat% >> ../tmp/box
echo %llon% %blat% >> ../tmp/box
psxy -R%R_inset% -JM ../tmp/box -W0.6,red -O -K -X-11>> %ps%
psbasemap -JX5/3.5787878787878786 -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -X15.5 >> %ps%
gawk "{if ($10<=%starttime%) print $9}" %tmpdata% | pshistogram -JX5/3.5787878787878786 -W0.5+b -Gblue -L -BESwn -Bx+lMagnitude -By+l"Jumlah Gempabumi" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> %ps%
psbasemap -JX5/3.5787878787878786 -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y5.028787878787878 >> %ps%
gawk "{if ($10<=%starttime%) print $8}" %tmpdata% | pshistogram -JX5/3.5787878787878786 -W20+b -Gblue -L -Z4 -BESwn -Bx+l"Kedalaman (km)" -By+l"Log(Jumlah Gempabumi)" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K  >> %ps%
psbasemap -JX5/3.5787878787878786 -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y5.028787878787878 >> %ps%
gawk "{if ($10<=%starttime%) print $4}" %tmpdata% | pshistogram -JX5/3.5787878787878786 -W1+b -Gblue -L -BESwn -Bx+l"Tanggal (UTC)" -By+l"Jumlah Gempabumi" -F --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K  >> %ps%
echo 0.9 -0.24 "by: @@eqhalauwet" | pstext -R -Bg1x -J -F+f9,ZapfChancery-MediumItalic+jLT -Y-10.057575757575757 -N -O >> %ps%
psconvert %ps% -Tg -E512 -P -A0.2 -Fframe/frame-%framenumber%
goto loopplot
:loopoutro
set /a framenumber = %framenumber% + 1
if %framenumber% GTR %stopframe% goto renderplot
pscoast -R%R% -JM15 -Dh -B2::WSne -G245/245/200 -S150/255/255 -W0.2p,black -Lg%x2%/%y2%+c-1+w%z2%k+l+ab+jTC -Tdg%x2%/%y2%+w1.2+f1+jBC --MAP_ANNOT_MIN_SPACING=0.1p --FONT_TITLE=10 --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 -K > %ps%
psxy %subduction% -JM -R -W0.51 -Sf0.8i/0.08i+r+t -Gblack -O -K >> %ps%
psxy %fault% -JM -R -W0.51 -O -K >> %ps%
REM Data
gawk -F" " "{print $2, $3}" %station% | psxy -J -R%R% -St0.3c -W0.25,black -Gblue -O -K >> %ps%
gawk -F" " "{print  $2, $3, $1}" %station% | pstext -J -R -F+f8p,Helvetica+jLT -O -K >> %ps%
gawk "{print $6,$7,$8,$9*0.0440}" %tmpdata% | psxy -R -JM -Sc -C%D% -W0.25 -O -K >> %ps%
psimage ../inc/logo.png -R -J -Dg124.36666666666666/-0.5+w2.3c+jLT -K -O >> %ps%
echo ^> 129.5 -1.8181818181818181 0.4 14 c > ../tmp/judul
echo %title% >> ../tmp/judul
pstext ../tmp/judul -R -J -F+f12p,NewCenturySchlbk-BoldItalic,black+jCB -Gwhite -M -t20 -O -K >> %ps%
echo 129.5 -2.2222222222222223 %fromdate% hingga %todate% | pstext -R -J -F+f10,NewCenturySchlbk-BoldItalic,black+jCB -Gwhite -N -t20 -O -K >> %ps%
echo 129.5 -2.857142857142857 Jumlah gempabumi 45 kejadian, 1 dilaporkan dirasakan oleh masyarakat | pstext -R -J -F+f9,NewCenturySchlbk-BoldItalic,black+jCM -Gwhite -N -t20 -O -K >> %ps%
pscoast -R%R_inset% -JM4 -Dh -W0.2p,black -Gwhite -S150/255/255 -B5::wsNE --MAP_FRAME_TYPE=plain --FONT_ANNOT_PRIMARY=6 -O -K >> %ps%
psbasemap -R0/4/0/2.0 -JX4/2.0 -Bx --FONT_ANNOT_PRIMARY=6 -O -K -X11 >> %ps%
psscale -Dg2.0/1.3333333333333333+w3.2/0.25+e+macl+h+jCB -J -R -Bx100+l"Kedalaman (km)" -G0/500 -I1 --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=6 --FONT_LABEL=6 -C%D% -O -K >> %ps%
psxy %L% -R -J -Sc -W0.35 -O -K >> %ps%
gawk "{print $1,$4,$5}" %L% | pstext -J -R -F+f6p,Helvetica,black+jCB -O -K >> %ps%
REM psxy %subduction% -JM -R%R_inset% -W0.39 -Sf0.2c/0.03c+r+t -Gblack -O -K >> %ps%
REM psxy %fault% -JM -R%R_inset% -W0.39 -O -K >> %ps%
echo %llon% %blat% > ../tmp/box
echo %llon% %ulat% >> ../tmp/box
echo %rlon% %ulat% >> ../tmp/box
echo %rlon% %blat% >> ../tmp/box
echo %llon% %blat% >> ../tmp/box
psxy -R%R_inset% -JM ../tmp/box -W0.6,red -O -K -X-11>> %ps%
psbasemap -JX5/3.5787878787878786 -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -X15.5 >> %ps%
gawk "{if ($10<=%starttime%) print $9}" %tmpdata% | pshistogram -JX5/3.5787878787878786 -W0.5+b -Gblue -L -BESwn -Bx+lMagnitude -By+l"Jumlah Gempabumi" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K >> %ps%
psbasemap -JX5/3.5787878787878786 -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y5.028787878787878 >> %ps%
gawk "{if ($10<=%starttime%) print $8}" %tmpdata% | pshistogram -JX5/3.5787878787878786 -W20+b -Gblue -L -Z4 -BESwn -Bx+l"Kedalaman (km)" -By+l"Log(Jumlah Gempabumi)" --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K  >> %ps%
psbasemap -JX5/3.5787878787878786 -R/0/1/0/1 -Bg1x --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K -Y5.028787878787878 >> %ps%
gawk "{if ($10<=%starttime%) print $4}" %tmpdata% | pshistogram -JX5/3.5787878787878786 -W1+b -Gblue -L -BESwn -Bx+l"Tanggal (UTC)" -By+l"Jumlah Gempabumi" -F --MAP_ANNOT_MIN_SPACING=0.1p --FONT_ANNOT_PRIMARY=8 --FONT_LABEL=9 --FONT_TITLE=10 -O -K  >> %ps%
echo 0.9 -0.24 "by: @@eqhalauwet" | pstext -R -Bg1x -J -F+f9,ZapfChancery-MediumItalic+jLT -Y-10.057575757575757 -N -O >> %ps%
psconvert %ps% -Tg -E512 -P -A0.2 -Fframe/frame-%framenumber%
goto loopoutro
:renderplot
ffmpeg -framerate %fps% -i frame/frame-%%d.png -c:v libx264 -profile:v high -crf 18 -pix_fmt yuv420p -vf "scale=1080:ceil(ih/(iw/1080*2))*2" %output%
REM gm convert -delay %delay% -loop %replay% frame/frame-*.png %output%
del gmt.history psconvert* Aa* %ps%
REM rd /S /Q frame
