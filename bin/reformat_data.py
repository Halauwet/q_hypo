from datetime import datetime
from datetime import timedelta

# python function by eQ
#
# reformat data to plot animation (time convert to second)
#
# using:
# ot_start, time_sec = from_sdigb(inputdata, outputdata, tz_sign, timezone, tz_name)
# example : ot_start, time_sec = from_sdigb(datagempa, datatmp, +, 9, WIT)
# MASIH ERROR KONVERSI SEBELUM TAHUN 1970
# DATA GEMPA KE INPUT TMP KE OUTPUT TZONE

def from_sdigb(inputdata, outputdata, tz_sign, timezone, tz_name):
    print('Input data SDIGB')
    file=open(inputdata,'r') 
    baris=file.readlines()
    for i in range(len(baris)):
        baris[i]=baris[i].split(',')
    file.close()
    file = open(outputdata,'w')
    i = 1
    jumlah_event=str(len(baris)-i)
    while i < len(baris):
        try:
            if len(baris[i])>0:
                tahun = baris[i][1].split('/')[2]
                tahun = int(tahun.split()[0])
                bulan = int(baris[i][1].split('/')[0])
                tanggal = int(baris[i][1].split('/')[1])
                jam = int(baris[i][2].split(':')[0].zfill(2))
                menit = int(baris[i][2].split(':')[1].zfill(2))
                detik = int(baris[i][2].split(':')[2].zfill(2))
                lintang = (('%.6f')%float(baris[i][3])).zfill(6)
                bujur = (('%.6f')%float(baris[i][4])).zfill(6)
                depth = ('%.2f')%float(baris[i][5])
                mag = ('%.2f')%float(baris[i][6])
                ot=datetime(tahun,bulan,tanggal,jam,menit,detik)
                if timezone == 0:
                    # print('timezone: UTC')
                    time_sec=ot.timestamp()
                    displayed_time=ot.strftime('%d-%m-%Y %H:%M:%S ')+tz_name
                else:
                    if tz_sign == '+':
                        lt=ot + timedelta(hours=timezone)
                    elif tz_sign == '-':
                        lt=ot - timedelta(hours=timezone)
                    else:
                        print('check convert time parameter on parameter.inp')
                        print('format: "Sign" "Time_Zone" "Zone_Name"')
                        print('example: "+ 9 WIT" (without quotes)')
                        break
                    # print('timezone: '+str(tz_name)+' ('+tz_sign+str(timezone)+' hours)')
                    time_sec=lt.timestamp()
                    displayed_time=lt.strftime('%d-%m-%Y %H:%M:%S ')+tz_name
                # print(str(i)+' '+str(tahun)+'-'+str(bulan)+'-'+str(tanggal)+' '+str(jam)+':'+str(menit)+':'+str(detik)+' '+str(bujur)+' '+str(lintang)+' '+str(depth)+' '+str(mag)+' '+str(time_sec)+' "'+str(displayed_time)+'"')
                file.write(str(i)+' '+str(tahun)+' '+str(bulan)+' '+str(tanggal)+' '+str(jam)+':'+str(menit)+':'+str(detik)+' '+str(bujur)+' '+str(lintang)+' '+str(depth)+' '+str(mag)+' '+str(time_sec)+' "'+str(displayed_time)+'"\n')
                if i==1:
                    ot_start=time_sec
            i += 1
        except:
            print('Please recheck input data option on "parameter.inp"')
            break
    file.close()
    return ot_start, time_sec, jumlah_event
    
