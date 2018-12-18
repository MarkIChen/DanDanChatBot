# DanDanChatBot
A ordering system with chat bot by FB messenger
因為丹丹點餐很沒效率 所以希望做一個Bot幫他們提升點餐速度


## How to interact DanDan ChatBot
輸入任何字元喚醒 chatbot 

在迎賓模式(user)時 可以使用以下功能:

|字串中含有以下單字                        |進入state      |可進行動作                   |
|---------------------------------------|--------------|----------------------------|
|`'order''點餐'`                         |`order`       |可以輸入想要的套餐號碼         |
|`'recommend''推薦'`                     |`recommend`   |可以輸入目前的心情            |
|`'location''nearest''位置''地點''最近'`  |`location`    |可以依據目前的位置找出最近的丹丹 |
|`'website''information''網站''資訊'`    |`website`     |可以提供丹丹的資訊網站          |

***
以下將解說不同state的功能

###Order
在order模式下,bot會傳一個份菜單,使用者可以進行點餐
回傳的字串中含有數字1~12，bot會進行下單
完成選取號碼之後，如果是5或9號餐，Bot會詢問雞腿堡口味
若是其他餐點會詢問飲料口味

###check_out
完成一個套餐的訂購後，Bot 會詢問是否追加訂單
使用者點完所有餐點後，Bot會列出所有訂單

###location
訂位服務
進入定位服務後，Bot會請使用者回傳位置
回傳後，Bot會依據經緯度座標尋找最靠近的丹丹(可參考location_service.py)
找到店家資訊後，回傳地址及Google地圖網址

###Recommend 點餐推薦系統
如果使用者不知道要吃什麼可以使用此系統
借助Facebook nlp自然語言處理
如果使用者回傳的訊息被判定為negative，則系統會在6~10之間任選一套餐，安慰使用者
如果使用者回傳的訊息被判定為positive，則系統會在1~5之間任選一套餐，一起慶祝
使用者若不滿意此餐點，可以要求重點

***
## NLP application
除了recommend 模式會使用到nlp處理，其他如果使用者打Bot無法處理的文字都會丟到nlp 中解讀

例如：
    使用者如果在選擇漢堡口味或飲料時，表現出負面情緒，系統猜測使用者懶得詳細指定
    此時，Bot會代替使用者決定漢堡和飲料口味
