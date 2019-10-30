# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 14:27:11 2019

@author: sidhant
"""


import json
import requests
import os 
refresh_token="GwlWsArfnetu5beJV_riqW-rrsDd9Eh6Nc0X1hWZbHBli"
account_logical_name="sidhaiorqunx"
service_instance_logical_name="sidhantDefa1a3t171503"
process_name_sintel="'singtel_testEnv'"
process_name_spgroup_starhub="'SPgroup_starhub2_testEnv'"
OrganizationUnitId="1327"   
API_jobdetails_spg_starhub="https://platform.uipath.com/"+account_logical_name+"/"+service_instance_logical_name+"/odata/Releases?$filter=%20Name%20eq%20"+ process_name_spgroup_starhub
API_jobdetails_sintel="https://platform.uipath.com/"+account_logical_name+"/"+service_instance_logical_name+"/odata/Releases?$filter=%20Name%20eq%20"+ process_name_sintel
API_jobrun="https://platform.uipath.com/"+account_logical_name+"/"+service_instance_logical_name+"/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs"
#"https://platform.uipath.com/sidhaiorqunx/sidhantDefa1a3t171503/odata/Releases?$filter=%20Name%20eq%20'newtest_testEnv'"
#"https://platform.uipath.com/sidhaiorqunx/sidhantDefa1a3t171503/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs"


def getJobDetails(access_token,API_jobdetails,service_instance_logical_name,OrganizationUnitId):
    job_req=requests.get(API_jobdetails,
                     headers={"Authorization":access_token,"X-UIPATH-TenantName":service_instance_logical_name,"X-UIPATH-OrganizationUnitId":OrganizationUnitId},
                     )
    return job_req

def refreshToken(refresh_token):
    refesh_data={
         "grant_type": "refresh_token",
         "client_id": "5v7PmPJL6FOGu6RB8I1Y4adLBhIwovQN",
         "refresh_token": refresh_token
        }

    refresh_req= requests.post("https://account.uipath.com/oauth/token",
                           headers={"Content-Type":"application/json"},
                           data=json.dumps(refesh_data))
    return refresh_req

def main(arg):
    print(type(arg))
    #print(refresh_req.json()['access_token'])
    refresh_req=refreshToken(refresh_token)
    
    access_token="Bearer "+refresh_req.json()['access_token']
    
#    print(refresh_req.json())
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    job_req_sintel=getJobDetails(access_token,API_jobdetails_sintel,service_instance_logical_name,OrganizationUnitId)
    job_req_strhub_sp=getJobDetails(access_token,API_jobdetails_spg_starhub,service_instance_logical_name,OrganizationUnitId)
    path= dir_path + r"\out.xlsx"
    inputData={"filePath":path}
    inputData2={"filePath":path,"arg":arg}
    
    #print(job_req_sintel.json()['value'][0]['Key'])
    key_sintel=job_req_sintel.json()['value'][0]['Key']
    key_str=job_req_strhub_sp.json()['value'][0]['Key']
    
    jobrun_data_sintel={
            "startInfo": {
        		"ReleaseKey": key_sintel,
        		"RobotIds": [],
        		"JobsCount": 0,
        		"Strategy": "All",
        		"InputArguments": json.dumps(inputData)
            }
            }
    jobrun_data_str={
            "startInfo": {
        		"ReleaseKey": key_str,
        		"RobotIds": [],
        		"JobsCount": 0,
        		"Strategy": "All",
        		"InputArguments": json.dumps(inputData2)
            }
            }
    #  api call for sintel job
    if arg=="1" or arg=="4":
        jobrun_req=requests.post(API_jobrun,
                                 headers={"Authorization":access_token,"X-UIPATH-TenantName":service_instance_logical_name,"X-UIPATH-OrganizationUnitId":OrganizationUnitId,"Content-Type":"application/json"},
                                 data=json.dumps(jobrun_data_sintel))
        
        print(jobrun_req.json())        
        print("")
        print("2nd API call")
    
    print("")
    #    api call for starhub and sp group job
    if arg=="2" or arg=="3" or arg=="4" or arg== "5":
        
        jobrun_req=requests.post(API_jobrun,
                                 headers={"Authorization":access_token,"X-UIPATH-TenantName":service_instance_logical_name,"X-UIPATH-OrganizationUnitId":OrganizationUnitId,"Content-Type":"application/json"},
                                 data=json.dumps(jobrun_data_str))
        print(jobrun_req.json())
        
    return True
        
        
#main(5)        
   