def from_hypodd(inputdata, outputdata, tz_sign, timezone, tz_name):
    print('Input data HypoDD')
    file=open(inputdata,'r') 
    baris=file.readlines()
    for i in range(len(baris)):
        baris[i]=baris[i].split()
    file.close()
    file = open(outputdata,'w')
    i = 0
    jumlah_event=str(len(baris)-i)
    while i < len(baris):
        try:
            if len(baris[i])>0:
                tahun = int(baris[i][10])
                bulan = int(baris[i][11])
                tanggal = int(baris[i][12])
                jam = int(baris[i][13])
                menit = int(baris[i][14])
                detik = int(float(baris[i][15]))
                lintang = (('%.6f')%float(baris[i][1])).zfill(6)
                bujur = (('%.6f')%float(baris[i][2])).zfill(6)
                depth = ('%.2f')%float(baris[i][3])
                mag = ('%.2f')%float(baris[i][16])
                ot=datetime(tahun,bulan,tanggal,jam,menit,detik)
                if timezone == 0:
                    # print('timezone: UTC')
                    time_sec=ot.timestamp()
                    displayed_time=ot.strftime('%d-%m-%Y %H:%M:%S ')+tz_name
                else:
                    if tz_sign == '+':
                        lt=ot + timedelta(hours=timezone)
                    elif tz_sign == '-':
                        lt=ot - timedelta(hours=timezone)
                    else:
                        print('check convert time parameter on parameter.inp')
                        print('format: "Sign" "Time_Zone" "Zone_Name"')
                        print('example: "+ 9 WIT" (without quotes)')
                        break
                    # print('timezone: '+str(tz_name)+' ('+tz_sign+str(timezone)+' hours)')
                    time_sec=lt.timestamp()
                    displayed_time=lt.strftime('%d-%m-%Y %H:%M:%S ')+tz_name
                # print(str(i)+' '+str(tahun)+'-'+str(bulan)+'-'+str(tanggal)+' '+str(jam)+':'+str(menit)+':'+str(detik)+' '+str(bujur)+' '+str(lintang)+' '+str(depth)+' '+str(mag)+' '+str(time_sec)+' "'+str(displayed_time)+'"')
                file.write(str(i)+' '+str(tahun)+' '+str(bulan)+' '+str(tanggal)+' '+str(jam)+':'+str(menit)+':'+str(detik)+' '+str(bujur)+' '+str(lintang)+' '+str(depth)+' '+str(mag)+' '+str(time_sec)+' "'+str(displayed_time)+'"\n')
                if i==1:
                    ot_start=time_sec
            i = i+1
        except:
            print('Please recheck input data option on "parameter.inp"')
            break
    file.close()
    return ot_start, time_sec, jumlah_event
    
def from_ascii(inputdata, outputdata, tz_sign, timezone, tz_name):
    print('Input from ASCII data sort ascending')
    print('Format: "tahun bulan tanggal jam menit detik lintang bujur depth magnitudo"')
    file=open(inputdata,'r') 
    baris=file.readlines()
    for i in range(len(baris)):
        baris[i]=baris[i].split()
    file.close()
    file = open(outputdata,'w')
    i = 0
    jumlah_event=str(len(baris)-i)
    while i < len(baris):
        try:
            if len(baris[i])>0:
                tahun = int(baris[i][0])
                bulan = int(baris[i][1])
                tanggal = int(baris[i][2])
                jam = int(baris[i][3])
                menit = int(baris[i][4])
                detik = int(float(baris[i][5]))
                lintang = (('%.6f')%float(baris[i][6])).zfill(6)
                bujur = (('%.6f')%float(baris[i][7])).zfill(6)
                depth = ('%.2f')%float(baris[i][8])
                mag = ('%.2f')%float(baris[i][9])
                ot=datetime(tahun,bulan,tanggal,jam,menit,detik)
                if timezone == 0:
                    # print('timezone: UTC')
                    time_sec=ot.timestamp()
                    displayed_time=ot.strftime('%d-%m-%Y %H:%M:%S ')+tz_name
                else:
                    if tz_sign == '+':
                        lt=ot + timedelta(hours=timezone)
                    elif tz_sign == '-':
                        lt=ot - timedelta(hours=timezone)
                    else:
                        print('check convert time parameter on parameter.inp')
                        print('format: "Sign" "Time_Zone" "Zone_Name"')
                        print('example: "+ 9 WIT" (without quotes)')
                        break
                    # print('timezone: '+str(tz_name)+' ('+tz_sign+str(timezone)+' hours)')
                    time_sec=lt.timestamp()
                    displayed_time=lt.strftime('%d-%m-%Y %H:%M:%S ')+tz_name
                # print(str(i)+' '+str(tahun)+'-'+str(bulan)+'-'+str(tanggal)+' '+str(jam)+':'+str(menit)+':'+str(detik)+' '+str(bujur)+' '+str(lintang)+' '+str(depth)+' '+str(mag)+' '+str(time_sec)+' "'+str(displayed_time)+'"')
                file.write(str(i)+' '+str(tahun)+' '+str(bulan)+' '+str(tanggal)+' '+str(jam)+':'+str(menit)+':'+str(detik)+' '+str(bujur)+' '+str(lintang)+' '+str(depth)+' '+str(mag)+' '+str(time_sec)+' "'+str(displayed_time)+'"\n')
                if i==1:
                    ot_start=time_sec
            i = i+1
        except:
            print('Please recheck input data option on "parameter.inp"')
            break
    file.close()
    return ot_start, time_sec, jumlah_event
    
    
