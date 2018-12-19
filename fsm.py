from transitions.extensions import GraphMachine

from utils import *

class TocMachine(GraphMachine):
    num_order=0
    meal_set=0
    hamburger_taste=0
    drink_taste=0
    all_meal=[]
    all_hamburger_taste=[]
    all_drink_taste=[]

    def __init__(self, **machine_configs):
        
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )

    def is_going_to_order(self, event):
        if event.get("message"):
            text = event['message']['text']
            if(text.lower() == 'order' or text == "點餐"):
                return True
            else:
                sender_id = event['sender']['id']
                print(send_text_message(sender_id, "抱歉 看不懂誒！你可以叫我點餐 英文馬ㄟ通") )
                return False
        else:
            return False

    def is_going_to_mood(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'mood'
        return False
    def is_going_to_taste(self, event):
        if(self.meal_set==5 or self.meal_set==9):
            return True
        return False

    def is_going_to_choose_drink(self, event):
        if(self.meal_set!=5 and self.meal_set!=9):
            return True
        elif(self.state=="taste" and self.hamburger_taste!=0):
            return True
        elif(self.state=="taste" and self.hamburger_taste==0):
            sender_id = event['sender']['id']
            print(send_text_message(sender_id, "哎呀！你忘了選漢堡口味了") )
            self.to_taste(event)
            return False
        else:
            return False
        
    def is_going_to_restart(self, event):
        if event.get("message"):
            text = event['message']['text']
            if(text.lower() == 'restart'):
                print('restart ordering system...')
                sender_id = event['sender']['id']
                print(send_text_message(sender_id, "Let's try again.") )
                self.meal_set=0
                self.hamburger_taste=0
                self.num_order=0
                return True
        return False
    def is_going_to_choose_set(self, event):
        if event.get("message"):
            self.meal_set=0
            text = event['message']['text']
            print('setting set')

            for i in range(1,13):
                p=13-i
                # print(p)
                if(str(p) in text):
                    self.meal_set=p
                    return True
                
            print('Unvalid input')
            sender_id = event['sender']['id']
            print(send_text_message(sender_id, "Sorry~ We do not have this set. Ex:9 set") )
            self.to_order(event)
            return False
        return False

    def is_going_to_checkout(self, event):
        print("trying to checkout")
        if(self.drink_taste!=0):
            return True
        else:       #think if the information is not complete
            sender_id = event['sender']['id']
            send_text_message(sender_id, "客官～別跟我開玩笑了！")
            self.to_drink(event)
            return False
        
    

    def on_enter_order(self, event):
        print("I'm entering order")
        self.meal_set=0
        self.hamburger_taste=0
        self.drink_taste=0

        sender_id = event['sender']['id']
        print(send_text_message(sender_id, "今天想要幾號餐？") )
        print(send_image_url(sender_id, "https://pic.pimg.tw/mokrt/1334379038-4159491170_n.jpg"))
       

        # self.restart()
    def on_enter_mood(self, event):
        print("I'm entering mood")

        sender_id = event['sender']['id']
        send_text_message(sender_id, "I'm entering mood")
    def on_enter_website(self, event):
        print("I'm entering website")

        sender_id = event['sender']['id']
        send_text_message(sender_id, "什麼！！你不知道丹丹嗎？？下面是我們的介紹")
        send_text_message(sender_id, "https://zh.wikipedia.org/wiki/丹丹漢堡")
        send_text_message(event['sender']['id'], "謝謝使用本服務！")
        self.to_user(event)
               

    def on_enter_recommend(self, event):
        print("I'm entering recommend")
        sender_id = event['sender']['id']
        send_text_message(sender_id, "歡迎使用點餐推薦系統\n今天過得如何呢？")

    def on_enter_user(self, event):
        print("Begin Serving")
        self.num_order=0
        self.meal_set=0
        self.hamburger_taste=0
        self.drink_taste=0
        self.all_meal=[]
        self.all_hamburger_taste=[]
        self.all_drink_taste=[]
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "Welcome to 丹丹.\nWhat can I help you?") 
        send_text_message(sender_id, "I provide order and location service.\nPlease type order or location or website.\nI can also recommend meal for you.")

    def on_enter_choose_set(self, event):
        print("Customer is choosing set")

        sender_id = event['sender']['id']
        send_text_message(sender_id, "Congratulation! You have chosen "+str(self.meal_set)+" set.") 
        self.advance(event)

    def on_enter_taste(self, event):
        print("I'm entering taste")
        sender_id = event['sender']['id']
        send_button_message_taste(sender_id,"原味","辣味")

    def on_enter_drink(self, event):
        print("I'm entering drink")
        sender_id = event['sender']['id']
        send_button_message_drink(sender_id)
        
    def on_enter_checkout(self, event):
        print("I'm entering checkout")

        if(self.drink_taste!=0):
            self.num_order +=1 
            print("current order number: "+str(self.num_order))
            self.all_meal.append(self.meal_set)
            self.all_drink_taste.append(self.drink_taste)
            self.all_hamburger_taste.append(self.hamburger_taste)

            sender_id = event['sender']['id']
            send_text_message(sender_id, "The following is your order:\nTotal: "+str(self.num_order))

            for index in range(self.num_order):
                print("try to display")
                sender_id = event['sender']['id']
                send_text_message(sender_id,"訂單："+str(index+1)+"\n\n套餐："+str(self.all_meal[index])+"\n飲料："+str(self.all_drink_taste[index]))

            sender_id = event['sender']['id']
            send_button_message_addorder(sender_id)

        else:
            sender_id = event['sender']['id']
            send_text_message(sender_id, "抱歉～我眼殘可以幫我重點嗎")
            self.on_enter_order

    def on_enter_final_check(self, event):
        print("I'm entering final_check")
        sender_id = event['sender']['id']
        send_text_message(sender_id, "Thanks!The following is all your order:\nTotal: "+str(self.num_order))

        for index in range(self.num_order):
            print("try to display")
            sender_id = event['sender']['id']
            send_text_message(sender_id,"訂單："+str(index+1)+"\n\n套餐："+str(self.all_meal[index])+"\n飲料："+str(self.all_drink_taste[index]))


        send_button_message_localtion_service(sender_id)

    def on_enter_location(self, event):
        print("I'm entering location")
        sender_id = event['sender']['id']
        send_button_message_localtion_request(sender_id)

    def on_exit_order(self,event):
        print('Leaving order')

    def on_exit_mood(self,event):
        print('Leaving mood')

    def set_hamburger_taste(self, i,event):
        
        if(i=="原味"):
            self.hamburger_taste="原味"
            print("hamburger_taste: "+self.hamburger_taste)
            self.advance(event)
        elif(i=="辣味"):
            self.hamburger_taste="辣味"
            print("hamburger_taste: "+self.hamburger_taste)
            self.advance(event)
        else:
            print("error: 1234")
    def set_drink(self, i,event):
    
        if(i=="檸檬紅茶"):
            self.drink_taste="檸檬紅茶"
            print("drink_taste: "+self.drink_taste)
            self.advance(event)
            
        elif(i=="可樂"):
            self.drink_taste="可樂"
            print("drink_taste: "+self.drink_taste)
            self.advance(event)
        elif(i=="雪碧"):
            self.drink_taste="雪碧"
            print("drink_taste: "+self.drink_taste)
            self.advance(event)
        else:
            print("error: 5678")
    
 
    def another_order(self, i,event):
        sender_id = event['sender']['id']
        
        if(i=="Yes"):
            send_text_message(sender_id, "OK!! Please order your next meal.")
            self.to_order(event)
        elif(i=="No"):      #not finish : next step to final check 0ut 
            self.checkout(event)
        else:
            print("error: 0987")

    def localtion_service(self,i,event):
        sender_id = event['sender']['id']
        
        if(i=="Yes"):
            send_text_message(sender_id, "OK!! Please help me press the botton to send the location.")
            if(self.state == 'final_check'):
                self.to_location(event)
        elif(i=="No"):      #not finish : next step to final check 0ut 
            send_text_message(sender_id, "謝謝使用本服務！")
            self.to_user(event)
            
        else:
            print("error: 0908")

    def recommend_service(self,i,event):
        sender_id = event['sender']['id']
        
        if(i=="Yes"):
            send_text_message(sender_id, "OK!! 請幫我挑選飲料")
            if(self.state == 'recommend'):
                self.to_drink(event)
        elif(i=="No"):      #not finish : next step to final check 0ut 
            send_text_message(sender_id, "真是難以捉摸啊～～\nHow are you today~")
          
            
        else:
            print("error: 0908")