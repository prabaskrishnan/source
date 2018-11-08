#Longitudinal Patient Data Interview Question
#Author: Praba Santhanakrishnan
#Date: Nov 8 2018

from datetime import datetime
import json # for better viewing inside writtein output file purpose only
import sys


#Initialization and Setup for the program, bring in as many variable config here
ICD = {'9': 'http://hl7.org/fhir/sid/icd-9-cm', '10' : 'http://hl7.org/fhir/sid/icd-10'}
file_events = 'events.psv' # full file path required if the files are not in the current folder
file_demo = 'demo.psv'
delimiter = '|'
header=True


# Custom file parser without using any of the python packages
def fileParser(fileName,delimiter, numCols):

    lstObject = []
    try:
        fileHandle =  open(fileName, 'r')
    except IOError:
        print('There was an error opening the file!')
        sys.exit()

    for line in fileHandle:
        fields = line.split(delimiter)
        fields[numCols-1] = fields[numCols-1].strip('\n')
        lstObject.append(fields)
    fileHandle.close()

    return lstObject

# Function to calculate the difference in days (returns 1 day if only one event found for the patient)
def calc_time(date1 , date2,period ):
    if period =='days':
        time = (date2-date1).days
    elif period =='years':
        time = int((date2-date1).days/365)
    if time==0: time=1
    return time

# To find the median for a given list
def median(lst):
    sortedList = sorted(lst)
    listLen = len(lst)
    index = (listLen - 1) // 2
    if (listLen % 2):
        return int(sortedList[index])
    else:
        return int((sortedList[index] + sortedList[index + 1])/2.0)


#def


#Parse the files into lists , using the basic data structures instead of advanced numpy , pandas objects

lstEvents = fileParser(file_events, delimiter, 4)
lstEvents_header = lstEvents[0:1]
if header: lstEvents  = lstEvents[1:]


lstDemos = fileParser(file_demo, delimiter, 3)
lstDemos_header = lstDemos[0:1]
if header: lstDemos  = lstDemos[1:]

#Check the index of the columns , so that if the order changes in the future , our program would still run
#Example for adaptation to the changes in the future
# IF the column names change , need to update this block only or the new column need to be added

index_patient_id = lstDemos_header[0].index('patient_id')
index_birth_date = lstDemos_header[0].index('birth_date')
index_gender = lstDemos_header[0].index('gender')
index_event_date = lstEvents_header[0].index('date')
index_system = lstEvents_header[0].index('icd_version')
index_code = lstEvents_header[0].index('icd_code')




# Construct the overall patients json(dictionary)  and also write to a seperate file for each patient
dict_patients = {}
for patient in lstDemos:
    lst_patient_events = [event for event in lstEvents if event[index_patient_id] == patient[index_patient_id]]
    if len(lst_patient_events) > 0: # Create patient data only if there are any associated with that patient

        events_json = {patient[index_patient_id]:{'date': item[index_event_date],\
                       'system' : ICD[item[index_system]]\
                        ,'code' : item[index_code]\
                       } for item in lst_patient_events}

        for k,v in events_json.items():          # To include code tag only if the code exists
            if not v['code'].split(): events_json[k] = {'date': v['date'],'system' : v['system']}
        patient_json = {'birth_date' : patient[index_birth_date],\
                                 'gender' : patient[index_gender],\
                                 'events' : [events_json[patient[index_patient_id]]]}

        dict_patients[patient[index_patient_id]] = patient_json

        try:

            with open('jsons/' +patient[index_patient_id] + '.json', 'w') as file:
                file.write(json.dumps( patient_json, indent=4))
            file.close()
        except IOError:
            print('There was an error writing to the file!')




# Now that we have the master joint json(dictionary) for all the patients  , we can do all sorts of analysis on this.

print('\n')
print('Total Number of valid Patients: ' , len(dict_patients))
print('Count of Females: ', len({k : v for k,v in dict_patients.items() if v[lstDemos_header[0][index_gender]] == 'F'}))
print('Count of Males: ', len({k : v for k,v in dict_patients.items() if v[lstDemos_header[0][index_gender]] == 'M'}))



# Extract only the event dates for each patient from the built json for the patients
# Create a dictionay in the format {patient_id: [birth_date,first_event_date,last_event_Date]}

dict_events = {k:[v['birth_date'], v['events']] for k,v in dict_patients.items()}
dict_date = {}

for k,v in dict_events.items():
    list_dates = []

    for item in v[1]:
        list_dates.append(datetime.strptime(item['date'], '%Y-%m-%d'))
    first_event_date = min(list_dates)
    last_event_date = max(list_dates)
    dict_date[k] = [datetime.strptime(v[0], '%Y-%m-%d'),first_event_date,last_event_date]



list_no_of_days = [calc_time(v[1],v[2],'days') for k,v in dict_date.items()]
list_age =  [calc_time(v[0],v[2],'years') for k,v in dict_date.items()]

print('\n')
print('Minimum length of patient timeline in days: ', min(list_no_of_days))
print('Maximum length of patient timeline in days: ', max(list_no_of_days))
print('Median length of patient timeline in days: ', median(list_no_of_days))
print('\n')
print('Minimum age of patient timeline in years: ', min(list_age))
print('Maximum age of patient timeline in years: ', max(list_age))
print('Median age of patient timeline in years: ', median(list_age))


#dict_patients = json.dumps(dict_patients ,indent=1)  # for better viewing
#print(dict_patients)