def sdigb_to_geoq(inputdata, outputdata, tz_sign, timezone, tz_name): #SDIGB data to geoQ format
    print('Input data SDIGB')
    file=open(inputdata,'r')
    baris=file.readlines()
    ot_start=0
    time_sec=0
    jumlah_event=0
    if len(baris) > 0:
        for i in range(len(baris)):
            baris[i]=baris[i].split(',')
        file.close()
        file = open(outputdata,'w')
        i = 1
        jumlah_event=str(len(baris)-i)
        while i < len(baris):
            try:
                if len(baris[i])>0:
                    tahun = baris[i][1].split('/')[2]
                    tahun = int(tahun.split()[0])
                    bulan = int(baris[i][1].split('/')[0])
                    tanggal = int(baris[i][1].split('/')[1])
                    jam = int(baris[i][2].split(':')[0].zfill(2))
                    menit = int(baris[i][2].split(':')[1].zfill(2))
                    detik = int(baris[i][2].split(':')[2].zfill(2))
                    lintang = (('%.6f')%float(baris[i][3])).zfill(6)
                    bujur = (('%.6f')%float(baris[i][4])).zfill(6)
                    depth = ('%.2f')%float(baris[i][5])
                    mag = ('%.2f')%float(baris[i][6])
                    ot=datetime(tahun,bulan,tanggal,jam,menit,detik)
                    time_sec, displayed_time = convert_timezone(ot, tz_sign, timezone, tz_name)
                    # print(str(i)+' '+str(tahun)+'-'+str(bulan)+'-'+str(tanggal)+' '+str(jam)+':'+str(menit)+':'+str(detik)+' '+str(bujur)+' '+str(lintang)+' '+str(depth)+' '+str(mag)+' '+str(time_sec)+' "'+str(displayed_time)+'"')
                    file.write(str(i)+' '+str(tahun)+' '+str(bulan)+' '+str(tanggal)+' '+str(jam)+':'+str(menit)+':'+str(detik)+' '+str(bujur)+' '+str(lintang)+' '+str(depth)+' '+str(mag)+' '+str(time_sec)+' "'+str(displayed_time)+'"\n')
                    if i==1:
                        ot_start=time_sec
                i = i+1
            except:
                print('Please recheck input data')
                break
    file.close()
    return ot_start, time_sec, jumlah_event


def hypodd_to_geoq(inputdata, outputdata, tz_sign, timezone, tz_name): #HypoDD data to geoQ format
    print('Input data HypoDD')
    file=open(inputdata,'r')
    baris=file.readlines()
    if len(baris) > 0:
        for i in range(len(baris)):
            baris[i]=baris[i].split()
        file.close()
        file = open(outputdata,'w')
        i = 0
        jumlah_event=str(len(baris)-i)
        while i < len(baris):
            try:
                if len(baris[i])>0:
                    tahun = int(baris[i][10])
                    bulan = int(baris[i][11])
                    tanggal = int(baris[i][12])
                    jam = int(baris[i][13])
                    menit = int(baris[i][14])
                    detik = int(float(baris[i][15]))
                    lintang = (('%.6f')%float(baris[i][1])).zfill(6)
                    bujur = (('%.6f')%float(baris[i][2])).zfill(6)
                    depth = ('%.2f')%float(baris[i][3])
                    mag = ('%.2f')%float(baris[i][16])
                    ot=datetime(tahun,bulan,tanggal,jam,menit,detik)
                    time_sec, displayed_time = convert_timezone(ot, tz_sign, timezone, tz_name)
                    # print(str(i)+' '+str(tahun)+'-'+str(bulan)+'-'+str(tanggal)+' '+str(jam)+':'+str(menit)+':'+str(detik)+' '+str(bujur)+' '+str(lintang)+' '+str(depth)+' '+str(mag)+' '+str(time_sec)+' "'+str(displayed_time)+'"')
                    file.write(str(i)+' '+str(tahun)+' '+str(bulan)+' '+str(tanggal)+' '+str(jam)+':'+str(menit)+':'+str(detik)+' '+str(bujur)+' '+str(lintang)+' '+str(depth)+' '+str(mag)+' '+str(time_sec)+' "'+str(displayed_time)+'"\n')
                    if i==0:
                        ot_start=time_sec
                i = i+1
            except:
                print('Please recheck input data')
                break
    else:
        ot_start=0; time_sec=0; jumlah_event=0
    file.close()
    return ot_start, time_sec, jumlah_event


