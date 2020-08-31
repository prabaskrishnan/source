import flask
from flask import request, jsonify, send_file
import requests

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['JSON_SORT_KEYS'] = False

@app.route('/api/v3/scancards', methods=['GET'])

def main():

    if 'image' in request.args:
        image_url = 'https://insuranceocr.blob.core.windows.net/ocrimages/' + request.args['image']
    else:
        return "Error: No image URL field provided. Please specify an image URL."
    #image_url = "https://insuranceocr.blob.core.windows.net/ocrimages/praba.jpg"

    

    #image_url = "https://insuranceocr.blob.core.windows.net/ocrimages/praba.jpg"
    endpoint='https://majorboost.cognitiveservices.azure.com/'
    subscription_key='081ffceb2d114857bdc8dbcf78c3cbbe'
    text_recognition_url = endpoint + "/vision/v3.0/read/analyze"

    subscriber_fname =""
    subscriber_lname =""
    subscriber_id="" 
    group_id="" 
    provider_name=""
    provider_contact=""
    bin_number=""
    health_plan=""
    rx_group = ""

    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    data = {'url': image_url}
    response = requests.post(
        text_recognition_url, headers=headers, json=data)
    response.raise_for_status()

    operation_url = response.headers["Operation-Location"]

    analysis = {}

    poll = True
    while (poll):
        response_final = requests.get(
            response.headers["Operation-Location"], headers=headers)
        analysis = response_final.json()
        

        if ("analyzeResult" in analysis):
            poll = False
        if ("status" in analysis and analysis['status'] == 'failed'):
            poll = False
            

    if analysis['status'] != 'succeeded':
        print("Please scan again")


        
    def find_provider():
        list_provider = ['PREMERA', 'Aetna']
        
        
        for provider in list_provider:
            if any(provider in s for s in sorted_ylabels):
                return provider
        
        
    def find_plan():
        list_plan = ['PPO', 'POS', 'HMO']
        
        for plan in list_plan:
            if plan in sorted_ylabels:
                return plan
            

    def find_nextkey(currentkey):
        '''Helper function to get the next key in the output list dictionary'''
        temp = list(word_list) 
        try: 
            nextkey = temp[temp.index(currentkey) + 1] 
        except (ValueError, IndexError): 
            nextkey = None
        return nextkey   

        
        
    def find_group():
        list_group = ['Group', 'Group#', 'Group #']
        
        for group in list_group:
            if group in word_list.keys():return find_nextkey(group)
                

    def find_bin():
        list_bin = ['BIN', 'BIN#', 'BIN #']
        
        for bin_no in list_bin:
            if bin_no in word_list.keys():return find_nextkey(bin_no)

    def find_rx():
        list_rx = ['Rx', 'Rx#', 'Rx #']
        
        for rx in list_rx:
            if rx in word_list.keys():return find_nextkey(rx)

            
            
            
    def find_next_listitem(list_item):
        #print(list_item)
        for item in list_item:
         #   print(item)
            while True:
                try:
                    return sorted_xlabels[sorted_xlabels.index(item)+1] 
                    break
                except ValueError:break


            
    def find_name():
        list_name = ['Member', 'Name', 'Member Name']
        return find_next_listitem(list_name)

            
    def find_Id():
        list_Id = ['Id', 'Identification', 'Identification#','Id#', 'ID','ID#']
        return find_next_listitem(list_Id)

    def find_lname(name):
        while True:
            try:
                return sorted_ylabels[sorted_ylabels.index(name)+1] 
                break
            except ValueError:break

                
    def centroid(vertexes):
        #print(vertexes)
        _x_list = [vertex [0] for vertex in vertexes]
        _y_list = [vertex [1] for vertex in vertexes]
        _len = len(vertexes)
        _x = sum(_x_list) / _len
        _y = sum(_y_list) / _len
        return(_x, _y)
                

        



    card_width = analysis['analyzeResult']['readResults'][0]['width']
    card_height = analysis['analyzeResult']['readResults'][0]['height']
    word_list = {}
    for line in analysis['analyzeResult']['readResults'][0]['lines']:
        
        for word in line['words']:
            word_list[word['text']] =  ((word['boundingBox'][0],word['boundingBox'][1]), (word['boundingBox'][2],word['boundingBox'][3]),(word['boundingBox'][4],word['boundingBox'][5]),(word['boundingBox'][6],word['boundingBox'][7]))
        
            
    word_list = {k: [{'centroid': centroid(v)},{'co-ordinates': v}] for k, v in word_list.items()}
    sorted_xlist = sorted(word_list.items(), key=lambda x:x[1][1]['co-ordinates'][0][0])
    sorted_xlabels = [label[0] for label in sorted_xlist]
    sorted_ylabels = list(word_list.keys())


    provider_name=find_provider()
    #provider_name = 'Aetna'
    print('Provider Name: ',provider_name)

    if  provider_name.find('PREMERA') == -1:
        sorted_xlabels = sorted_ylabels
        
    subscriber_fname = find_name()
    subscriber_id = find_Id()
        

    health_plan  =find_plan()
    group_id = find_group()
    bin_number = find_bin()
    rx_group = find_rx()
    subscriber_fname = find_name()
    subscriber_lname =  find_lname(subscriber_fname)
    subscriber_id = find_Id()

    output =    {"Status":"Success",\
     "Subscriber First Name": subscriber_fname,\
     "Subscriber Last Name": subscriber_lname,\
     "Subscriber Id": subscriber_id,\
     "Provider Name": provider_name,\
     "Rx Bin#": bin_number,\
     "Health Plan":health_plan,\
     "Rx Group": rx_group}

    return  jsonify(output)
app.run()