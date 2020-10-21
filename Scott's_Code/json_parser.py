# -*- coding: utf-8 -*-
"""
Author: Scott Miller
PhD Candidate at Florida State University
Advisor: Andrew Rassweiler

This script was written for NSF project, "CNH-L: Multiscale Dynamics of Coral Reef Fisheries: Feedbacks Between Fishing Practices, Livelihood Strategies, and Shifting Dominance of Coral and Algae" (Award #1714704).

This script takes the exported JSON file from the previous scripts and converts the data to a .csv file in a similar (although not identical) format
as that generated by the web version of CoralNet.  This is analogous to the "annotation" export, not the percent covers export.  Note: this will return errors
if errors remain in the JSON from coralnet_api_deployer.py, so make sure you run json_error_checker.py until it tells you there are no errors.
"""

#Imports necessary libraries
import json
import pandas as pd
import re

#Define variables to easily locate the exported JSON from previous steps
site_to_use = ''
local_path = ''
image_extension = '' #The file extension on your images you uploaded.  In our case, we use GoPro JPEG's, so we use "JPG"

#Loads the json file
f = open(f"{local_path}{site_to_use}_export.json",)

#Converts the json file into a dictionary and extracts the value from the only key
dat = json.load(f)
d = dat['data']

#Creates an empty dictionary used to store the relevant information
dic = {}
n = 1
#Nested loop to extract information from the json dictionary
for i in range(len(d)): #loops over the images in the file
   
    #Extracts information at the image level
    img_id = d[i]['id'] #Pulls out the image url
    attrib = d[i]['attributes'] #Pulls out the attributes dictionary
    img_points = attrib['points'] #Pulls out the information for each point
    
    for j in range(len(img_points)): #Loops over the points on each image
    
        temp_class = img_points[j]['classifications'] #Pulls out the information on classifications for each point (each point has 5 suggestions)
        
        #Creates an empty list used in the next loop (want it overwritten each time)
        temp_lab = []
        temp_conf = []
        
        for k in range(len(temp_class)): #Loops over the five machine suggestions
            temp_lab.append(temp_class[k]['label_code'])
            temp_conf.append(temp_class[k]['score'])

        #Now it takes the relevant information and appends it to the output dictionary.  A dictionay is used in this step for efficiency purposes.
        dic[f'row_{n}'] = [re.search(f'^.*[/](.*[.{image_extension}])', img_id).group(1), img_id, j+1, 
                                img_points[j]['column'], img_points[j]['row'],
                                temp_lab[0], temp_conf[0], 
                                temp_lab[1], temp_conf[1],
                                temp_lab[2], temp_conf[2],
                                temp_lab[3], temp_conf[3],
                                temp_lab[4], temp_conf[4]]
        n += 1
        
output = pd.DataFrame.from_dict(dic, orient = 'index') #Converts the dictionary to a dataframe
output.columns = ['img_name','img_url','point','column','row',
                                 'machine_suggestion1','confidence1',
                                 'machine_suggestion2','confidence2',
                                 'machine_suggestion3','confidence3',
                                 'machine_suggestion4','confidence4',
                                 'machine_suggestion5','confidence5']
#Outputs the csv
output.to_csv(f'{local_path}{site_to_use}.csv', index=False)