def ascii_to_geoq(inputdata, outputdata, tz_sign, timezone, tz_name): #ASCII data to geoQ format
    print('Input Format: "tahun bulan tanggal jam menit detik lintang bujur depth magnitudo"')
    file=open(inputdata,'r')
    baris=file.readlines()
    if len(baris) > 0:
        for i in range(len(baris)):
            baris[i]=baris[i].split()
        file.close()
        file = open(outputdata,'w')
        i = 0
        jumlah_event=str(len(baris)-i)
        while i < len(baris):
            try:
                if len(baris[i])>0:
                    tahun = int(baris[i][0])
                    bulan = int(baris[i][1])
                    tanggal = int(baris[i][2])
                    jam = int(baris[i][3])
                    menit = int(baris[i][4])
                    detik = int(float(baris[i][5]))
                    lintang = (('%.6f')%float(baris[i][6])).zfill(6)
                    bujur = (('%.6f')%float(baris[i][7])).zfill(6)
                    depth = ('%.2f')%float(baris[i][8])
                    mag = ('%.2f')%float(baris[i][9])
                    ot=datetime(tahun,bulan,tanggal,jam,menit,detik)
                    time_sec, displayed_time = convert_timezone(ot, tz_sign, timezone, tz_name)
                    # print(str(i)+' '+str(tahun)+'-'+str(bulan)+'-'+str(tanggal)+' '+str(jam)+':'+str(menit)+':'+str(detik)+' '+str(bujur)+' '+str(lintang)+' '+str(depth)+' '+str(mag)+' '+str(time_sec)+' "'+str(displayed_time)+'"')
                    file.write(str(i)+' '+str(tahun)+' '+str(bulan)+' '+str(tanggal)+' '+str(jam)+':'+str(menit)+':'+str(detik)+' '+str(bujur)+' '+str(lintang)+' '+str(depth)+' '+str(mag)+' '+str(time_sec)+' "'+str(displayed_time)+'"\n')
                    if i==0:
                        ot_start=time_sec
                i = i+1
            except:
                print('Please recheck input data')
                break
    else:
        ot_start=0; time_sec=0; jumlah_event=0
    file.close()
    return ot_start, time_sec, jumlah_event


def convert_timezone(ot, tz_sign, timezone, tz_name):
    if timezone == 0:
        # print('timezone: UTC')
        time_sec=ot.timestamp()
        displayed_time=ot.strftime('%d-%m-%Y %H:%M:%S ')+tz_name
    else:
        if tz_sign == '+':
            lt=ot + timedelta(hours=timezone)
            time_sec=lt.timestamp()
            displayed_time=lt.strftime('%d-%m-%Y %H:%M:%S ')+tz_name
        elif tz_sign == '-':
            lt=ot - timedelta(hours=timezone)
            time_sec=lt.timestamp()
            displayed_time=lt.strftime('%d-%m-%Y %H:%M:%S ')+tz_name
        else:
            print('check convert time parameter!')
            print('format: "Sign", "Time_Zone", "Zone_Name"')
            print('example: "'+', 9, WIT" (without quotes)')
            time_sec='0000000000.0'
            displayed_time='00-00-0000 00:00:00'+tz_name
        # print('timezone: '+str(tz_name)+' ('+tz_sign+str(timezone)+' hours)')
    return time_sec, displayed_time