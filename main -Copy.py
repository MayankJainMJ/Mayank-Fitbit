
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 16:06:26 2017

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
#Code = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2Nko0Q00iLCJhdWQiOiIyMkNIVzgiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd251dCB3cHJvIHdzbGUgd3dlaSB3c29jIHdzZXQgd2FjdCB3bG9jIiwiZXhwIjoxNTE1MDg5OTgzLCJpYXQiOjE1MTUwNjExODN9.6Maao3z8M6qyQpKR3gxH3YHXSshQfpKoeY_mAqy7ocI'
from iniHandler import print_data, print_json, ReadCredentials, ReadTokens
from authHandler import *

if __name__ == "__main__":
    ResourceTypes = ['steps', 'floors', 'caloriesOut']

	#This is the Fitbit URL to use for the API call
    FitbitURL = "https://api.fitbit.com/1/user/-/profile.json"

	#Get credentials
    ClientID, ClientSecret = ReadCredentials()

    APICallOK = False
    while not APICallOK:
		#Get tokens
        AccessToken, RefreshToken = ReadTokens()
		#Make the API call
        APICallOK, TokensOK, APIResponse = MakeAPICall(FitbitURL, AccessToken, RefreshToken)
		
        print_json('status',APIResponse)
        if not TokensOK:
            sys.exit(1)
            
try:
    Day, Month, Year = input('Enter From Date in format(Day-Month-Year): ').split('-')
    st = datetime.date(datetime(int(Year), int(Month), int(Day)))
    print('data from date : {}'.format(st))
except Exception as e:
    st = datetime.date((datetime.now() - timedelta(days=1)))
    print('data of date : {}'.format(st))
    
try:
    Dayx, Monthx, Yearx = input('Enter To Date in format(Day-Month-Year): ').split('-')
    stx = datetime.date(datetime(int(Yearx), int(Monthx), int(Dayx)))
    if stx >= datetime.date(datetime.now()):
        stx = datetime.date(datetime.now()) - timedelta(days=1)        
except Exception as e:
    stx = datetime.date(datetime.now()) - timedelta(days=1)
    print('data till date : {}'.format(stx))
    
    
header_key = 'Authorization'
header_value = 'Bearer ' + AccessToken

#st = datetime.date(datetime(int(Year), int(Month), int(Day)))

#profile

req = urllib.request.Request('https://api.fitbit.com/1/user/-/profile.json')

req.add_header(header_key, header_value)
P = urllib.request.urlopen(req)
open('Data/'+'profile.json', 'w').write(P.read().decode('utf8'))
print("Recd Profile Data")
sleep(1)

def jsonify(resource,date,Tracker = False):    
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


def jsonify_sleep(st,date):
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
    
    
while st <= stx:
    date = st.strftime("%Y-%m-%d")
    
    
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
    
    heart_F = jsonify('heart',date)
    calories_F = jsonify('calories',date)
    steps_F = jsonify('steps',date)
    distance_F = jsonify('distance',date)
    elevation_F = jsonify('elevation',date)
    minutesSedentary_F = jsonify('minutesSedentary',date)
    minutesLightlyActive_F =jsonify('minutesLightlyActive',date)
    minutesFairlyActive_F = jsonify('minutesFairlyActive',date)
    minutesVeryActive_F = jsonify('minutesVeryActive',date)
    activityCalories_F = jsonify('activityCalories',date)
    activity = jsonify('activity',date)
#    trackercalories = jsonify('calories',date,True)
#    trackersteps = jsonify('steps',date,True)
#    trackerdistance = jsonify('distance',date,True)
#    trackerfloors = jsonify('floors',date,True)
#    trackerelevation = jsonify('elevation',date,True)
    
    sl = jsonify_sleep(st,date)
    
   
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
                  e[i]['value'],fa[i]['value'],la[i]['value'],va[i]['value'],sed[i]['value'],crash))
    C = pd.DataFrame(l)
    C.columns = ['Time','Heart','Calories','Steps','Distance','Elevation',
                 'MinutesFairlyActive','MinutesLightlyActive','MinutesVeryActive','MinutesSedentary','Sleep']
    CT  = C.T
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
    C.to_csv('Activity_CSV/'+date+'.csv') 
    st = st + timedelta(days=1)
#    if input("next dates?(Y/N)\n").upper() == 'N':break
os.remove('Data/'+"profile.json")