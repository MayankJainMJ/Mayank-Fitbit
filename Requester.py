# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 17:44:37 2018

@author: mayan
"""


import urllib.request
from time import sleep
from datetime import datetime, timedelta
import json
import pandas as pd
import os
import numpy as np
os.chdir('C:/Users/mayan/Desktop/Fitbit/Mayank-Fitbit/')

def jsonify(resource,date,header_key,header_value,Tracker = False):    
    if resource == 'activity':
        req = urllib.request.Request('https://api.fitbit.com/1/user/-/activities/date/{}.json'.format(date))
    elif  Tracker == True:
        req = urllib.request.Request('https://api.fitbit.com/1/user/-/activities/tracker/{}/date/{}/1d.json'.format(resource,date))
    else :
        req = urllib.request.Request('https://api.fitbit.com/1/user/-/activities/{}/date/{}/1d.json'.format(resource,date))
    
    req.add_header(header_key, header_value)
    R = urllib.request.urlopen(req)
    if  Tracker == True:
        open('Data/'+resource+"_tracker_" + date + '.json', 'w').write(R.read().decode('utf8'))
        print("Recd tracker {} for {}".format(resource,date))
        sleep(1)
        dataload = json.load(open("Data/{}_tracker_{}.json".format(resource,date), buffering = 1000))
        os.remove("Data/{}_tracker_{}.json".format(resource,date))
    else:
        open('Data/'+ resource+"_" + date + '.json', 'w').write(R.read().decode('utf8'))
        print("Recd {} for {}".format(resource,date))
        sleep(1)
        dataload = json.load(open('Data/'+"{}_{}.json".format(resource,date), buffering = 1000))
        os.remove('Data/'+ "{}_{}.json".format(resource,date))
    return dataload


def jsonify_sleep(st,date,header_key,header_value):
    date2 = st.strftime("%Y-%m-%d")
    st1 = st - timedelta(days=1)
    date1 = st1.strftime("%Y-%m-%d")
    req = urllib.request.Request('https://api.fitbit.com/1/user/-/sleep/date/{}.json'.format(date1))
    req.add_header(header_key, header_value)
    R = urllib.request.urlopen(req)
    open('Data/'+"sleep1_" + date1 + '.json', 'w').write(R.read().decode('utf8'))
    sleep(1)
    req = urllib.request.Request('https://api.fitbit.com/1/user/-/sleep/date/{}.json'.format(date2))
    req.add_header(header_key, header_value)
    R = urllib.request.urlopen(req)
    open('Data/'+"sleep2_" + date2 + '.json', 'w').write(R.read().decode('utf8'))
    print("Recd {} for {} to {}".format("sleep",date1,date2))
    sleep(1)
    sleep1_F = json.load(open("Data/sleep1_{}.json".format(date1), buffering = 1000))
    sleep2_F = json.load(open("Data/sleep2_{}.json".format(date2), buffering = 1000))
    os.remove('Data/'+"sleep1_{}.json".format(date1))
    os.remove('Data/'+"sleep2_{}.json".format(date2))  
    s = []
    for i in range(len(sleep1_F['sleep'])):
        sl1 = sleep1_F['sleep'][i]['minuteData']
        for j in range(len(sl1)):
            if sl1[j]['dateTime'].split(':')[0]=='00':
                if sl1[j-1]['dateTime'].split(':')[0]=='23':
                    st1 = st1 + timedelta(days=1)
                    date1 = st1.strftime("%Y-%m-%d")
            time = date1 + ' '+':'.join(sl1[j]['dateTime'].split(':')[:-1])
            s.append((time,sl1[j]['value']))
    for i in range(len(sleep2_F['sleep'])):
        sl2 = sleep2_F['sleep'][i]['minuteData']
        for j in range(len(sl2)):
            if sl2[j]['dateTime'].split(':')[0]=='00':
                if sl2[j-1]['dateTime'].split(':')[0]=='23':
                    st = st + timedelta(days=1)
                    date2 = st.strftime("%Y-%m-%d")
            time = date2 + ' '+':'.join(sl2[j]['dateTime'].split(':')[:-1])
            s.append((time,sl2[j]['value']))   
    return s
def profiler(header_key, header_value):
    req = urllib.request.Request('https://api.fitbit.com/1/user/-/profile.json')
    req.add_header(header_key, header_value)
    P = urllib.request.urlopen(req)
    open('Data/'+'profile.json', 'w').write(P.read().decode('utf8'))
    print("Recd Profile Data")
    sleep(1)
    
def DataRetrieve(st,date,header_key,header_value):
    F = json.load(open('Data/'+"profile.json", buffering = 1000))
    P = {}
    P['fullName'] = F['user']['fullName'] 
    P['gender'] = F['user']['gender']
    P['height'] = F['user']['height']
    P['dateOfBirth'] = F['user']['dateOfBirth']
    P['weight'] = F['user']['weight']
    Pdf = pd.DataFrame(data = P,index=[0])
    PdfT =Pdf.T
 
    writer = pd.ExcelWriter('Data/'+F['user']['fullName'] +' '+ date +'.xlsx')
    PdfT.to_excel(writer,'Profile')
    
    heart_F = jsonify('heart',date,header_key,header_value)
    calories_F = jsonify('calories',date,header_key,header_value)
    steps_F = jsonify('steps',date,header_key,header_value)
    distance_F = jsonify('distance',date,header_key,header_value)
    elevation_F = jsonify('elevation',date,header_key,header_value)
    minutesSedentary_F = jsonify('minutesSedentary',date,header_key,header_value)
    minutesLightlyActive_F =jsonify('minutesLightlyActive',date,header_key,header_value)
    minutesFairlyActive_F = jsonify('minutesFairlyActive',date,header_key,header_value)
    minutesVeryActive_F = jsonify('minutesVeryActive',date,header_key,header_value)
    activity = jsonify('activity',date,header_key,header_value)
#    activityCalories_F = jsonify('activityCalories',date,header_key,header_value)
#    trackercalories = jsonify('calories',date,header_key,header_value,True)
#    trackersteps = jsonify('steps',date,header_key,header_value,True)
#    trackerdistance = jsonify('distance',date,header_key,header_value,True)
#    trackerfloors = jsonify('floors',date,header_key,header_value,True)
#    trackerelevation = jsonify('elevation',date,header_key,header_value,True)
    
    sl = jsonify_sleep(st,date,header_key,header_value)
    
   
    Date = heart_F['activities-heart'][0]['dateTime']
    Date = ''.join(Date.split('-'))

    h = heart_F['activities-heart-intraday']['dataset']
    c = calories_F['activities-calories-intraday']['dataset']
    s = steps_F['activities-steps-intraday']['dataset']
    d = distance_F['activities-distance-intraday']['dataset']
    e = elevation_F['activities-elevation-intraday']['dataset']
    fa = minutesFairlyActive_F['activities-minutesFairlyActive-intraday']['dataset']
    la = minutesLightlyActive_F['activities-minutesLightlyActive-intraday']['dataset']
    va = minutesVeryActive_F['activities-minutesVeryActive-intraday']['dataset']
    sed = minutesSedentary_F['activities-minutesSedentary-intraday']['dataset']

    l = []
    for i in range(len(h)):
        crash = 0
        time = date + ' ' + ':'.join(h[i]['time'].split(':')[:-1])
        for j in range(len(sl)):
            if time == str(sl[j][0]):
                crash = str(sl[j][1])               
        l.append((time, h[i]['value'], c[i]['value'], s[i]['value'],d[i]['value'],
                  e[i]['value'],2*la[i]['value'] + 3*fa[i]['value'] + 4*va[i]['value'] + 1*sed[i]['value'],crash))
    C = pd.DataFrame(l)
    C.columns = ['Time','Heart','Calories','Steps','Distance','Elevation',
                 'activity_type','Sleep']
                
#        l.append((time, h[i]['value'], c[i]['value'], s[i]['value'],d[i]['value'],
#                  e[i]['value'],fa[i]['value'],la[i]['value'],va[i]['value'],sed[i]['value'],2*la[i]['value'] + 3*fa[i]['value'] + 4*va[i]['value'] + 1*sed[i]['value'],crash))
#    C = pd.DataFrame(l)
#    C.columns = ['Time','Heart','Calories','Steps','Distance','Elevation',
#                 'MinutesFairlyActive','MinutesLightlyActive','MinutesVeryActive','MinutesSedentary','activity','Sleep']
    C.to_excel(writer,'Heart')

    D = {}
    try:
        D['RestingHeartRate'] = activity['summary']['restingHeartRate']
        D['ZoneRestHrs'] = round(activity['summary']['heartRateZones'][0]['minutes'] / 60, 3)
        D['ZoneFatburnHrs'] = round(activity['summary']['heartRateZones'][1]['minutes'] / 60, 3)
        D['ZoneCardioMins'] =activity['summary']['heartRateZones'][2]['minutes']
        D['ZonePeakMins'] =activity['summary']['heartRateZones'][3]['minutes']
        D['ZoneRestCals'] =activity['summary']['heartRateZones'][0]['caloriesOut']
        D['ZoneFatburnCals'] =activity['summary']['heartRateZones'][1]['caloriesOut']
        D['ZoneCardioCals'] =activity['summary']['heartRateZones'][2]['caloriesOut']
        D['ZonePeakCals'] =activity['summary']['heartRateZones'][3]['caloriesOut']
        D['BPM_Min'] = int(C[['Heart']].min())
        D['BPM_Mean'] = int(C[['Heart']].mean())
        D['BPM_Max'] = int(C[['Heart']].max())
        D['BPM_Std'] = int(C[['Heart']].std())
    except Exception as e:
        print("No Heart Summary for {}".format(st))
        print(e)
    D['CaloriesBMR'] =activity['summary']['caloriesBMR']
    D['CaloriesOut'] =activity['summary']['caloriesOut']
    D['CaloriesActivity'] =activity['summary']['activityCalories']
    D['ActiveVeryMins'] =activity['summary']['veryActiveMinutes']
    D['ActiveFairlyMins'] =activity['summary']['fairlyActiveMinutes']
    D['ActiveLightlyHrs'] = round(activity['summary']['lightlyActiveMinutes'] / 60, 3)
    D['Elevation'] =activity['summary']['elevation']
    D['Floors'] =activity['summary']['floors']
    D['Steps'] =activity['summary']['steps']
    D['Distance'] =activity['summary']['distances'][0]['distance']
    D['SedentaryHrs'] = round(activity['summary']['sedentaryMinutes'] / 60, 3)
    
    df = pd.DataFrame(data=D, index=[0])
    df.to_excel(writer,'Brief')
    writer.save()
    directory='CSV_{}'.format(F['user']['fullName'])
#    directory='CSV_Tarun Gupta'
    if not os.path.exists(directory):
        os.makedirs(directory)
    C.to_csv(directory + '/{}.csv'.format(date))
    return st + timedelta(days=1)
    
    