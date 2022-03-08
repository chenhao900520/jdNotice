import os
import json
from flask import Flask, request, render_template, Markup
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def demo():
    if request.method == 'GET':
        return render_template('index.html', input_text = '', res_text = '')
    else:
        ck = request.form.get("ck")
        uid = request.form.get("uid")
       
        
        new_item = {'pt_pin':'123', 'Uid':'234'}
        
        return render_template('index.html', ck = ck, uid = uid)

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