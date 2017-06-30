import nltk
from nltk.corpus import stopwords
import requests
import configparser
import os


def process_json(json, query, typ):
    print("result json-> ", json)

    # get answer result
    result = get_answer(json)
    if len(result) > 0:
        result = "Here's what I have found answer about " + query[:-1] + "! " + result
    else:
        # Definition
	result = get_definition(json)
        if len(result) > 0:
            result = "Here's what I have found definition about " + query[:-1] + "! " + result
        else:
            result = get_abstract(json)
            if len(result) > 0:
                result = "Here's what I have found abstract about " + query[:-1] + "! " + result
            else:
                result = get_text(json)
                if len(result) > 0:
                    result = "Here's what I have found text about " + query[:-1] + "! " + result
                # need test more typ == 'mth'
				#elif typ == 'mth':# mth
                    #result = "Can't evaluate expression."
                else:
                    result = "Sorry! I couldn't find anything around " + query[:-1]

    return result


def get_answer(json):
    try:
        return json['Answer']
    except:
        return ""


def get_definition(json):
    try:
        return json['Definition']
    except:
        return ""


def get_abstract(json):
    try:
        return json['Abstract']
    except:
        return ""


def get_text(json):
    try:
        return json['RelatedTopics'][0]['Text']
    except:
        return ""


def get_weather_info(query):
    for w in ["weather", "Weather", "temperature", "Temperature", "cold", "hot", "humid", "climate"]:
        if w in query:
            query = query.replace(w, "")
            break


    # Get Project Directory and config file path
    project_dir = os.path.dirname(os.path.abspath(__file__))
    config_filepath = os.path.join(project_dir, 'raw', 'keys.config')

    # Read config file
    config = configparser.RawConfigParser()
    config.read(config_filepath)
    print(config.sections())

    # Get Weather API key
    api_key = config.get('APIKeys', 'weather')
    print(api_key)

    #APPID=d9ce01906a466d5b7a74402fba00c9
    # http://api.openweathermap.org/data/2.5/weather?q=London&appid=XXXXX
    url_endpoint = 'http://samples.openweathermap.org/data/2.5/weather'
    param = {'q': query[:-1], 'appid': api_key}
    headers = {'Content-Type': 'application/json'}

    resp = requests.get(url_endpoint, params=param, headers=headers)
    print("resp -> ", resp.json())
    result_json = resp.json()
    temp = result_json['main']['temp']

    try:
        temp -= 273
        temp = round(temp, 1)
    except:
        return ""

    print("temp -> ", temp)

    return "Temperature is " + str(temp) + " degree celsius in " + query


def get_translate_info(query):
    for w in ["translate", "Translate", "translating", "translator", "meaning", "dictionary"]:
        if w in query:
            query = query.replace(w, "")
            break


    # Get Project Directory and config file path
    project_dir = os.path.dirname(os.path.abspath(__file__))
    config_filepath = os.path.join(project_dir, 'raw', 'keys.config')

    # Read config file
    config = configparser.RawConfigParser()
    config.read(config_filepath)
    print(config.sections())

    # Get Weather API key
    api_key = config.get('APIKeys', 'translate')
    print(api_key)

	langpair ='en-US|vi-VN'
	api_user = 'haylamvietnam@gmail.com'
	api_key = '2b8fb652eb85bf13858e'
    # 
    url_endpoint = 'http://api.mymemory.translated.net/get'
    param = {'q': query[:-1], 'key': api_key, 'de': api_user, 'langpair': langpair}
    headers = {'Content-Type': 'application/json'}

    resp = requests.get(url_endpoint, params=param, headers=headers)
    print("resp -> ", resp.json())
    result_json = resp.json()

    translatedText = result_json['responseData']['translatedText']
    
    print("Translate result  -> ", translatedText)

    return "Translate result " + query + " meaning " +  str(translatedText)


# function get web result main
def get_web_result(text, typ):
    is_weather = False
	is_translate = False

    for w in ["weather", "Weather", "temperature", "Temperature", "cold", "hot", "humid", "climate"]:
        if w in text:
            is_weather = True
            break

    for w in ["translate", "Translate", "translating", "translator", "meaning", "dictionary"]:
        if w in text:
            is_translate = True
            break

	# tokenize and remove stop words
    tokenized = nltk.word_tokenize(text)

    stop_words = set(stopwords.words("english"))
    filtered_text = [w for w in tokenized if not w in stop_words]
    print("fitered text -> ", filtered_text)

    #  tag the filtered words
    tags = nltk.pos_tag(filtered_text)
    print("fitered tags -> ", tags)

    allowed_word_types = ["N"]  # ["J", "R", "V", "N", "CD"]

    query = ""
    for w in tags:
        if w[1][0] in allowed_word_types:
            query += w[0] + " "

    result = ''
    if is_weather:
        result = get_weather_info(query)
	elif:
		if is_translate:
			result = get_translate_info(query)

    if len(result) == 0:
        url_endpoint = 'https://www.duckduckgo.com'
        param = {'q': query[:-1], 'format': 'json', 't': 'h', 'ia': 'web'}
        headers = {'Content-Type': 'application/json'}

        resp = requests.get(url_endpoint, params=param, headers=headers)
        print("resp -> ", resp.json())
        result_json = resp.json()

        # process json response from server search api
	result = process_json(result_json, query, typ)
        print("result --> ", result)

    return result
