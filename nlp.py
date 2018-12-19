from fsm import TocMachine
from utils import *
from fsm import TocMachine
import random

def nlp_introducing(nlp,event,machine):
    sender_id = event['sender']['id']
    if(machine.state=="recommend"):
        if('sentiment' in  nlp['entities']):
            if(nlp['entities']['sentiment'][0]['confidence'] > 0.5):
                if(nlp['entities']['sentiment'][0]['value'] =="positive"):
                    temp=random.randint(1,5)
                    send_text_message(sender_id, "Wow!! It semms that you have a nice day.\n Well...Let's me see.\n How about a "+str(temp)+" set?")
                    send_button_message_recommend(str(temp),sender_id)
                    machine.meal_set=temp
                    return True
                    # send_text_message(sender_id, "I am glad you are happy")
                elif(nlp['entities']['sentiment'][0]['value'] =="negative"):
                    temp=random.randint(6,10)
                    send_text_message(sender_id, "I'm sorry! Well...How about a "+str(temp)+" set, because chicken make you happier.")
                    send_button_message_recommend(str(temp),sender_id)
                    machine.meal_set=temp
                    return False
                else:
                    temp=random.randint(1,10)
                    send_text_message(sender_id, "哇～這好哲學喔！我只是個賣漢堡的，不然"+str(temp)+"號餐如何")
                    send_button_message_recommend(str(temp),sender_id)
                    machine.meal_set=temp
                    return False
        else:
            temp=random.randint(1,10)
            send_text_message(sender_id, "哇～這好哲學喔！我只是個賣漢堡的，不然"+str(temp)+"號餐如何")
            send_button_message_recommend(str(temp),sender_id)
            machine.meal_set=temp
            return False
    if(machine.state=="drink" or machine.state=="taste"):
        if('sentiment' in  nlp['entities']):
            if(nlp['entities']['sentiment'][0]['confidence'] > 0.5):
               
                if(nlp['entities']['sentiment'][0]['value'] =="negative"):
                    send_text_message(sender_id, "別生氣啊～～那我幫你決定好了")
                    machine.drink_taste="檸檬紅茶"
                    machine.hamburger_taste="原味"
                    machine.to_checkout(event)
                    
                    return False

    if(machine.state=="checkout"):
        if('sentiment' in  nlp['entities']):
            if(nlp['entities']['sentiment'][0]['confidence'] > 0.5):
                if(nlp['entities']['sentiment'][0]['value'] =="positive"):
                    send_button_message_addorder(event['sender']['id'])
                    return False
                elif(nlp['entities']['sentiment'][0]['value'] =="negative"):
                    send_text_message(sender_id, "Be patient.")
                    send_button_message_addorder(event['sender']['id'])
                    return False
                else:
                    send_button_message_addorder(event['sender']['id'])
        else:
            send_button_message_addorder(event['sender']['id'])
    if(machine.state=="final_check"):
        if('sentiment' in  nlp['entities']):
            if(nlp['entities']['sentiment'][0]['confidence'] > 0.5):
                if(nlp['entities']['sentiment'][0]['value'] =="positive"):
                    send_text_message(event['sender']['id'], "What???")
                    send_button_message_localtion_service(event['sender']['id'])
                    return False
                elif(nlp['entities']['sentiment'][0]['value'] =="negative"):
                    send_text_message(sender_id, "Be patient.")
                    send_button_message_localtion_service(event['sender']['id'])
                    return False
                else:
                    send_text_message(event['sender']['id'], "What???")
                    send_button_message_localtion_service(event['sender']['id'])
        else:
            send_text_message(event['sender']['id'], "What???")
            send_button_message_localtion_service(event['sender']['id'])
    if(machine.state=="location"):

        send_text_message(event['sender']['id'], "What???")
        send_button_message_localtion_request(event['sender']['id'])


def deal_mood_order(event,machine):
    text = event['message']['text']
    if("Yes" in text):
        machine.recommend_over(event)
    elif("No" in text):
        send_text_message(event['sender']['id'], "Alright~Let's try again")
        machine.to_recommend(event)
        
