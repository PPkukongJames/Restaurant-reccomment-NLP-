from package import *
from globalVariable import *
import line

app = Flask(__name__)

def remove_special_characters(text):
    # ใช้ regular expression เพื่อลบสัญลักษณะที่ไม่ใช่ตัวอักษร
    cleaned_text = re.sub(r'[^a-zA-Z0-9ก-๙\s]', '', text)
    cleaned_text = re.sub(r'[&\'(),]', '', cleaned_text)
    return cleaned_text

def translate_text_mtranslate(text, target_lang='en'):
    translation = translate(text, target_lang)
    return translation

def lemmatize_tokenize(text):#สำหรับทำ lemmatize และ tokenize
    words = remove_special_characters(text)
    words = word_tokenize(words)
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return lemmatized_words

def time_format(time) :
    temp = time.split(':')
    if len(temp[0]) == 1 :
        temp[0] = '0'+temp[0]
    if len(temp[1]) == 1 :
        temp[1] = temp[1]+'0'
    return temp[0]+':'+temp[1]

def cosine_similarity_result (user_query) :
    name_result = cosine_similarity(name_tf_idf.transform([user_query]),name_features)
    city_result = cosine_similarity(city_tf_idf.transform([user_query]),city_features)
    state_result = cosine_similarity(state_tf_idf.transform([user_query]),state_features)
    categories_result = cosine_similarity(categories_tf_idf.transform([user_query]),categories_features)

    result_cosine = name_result[0]+city_result[0]+state_result[0]+categories_result[0]

    return result_cosine

@app.route('/webhook', methods = ['POST']) 
def webhook():
    req = request.json
    print(request.json)
    try :
        if not('message' in list(req['events'][0].keys()) ):
            return Response(response="EVENT RECEIVED",status=200)     
        query = req['events'][0]['message']['text']
        if query[0:7] != 'Review:':
            msg = line.sentMessage("Please wait a moment We are searching for the store you want. It may take about 40 seconds.")
            payload = line.push_message(req,[msg])
            requests.post(payload['api_url'], headers=HEADERS, data=json.dumps(payload['data']))
            
            query = translate_text_mtranslate(query)

            result_business = business.copy()
            result_business['cosine_similarity'] = cosine_similarity_result(query)
            data_sent = result_business[result_business['cosine_similarity']>=1].sort_values(['cosine_similarity'],ascending=False).reset_index(drop=True).copy() #นำมาเรียงและสนใจเฉพาะที่ค่าความใกล้มากกว่าเท่ากับ 1
            for i in range(0,3) :
                temp_text = text
                for column in columns_print :
                    temp_columns = '<'+column+'>'
                    temp_text = temp_text.replace(temp_columns,str(data_sent[column].iloc[i]))

                    #columns_print =['name','address','city','state','review_count','latitude','longitude','stars','categories']
                time_list = []
                for d in day :
                    if data_sent[d].iloc[i] != '-' :
                        time_list.append(time.replace('<day>',d).replace('<time>',data_sent[d].iloc[i]))
                time_result = ','.join([str(i) for i in time_list])
                temp_text = temp_text.replace('<time>',time_result)
                msg = line.sentFlexMessage(temp_text)
                location = line.sentLocation(data_sent['name'].iloc[i],data_sent['address'].iloc[i],float(data_sent['latitude'].iloc[i]),float(data_sent['longitude'].iloc[i]))
                payload = line.push_message(req,[msg,location])
                r = requests.post(payload['api_url'], headers=HEADERS, data=json.dumps(payload['data']))
                print(r.text)
                r.close()
    except :
        payload = line.push_message(req,[line.sentMessage("Process not complete please sent again later.")])
        return Response(response="EVENT RECEIVED",status=200)        
    return Response(response="EVENT RECEIVED",status=200)

if __name__ == '__main__' :
    app.run(host='0.0.0.0', debug=True, port=int(os.environ.get('PORT','8080')))
    