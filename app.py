from bottle import route, run, request, abort, static_file
from transitions.extensions import GraphMachine as Machine
import pygraphviz
import os

from fsm import TocMachine
from locaton_service import find_the_nearest_DanDan
from nlp import  *

# VERIFY_TOKEN = "1234567890987654321"
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
PORT = os.environ['PORT']

machine = TocMachine(
    states=['user','order','taste','choose_set','drink','checkout','final_check','location','recommend','website'],
    transitions=[
        # {'trigger': 'advance','source': 'user','dest': 'order','conditions': 'is_going_to_order'},
        {'trigger': 'start_order','source': 'user','dest': 'order'},
        {'trigger': 'start_recommend','source': 'user','dest': 'recommend'},
        {'trigger': 'start_information','source': 'user','dest': 'website'},
        
       
        {'trigger': 'advance','source': 'order','dest': 'choose_set','conditions': 'is_going_to_choose_set'},
        {'trigger': 'advance','source': 'choose_set','dest': 'taste','conditions': 'is_going_to_taste'},
        
        {'trigger': 'advance','source': ['choose_set','taste'],'dest': 'drink','conditions': 'is_going_to_choose_drink'},
        
        {'trigger': 'advance','source': 'drink','dest': 'checkout','conditions': 'is_going_to_checkout'},
        

        {'trigger': 'checkout','source': 'checkout','dest': 'final_check'},
        {'trigger': 'sned_location','source': 'final_check','dest': 'location'},

        {'trigger': 'recommend_over','source': 'recommend','dest': 'drink'},
   
        
        {'trigger':'restart','source': '*','dest': 'user'},
        {'trigger':'advance','source': '*','dest': 'user','conditions': 'is_going_to_restart'}
    ],
    initial='user',
    auto_transitions=True,
    show_conditions=True,
)


@route("/webhook", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge

    else:
        abort(403)


@route("/webhook", method="POST")
def webhook_handler():
    body = request.json
    print('\nFSM STATE: ' + machine.state)
    print('REQUEST BODY: ')
    print(body)

    event = body['entry'][0]['messaging'][0]

    try:
        if ('quick_reply' in body['entry'][0]['messaging'][0]['message'] ):
            if(machine.state=="taste" and  body['entry'][0]['messaging'][0]['message']['quick_reply']['payload']=="hamburger_taste"):
                machine.set_hamburger_taste(body['entry'][0]['messaging'][0]['message']['text'],event)
            elif(machine.state=="drink" and body['entry'][0]['messaging'][0]['message']['quick_reply']['payload']=="drink_taste"):
                machine.set_drink(body['entry'][0]['messaging'][0]['message']['text'],event)
            elif(machine.state=="checkout" and body['entry'][0]['messaging'][0]['message']['quick_reply']['payload']=="another_order"):
                machine.another_order(body['entry'][0]['messaging'][0]['message']['text'],event)
            elif(machine.state=="final_check" and body['entry'][0]['messaging'][0]['message']['quick_reply']['payload']=="localtion_service"):
                machine.localtion_service(body['entry'][0]['messaging'][0]['message']['text'],event)
            elif(machine.state=="recommend" and body['entry'][0]['messaging'][0]['message']['quick_reply']['payload']=="recommend_order"):
                print("trying to set drink")
                machine.recommend_service(event['message']['text'],event)
                

        elif(machine.state=="location" and'attachments' in body['entry'][0]['messaging'][0]['message'] ):
            if('type' in body['entry'][0]['messaging'][0]['message']['attachments'][0] ):
                if(body['entry'][0]['messaging'][0]['message']['attachments'][0]['type']=='location' ):
                    location_event=body['entry'][0]['messaging'][0]['message']['attachments'][0]['payload']['coordinates']
                    find_the_nearest_DanDan(location_event['lat'],location_event['long'],event)
                    send_text_message(event['sender']['id'], "謝謝使用本服務！")
                    machine.to_user(event)

        elif(body['object'] == "page"  and 'text' in body['entry'][0]['messaging'][0]['message']):
            
            text = event['message']['text']
            if(machine.state == "user"):
                if("order" in  text.lower() or "點餐" in text):
                    print(text.find("點餐"))
                    machine.start_order(event)
                elif("recommend" in text.lower() or "推薦" in text):
                    print('start to recommend')
                    machine.start_recommend(event)
                elif("location" in text.lower() or "nearest" in text.lower() or "位置" in text or "地點" in text or "最近" in text):
                    print('start to location service')
                    machine.to_location(event)
                elif("website" in text.lower() or "information" in text.lower() or "網站" in text or "資訊" in text):
                    print('provide the nearest store website')
                    machine.start_information(event)
                else:
                    machine.to_user(event)
                
            else:
                reasonable = machine.advance(event)  #if it cannot move, it will return False
                if(reasonable==False):     #start nlp
                    nlp_introducing(body['entry'][0]['messaging'][0]['message']['nlp'] ,event,machine)

            return 'OK'

    except Exception as ex:
        print("Facebook 又在亂傳訊息了 error:" +str(ex))


@route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return static_file('fsm.png', root='./', mimetype='image/png')


if __name__ == "__main__":

    # machine.get_graph().draw('my_state_diagram.png', prog='dot')
    
    # run(host="localhost", port=5000, debug=True, reloader=True)

    run(host="0.0.0.0", port= PORT, debug=True, reloader = True)
