import json
def push_message(req:dict,messages) :
    UserID = req['events'][0]['source']['userId']
    Push_URL = 'https://api.line.me/v2/bot/message/push'
    
    data = {
        "to": UserID, 
    }

    data['messages'] = messages
    
    payload = {
        "data" : data,
        "api_url" : Push_URL
    }

    return payload

def sentMessage(messages) :
    
    text = messages
    objMsg = {
             "type":"text",
             "text":  text
             }
    
    return objMsg

def sentLocation(title,address,latitude,longitude) :
    
    objMsg = {
        "type":"location",
        "title": title,
        "address": address,
        "latitude": latitude,
        "longitude": longitude
    }
    
    return objMsg

def sentFlexMessage(flexObj):

    objMsg = {
        "type": "flex",
        "altText": "this is a flex message",
        "contents":json.loads(flexObj)
    }
    return objMsg