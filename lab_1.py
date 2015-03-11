# coding:utf8
import urllib2
import os
import pandas as pd
from datetime import datetime


def download(id, num):
    t = datetime.now()
    t = t.strftime('_%y-%m-%d_%H-%M')
    url = "http://www.star.nesdis.noaa.gov/smcd/emb/vci/gvix/G04/ts_L1/ByProvince/Mean/L1_Mean_UKR.R{0}.txt".format(id)
    vhi_url = urllib2.urlopen(url)
    out = open('vhi_id_{0}_{1}.csv'.format(num, t), 'wb')
    out.write(vhi_url.read())
    out.close()
    print "VHI {0} is downloaded...".format(id)



def read_and_print(path):
    for name in os.listdir(path):
        head = ['year', 'week', 'VHI', 'Area VHI < 15', 'Area VHI < 35']
        df = pd.read_csv(name, header=1)
        del df['SMN'], df['SMT'], df['VCI'], df['TCI']
        df.columns = head
        print df
    return df



def find(id, year):
    df = pd.read_csv(filter(lambda x: x.startswith('vhi_id' + id + '_'), os.listdir())[0], header=1)
    del df['SMN'], df['SMT'], df['VCI'], df['TCI']
    df.columns = head
    print "region # {0} in year {1}".format(id, year)
    print "max:"
    df = df[[(df['year'] == year) & (df['VHI'] == df['VHI'].max())]]
    print df
    print "min:"
    df = df[[(df['year'] == year) & (df['VHI'] == df['VHI'].min())]]
    print df
    return df

def extreme(id, area):
    df = pd.read_csv(filter(lambda x: x.startswith('vhi_id_' + id + '_'), os.listdir())[0], header=1)
    del df['SMN'], df['SMT'], df['VCI'], df['TCI']
    df.columns = head
    print df
    print "output for extreme:"
    df = df[df['Area VHI < 15'] > area]
    print df
    return df

def normal(id, area):
    df = pd.read_csv(filter(lambda x: x.startswith('vhi_id_' + id + '_'), os.listdir())[0], header=1)
    del df['SMN'], df['SMT'], df['VCI'], df['TCI']
    df.columns = head
    print df
    print "output for normal:"
    df = df[df['Area VHI < 35'] > area]
    print df
    return df

def extra_task():
    norma = 52/3
    for id in range(1,28):
        df = pd.read_csv(filter(lambda x: x.startswith('vhi_id_{:02d}_'), os.listdir())[0], header=1).format(id)
        extr = 0
        norm = 0
        for year in xrange(1981,2015):
            df = df[df['year']==year]
            for week in xrange(1,53):
                df = df[df['week']==week]
                if df['VHI'] < 15:
                    extr += 1
            if extr < 13:
                extr_bool = True
            for week in xrange(1,53):
                df = df[df['week']==week]
                if df['VHI'] < 35:
                    norm += 1
            if norm < norma:
                norm_bool = True
            if extr_bool & norm_bool:
                print df



os.chdir('VHI')
head = ['year', 'week', 'VHI', 'Area VHI < 15', 'Area VHI < 35']
number = 0
order = [24, 25, 5, 6, 27, 23, 26, 7, 11, 13, 14, 15, 16, 17, 18, 19, 21, 22, 8, 9, 10, 1, 3, 2, 4, 12, 20]
for i in order:
    number += 1
    download('{:02d}'.format(i), '{:02d}'.format(number))




