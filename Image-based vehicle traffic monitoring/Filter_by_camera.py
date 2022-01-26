"""Created on Fri Jul  3 16:30:44 2020
@author: Geovani BM
"""

import requests
import datetime
import dropbox
import sys
import os 
import csv
import pandas as pd

def uploadToDropbox(): 
    #Generate you access token with OAuth guide from dropbox developers documentation
    dbx = dropbox.Dropbox('your.token.here') 
    rootdir = '/home/p3rplex/Desktop/TrafficMonitoring' #Local path
    print ("Attempting to upload...")
    # walk return first the current folder that it walk, then tuples of dirs and files not "subdir, dirs, files"
    for dir, dirs, files in os.walk(rootdir):
        for file in files:
            try:
                file_path = os.path.join(dir, file)
                dest_path = os.path.join('/', file) #root folder of dropbox app
                print('Uploading %s to %s' % (file_path, dest_path))
                with open(file_path, "br") as f:
                    dbx.files_upload(f.read(), dest_path, mute=True)
                print("Finished upload.")
            except Exception as err:
                print("Failed to upload %s\n%s" % (file, err))

def getURLS(date_format):
    global times
    image=[]
    time =[]
    for i in range(len(date_format)):
        #Adjust timestamps to correct url format
        url_date = date_format[i].replace('/','-') 
        endpoint = "https://api.data.gov.sg/v1/transport/traffic-images?date_time="+url_date
        data = requests.get(endpoint)
        if (data):
            #if response status 200
            data = requests.get(endpoint).json()    
            for item in data['items']:
                for cam in item['cameras']:
                    camera_id = cam['camera_id']
                    if camera_id == req_camera_id:	
                        image = cam['image']
                        wanted_cam.append(camera_id)
                        wanted_url.append(image)
                        time.append(cam['timestamp'])
                        print(times[i])
    df = pd.DataFrame(list(zip(wanted_cam, wanted_url,times)), 
                   columns =['Cam_id', 'Image','Timestamp_sg_time'])
    df.set_index('Cam_id', inplace=True) 
    df.to_csv('/home/p3rplex/Desktop/TrafficMonitoring/Wed1-20-20.csv', sep=',', encoding='utf-8')
    
if __name__ == "__main__":
    req_camera_id = '1701' #Filtrate by specific camera    
    string_date_list = []  #list of timestamps

    #Generate timestamps every delta minutes, initial_time, final_time and 
    #delta parameters can be modified
    initial_time = datetime.datetime(2020, 1, 20, 0, 0)
    final_time = datetime.datetime(2020, 1, 21, 0, 0)
    delta = datetime.timedelta(minutes=60) 
    times = []
    wanted_url=[]
    wanted_cam=[]
    endpoints =[]
    data_lists =[]
    
    while initial_time < final_time:
        times.append(initial_time)
        initial_time += delta
     
     #Convert datetime objects to string list  
    for i in range(len(times)):   
        string_date_list.append((times[i].strftime('%Y/%m/%dT%H:%M:%S')))
    getURLS(string_date_list)
    uploadToDropbox()
            