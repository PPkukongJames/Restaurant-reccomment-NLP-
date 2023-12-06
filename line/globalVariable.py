from package import *

def remove_special_characters(text):
    # ใช้ regular expression เพื่อลบสัญลักษณะที่ไม่ใช่ตัวอักษร
    cleaned_text = re.sub(r'[^a-zA-Z0-9ก-๙\s]', '', text)
    cleaned_text = re.sub(r'[&\'(),]', '', cleaned_text)
    return cleaned_text

def lemmatize_tokenize(text):#สำหรับทำ lemmatize และ tokenize
    words = remove_special_characters(text)
    words = word_tokenize(words)
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return lemmatized_words

lemmatizer = WordNetLemmatizer()
business = pd.read_excel('processing_data.xlsx')
city_tf_idf = TfidfVectorizer(
    tokenizer=lemmatize_tokenize,
    vocabulary=pickle.load(open("models/city_tf_idf.pkl", "rb"))
)
state_tf_idf = TfidfVectorizer(
    tokenizer=lemmatize_tokenize,
    vocabulary=pickle.load(open("models/state_tf_idf.pkl", "rb"))
)
name_tf_idf = TfidfVectorizer(
    tokenizer=lemmatize_tokenize,
    vocabulary=pickle.load(open("models/name_tf_idf.pkl", "rb"))
)
categories_tf_idf = TfidfVectorizer(
    tokenizer=lemmatize_tokenize,
    vocabulary=pickle.load(open("models/categories_tf_idf.pkl", "rb"))
)
categories_features = categories_tf_idf.fit_transform(business['categories']).toarray()
name_features = name_tf_idf.fit_transform(business['name']).toarray()
state_features = state_tf_idf.fit_transform(business['state']).toarray()
city_features = city_tf_idf.fit_transform(business['city']).toarray()
category_list = list(categories_tf_idf.get_feature_names_out())
user_preference = pd.DataFrame(columns = ['user']+category_list,data = [ ['test']+list(np.zeros(len(category_list)))])
columns_print =['name','address','city','state','review_count','stars','categories']
day =  ['Monday','Tuesday', 'Wednesday', 'Thursday',  'Friday','Saturday', 'Sunday']
day_dic = {
    'Monday':[],
    'Tuesday':[], 
    'Wednesday':[], 
    'Thursday':[], 
    'Friday':[], 
    'Saturday':[], 
    'Sunday':[]
}
time = '''{
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "<day>",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1,
                "contents": []
              },
              {
                "type": "text",
                "text": "<time>",
                "flex": 3
              }
            ]
          }'''

text ='''{
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "<name>",
        "weight": "bold",
        "size": "xl"
      },
      {
        "type": "box",
        "layout": "baseline",
        "margin": "md",
        "contents": [
          {
            "type": "text",
            "text": "<stars>",
            "size": "xl",
            "color": "#e3bb1c",
            "margin": "md",
            "flex": 0
          }
        ]
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "Place",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "<address> <city> <state>",
                "wrap": true,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "contents": [
              {
                "type": "text",
                "text": "Categories",
                "color": "#aaaaaa",
                "size": "sm"
              },
              {
                "type": "text",
                "text": "<categories>",
                "flex": 2
              }
            ],
            "spacing": "sm"
          },
          <time>
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "Review",
          "text": "Review:<name>"
        }
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [],
        "margin": "sm"
      }
    ],
    "flex": 0
  }
}
'''
PATH_KEY = 'key.json'
with open(PATH_KEY, 'r') as file:
    key = json.load(file)
HEADERS = {
    'Content-Type':'application/json; charset=UTF-8',
    'Authorization': 'Bearer ' + key['Channel_Access_Token']
}