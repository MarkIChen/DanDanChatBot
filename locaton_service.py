from utils import *

def find_the_nearest_DanDan(lat, long2,event):
    info={
        0:{'name': '丹丹仁德店','lat':22.970771, 'longi': 120.259675,'address':"台南市仁德區中山路272號",'tel':'06 2491350','url':"https://www.google.com.tw/maps/place/丹丹漢堡+仁德店/@22.9708525,120.2575296,17z/data=!3m1!4b1!4m5!3m4!1s0x346e73ffbe8dd005:0xa6aecb9bbf181f6d!8m2!3d22.9708525!4d120.2597183?hl=zh-TW&authuser=0"},
        1:{'name': '丹丹佳里店','lat':23.158598, 'longi': 120.178632,'address':"台南市佳里區延平路191號",'tel':'06 7230909','url':"https://www.google.com.tw/maps/place/丹丹漢堡-佳里延平店/@23.158633,120.1772545,17.75z/data=!4m12!1m6!3m5!1s0x346e7f4b185b70c1:0x5c6461adca1c6e1c!2z5Li55Li55ryi5aChLeS9s-mHjOW7tuW5s-W6lw!8m2!3d23.158581!4d120.1785255!3m4!1s0x346e7f4b185b70c1:0x5c6461adca1c6e1c!8m2!3d23.158581!4d120.1785255?hl=zh-TW&authuser=0"},
        2:{'name': '丹丹成功店','lat':23.000092, 'longi': 120.200194,'address':"台南市北區成功路380號",'tel':'06 2226848','url':'https://www.google.com.tw/maps/place/丹丹漢堡(成功店)/@23.0000003,120.1999355,18.95z/data=!4m5!3m4!1s0x0:0xf8e499ee591033fa!8m2!3d23.0002052!4d120.2001919?hl=zh-TW&authuser=0'},
        3:{'name': '丹丹安南店','lat':22.970771, 'longi': 120.259675,'address':"台南市安南區海佃路一段215號",'tel':'06 3501172','url':'https://www.google.com.tw/maps/place/丹丹漢堡+安南店/@23.0290883,120.197358,12.41z/data=!4m5!3m4!1s0x346e764d2543c473:0xf2c9eb737028dd84!8m2!3d23.0248582!4d120.1913336?hl=zh-TW&authuser=0'},
        4:{'name': '丹丹安平店','lat':22.999522, 'longi': 120.164778,'address':"台南市安平區安平路97號",'tel':'06 2263861','url':'https://www.google.com.tw/maps/place/丹丹漢堡+安平店/@22.9994616,120.162599,17z/data=!3m1!4b1!4m5!3m4!1s0x346e761b5871ca43:0x21c556b394709c67!8m2!3d22.9994616!4d120.1647877?hl=zh-TW&authuser=0'}
    }
    
    dis=1000
    number=0
    for index in range(len(info)):
        temp=((info[index]['lat']-lat)**2+(info[index]['longi']-long2)**2)**0.5
        if(temp<dis):
            dis=temp
            number=index
    
    
    print(number)
    sender_id = event['sender']['id']
                   
    # for index in range(len(info[0])-1 ):
    #     temp=(( info[index]['lat']-lat)**2+(info[index]['longi']-long2)**2)**0.5
    #     print("index: "+str(index)+"temp"+str(temp))
    #     if(temp<dis):
    #         dis=temp
    #         number=index
    
    # print(number)
    # sender_id = event['sender']['id']
    send_text_message(sender_id, "離您最近的店家是： "+str(info[number]['name'])+"\n地址是： "+str(info[number]['address']))
    send_text_message(sender_id, "以下是Googel 地圖連結：")
    send_text_message(sender_id, info[number]['url'])

    
    return info[number]


