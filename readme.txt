1. masukan parameter Title, Plot_Area, Durasi_Animasi, Frame_per_second, Type data, dan Opsi konversi waktu, dll pada file "parameter.inp". [untuk opsi plot_area masukan parameter format yang digunakan pada baris keempat dibawah plot_area]
2. jika ingin plot cross_section, tambahkan parameter Epic, Mag, Nodal Plane, Panjang Cross-Section, Max kedalaman Cross-Section, serta Opsi plot topografi.
3. masukan data hiposenter ke file data/hiposenter.dat & data dirasakan ke file data/dirasakan.dat (format: SDIGB/Hypodd/ASCII)
4. masukan data stasiun yang digunakan ke file input/station.sel (format: kode_sta long lat elev) [diisi jika menggunakan opsi plot cross section]
5. masukan data focal mechanism (global cmt) ke file psmeca.dat (format gmt psmeca CMT) [diisi jika menggunakan opsi plot cross section]
6. Run plot.py