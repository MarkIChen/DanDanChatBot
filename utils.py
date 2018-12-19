import requests
import os

GRAPH_URL = "https://graph.facebook.com/v2.6"
# ACCESS_TOKEN = "EAADuqvO9TFgBALoNOoGZAWiTucKRcIytg5HnsEoJZCZAuu274MnqePt5CcSZAxaKHcYZBNxtMtQmI6y4PpPZB5srpzYWieIcfYzALPW73eNF8y5E6ktaR97vGiLPD67Jf1mslNqmEYmWBrOYxABn0SFZBBRFFxVnUiihgfTLPyLoAZDZD"
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

def send_text_message(id, text):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {"text": text}
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response



def send_image_url(id, img_url):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message":{
            "attachment":{
                "type":"image", 
                "payload":{
                    "url":img_url, 
                    "is_reusable":True
                }
            }
        }
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response


def send_button_message_taste(id, text1, text2):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message":{
            "text": "雞腿堡原味辣味？",
            "quick_replies":[
                {
                    "content_type":"text",
                    "title":text1,
                    # "image_url":"http://example.com/img/red.png",
                     "payload":"hamburger_taste"
                },
                {
                    "content_type":"text",
                    "title":text2,
                    # "image_url":"http://example.com/img/red.png",
                     "payload":"hamburger_taste"
                }               
               
            ]
        }
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send botton_hamburger: " + response.text)
    return response

def send_button_message_drink(id):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message":{
            "text": "飲料想喝什麼呢？",
            "quick_replies":[
                {
                    "content_type":"text",
                    "title":"檸檬紅茶",
                    # "image_url":"http://example.com/img/red.png",
                     "payload":"drink_taste"
                },
                {
                    "content_type":"text",
                    "title":"可樂",
                    # "image_url":"http://example.com/img/red.png",
                     "payload":"drink_taste"
                },
                {
                    "content_type":"text",
                    "title":"雪碧",
                    # "image_url":"http://example.com/img/red.png",
                     "payload":"drink_taste"
                }               
               
            ]
        }
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send botton_hamburger: " + response.text)
    return response



def send_button_message_addorder(id):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message":{
            "text": "Do you need another order??",
            "quick_replies":[
                {
                    "content_type":"text",
                    "title":"Yes",
                    # "image_url":"http://example.com/img/red.png",
                     "payload":"another_order"
                },
                {
                    "content_type":"text",
                    "title":"No",
                    # "image_url":"http://example.com/img/red.png",
                     "payload":"another_order"
                }
            ]
        }
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send botton_hamburger: " + response.text)
    return response

def send_button_message_localtion_service(id):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message":{
            "text": "Do you want me to send the order to the nearest DanDan restaurant??",
            "quick_replies":[
                {
                    "content_type":"text",
                    "title":"Yes",
                    # "image_url":"http://example.com/img/red.png",
                     "payload":"localtion_service"
                },
                {
                    "content_type":"text",
                    "title":"No",
                    # "image_url":"http://example.com/img/red.png",
                     "payload":"localtion_service"
                }
            ]
        }
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send botton_hamburger: " + response.text)
    return response


def send_button_message_localtion_request(id):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message":{
            "text": "Please press the botton!!",
            "quick_replies":[
                {
                    "content_type":"location"
                }
            ]
        }
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send botton_hamburger: " + response.text)
    return response



def send_button_message_recommend(text,id):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message":{
            "text": "Do you like a "+text+" set for your meal?",
            "quick_replies":[
                {
                    "content_type":"text",
                    "title":"Yes",
                    "payload":"recommend_order"
                },
                {
                    "content_type":"text",
                    "title":"No",
                    "payload":"recommend_order"
                }
            ]
        }
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send botton_hamburger: " + response.text)
    return response
