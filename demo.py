import os
import json
from flask import Flask, request, render_template, Markup
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def demo():
    if request.method == 'GET':
        return render_template('index.html', result_text = '请输入您的CK和UID进行通知绑定')
    else:
        ck = request.form.get("ck")
        uid = request.form.get("uid")
        
        #处理ck
        ckarr = ck.split(';')
        sign = 0
        for i in ckarr:
            if 'pt_pin' in i:
                ck_pt_pin = i.split('=')[1]
                sign = 1
        
        if sign == 0:
            result_text = '您输入的CK存在问题，请查询'
        else:
            filename = os.path.join(os.getcwd(), 'CK_WxPusherUid.json')
            with open(filename) as blog_file:
                data = json.load(blog_file)
                
            ckfile = os.path.join(os.getcwd(), 'config/env.sh')
            with open(ckfile) as ck_file:
                ckstr = ck_file.read()
            if ck_pt_pin in ckstr:
                if ck_pt_pin in json.dumps(data):
                    result_text = '当前CK已被绑定，请不要重复绑定'
                else:
                    num = len(data)
                    item_list = []
                    for item in range(num):
                        pt_pin = data[item]['pt_pin']
                        Uid = data[item]['Uid']
                        item_dict = {'pt_pin':pt_pin, 'Uid':Uid}
                        item_list.append(item_dict)
                    
                    new_item = {'pt_pin':ck_pt_pin, 'Uid':uid}
                    item_list.append(new_item) 
                    
                    json_str = json.dumps(item_list, indent=4)
                    with open(filename, 'w') as json_file:
                        json_file.write(json_str)
                        
                    result_text = '绑定成功！'
            else:
                result_text = '抱歉，您的CK不存在，请重试！'
        
        return render_template('index.html', ck = ck, uid = uid, result_text = result_text)

def formatRes(textList):
    return '<p>' + '</p><p>'.join(textList) + '</p>'

# A sample
def reverseText(text):
    res = []
    filename = os.path.join(os.getcwd(), 'CK_WxPusherUid.json')
    with open(filename) as blog_file:
        data = json.load(blog_file)
    
    num = len(data)
    item_list = []
    for item in range(num):
        pt_pin = data[item]['pt_pin']
        Uid = data[item]['Uid']
        item_dict = {'pt_pin':pt_pin, 'Uid':Uid}
        item_list.append(item_dict)
    
    new_item = {'pt_pin':'123', 'Uid':'234'}
    item_list.append(new_item) 
    
    res.append('Original text: %s' %(item_list))
    res.append('Converted text: %s' %(''.join(reversed(list(text)))))
    return res

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',  port=7000)