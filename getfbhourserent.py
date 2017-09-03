
import requests
import pandas as pd 
from datetime import datetime, timedelta
from dateutil.parser import parse
import time

#在Facebook Graph API Exploer取得token
#Fill in your access token
token = 'Fill in your access token' 

#message id = 464870710346711_816628221837623
#message link = https://www.facebook.com/groups/464870710346711/permalink/816628221837623/

#在Facebook Graph API Exploer取得粉絲專頁的id與名稱，並將其包成字典dic
fanpage = {'464870710346711':'台北租屋、出租專屬社團'} 

#define timestamp in the previous 7 days
PreviousDay = 7;
ts = datetime.today()-timedelta(days=PreviousDay);
print(int(ts.timestamp()));

#reset file
filename = "getfbrent_"+time.strftime("%Y%m%d")+".csv"
f = open(filename, 'w');
f.close()

#建立一個空的list          
information_list = [];

for ele in fanpage:
    print("ele="+ele+"\ntoken="+token);
#     https://graph.facebook.com/v2.10/464870710346711/feed?since=1503832629&format=json&access_token="xxx"&limit=25&until=1504433687

    req = 'https://graph.facebook.com/v2.10/'+ele+'/feed?access_token='+token+'&format=json'+'&since='+str(int(ts.timestamp()));
    print('req='+req);
    res = requests.get(req);
    print(res.json()['paging']['next']);

    count = 1;
    #API最多一次呼叫100筆資料，因此使用while迴圈去翻頁取得所有的資料
    while 'paging' in res.json():    
        for x in res.json()['data']:
            if 'message' in x:
                #print('time='+x['updated_time']+'\n'+'id='+x['id']+'\n'+'msg='+x['message']+'\n');
                ary = x['id'].split('_',1);
                fbmsglink = 'https://www.facebook.com/groups/'+ary[0]+'/permalink/'+ary[1];
                information_list.append([x['id'],x['message'],x['updated_time'],fbmsglink]);
        print('page#'+str(count));
        count += 1;
        
        #最後將list轉換成dataframe，並輸出成csv檔
        #information_df = pd.DataFrame(information_list, columns=['id', 'message', 'updated_time'])
        information_df = pd.DataFrame(information_list, columns=['id', 'message', 'updated_time', 'fbmsglink']) 
        
        information_df.to_csv(filename,  mode='a', index=False) 
        information_list = [];

        if 'next' in res.json()['paging']:
            res = requests.get(res.json()['paging']['next']);
        else:
            print('done');
            break;
