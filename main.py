
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 16:06:26 2017

@author: mayan
"""

from datetime import datetime, timedelta
import os
os.chdir('C:/Users/mayan/Desktop/Fitbit/Mayank-Fitbit/')
from Requester import DataRetrieve,profiler
from iniHandler import print_data, print_json, ReadCredentials, ReadTokens
from authHandler import *

if __name__ == "__main__":
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
profiler(header_key, header_value)

 
while st <= stx:
    date = st.strftime("%Y-%m-%d")
    st = DataRetrieve(st,date,header_key,header_value)
#    if input("next dates?(Y/N)\n").upper() == 'N':break
os.remove('Data/'+"profile.json")