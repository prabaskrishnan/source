## Longitudinal Patient Data Interview Question



The steps to run the program.

1. Please use python3
2. The following setup parameters can be controlled at the beginning of the python file lumiata.py
These could also be written to a setup config file


#Initialization and Setup for the program, bring in as many variable config here
ICD = {'9': 'http://hl7.org/fhir/sid/icd-9-cm', '10' : 'http://hl7.org/fhir/sid/icd-10'}
file_events = 'events.psv' # full file path required if the files are not in the current folder
file_demo = 'demo.psv'
delimiter = '|'
header=True

3. Run the command python3 lumiata.py
(Please make sure python3 is in the appropriate path)

4. Joss files for each valid patient will be in the sons folder with the patient_id as the file name


