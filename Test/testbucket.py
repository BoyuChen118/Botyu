
### AMAZON CLIENT TEST BEGINS

# import boto3,os

# client = boto3.client(
#     's3',
#     aws_access_key_id = os.environ['S3_KEY'],
#     aws_secret_access_key = os.environ['S3_SECRET'],
#     region_name = 'us-west-1'
# )

# clientResponse = client.list_buckets()

# # Print the bucket names one by one
# print('Printing bucket names...')
# for bucket in clientResponse['Buckets']:
#     print(f'Bucket Name: {bucket["Name"]}')


# absolute_path = os.path.dirname(os.path.abspath(__file__))
# custmeme = client.download_file('botyutoken','custommemes.txt','C:\\Users\\Alex Chen\\Desktop\\DiscordBot\\memes\\custommemes.txt')

# with open('C:\\Users\\Alex Chen\\Desktop\\DiscordBot\\memes\\custommemes.txt', 'r') as f:       # write it in custom meme templates first
#     print(f.readlines())

# FILE_DIR = os.path.dirname(os.path.abspath(__file__))
# # absolute path to this file's root directory
# PARENT_DIR = os.path.join(FILE_DIR, os.pardir) 
# ROOT = os.path.join(PARENT_DIR, os.pardir) 
# print(PARENT_DIR)

### AMAZON CLIENT TEST ENDS


### WEEBIFY TEST WITH GOOGLE TRANS BEGINS

# from googletrans import Translator
# from googletrans.gtoken import TokenAcquirer
# import time
# import pykakasi


# translator = Translator(service_urls=['translate.googleapis.com'])
# texts = ["I","this","translator","sucks"]
# tex = " ".join(texts)   
# detected = "en"

# kks = pykakasi.kakasi()
# if detected == "en":
#     time.sleep(1)           # suppress timeout errors
#     try:
#         trans = translator.translate(text=tex,src="en",dest="ja")
#         t = kks.convert(trans.text)
#         print(trans.text)
#         for item in t:
#             print(item['hepburn'])
#     except:
#         print("bruh2")


### WEEBIFY TEST ENDS

## IBM TRANSLATE TEST BEGINS
import time,pykakasi,json,os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pykakasi
apikey = os.environ["IBMTOKEN"]
version = "2018-05-01"
authenticator = IAMAuthenticator(f"{apikey}")
language_translator = LanguageTranslatorV3(
    version=f'{version}',
    authenticator=authenticator
)

language_translator.set_service_url('https://api.us-south.language-translator.watson.cloud.ibm.com')
languages = language_translator.list_languages().get_result()
#print(json.dumps(languages, indent=2))

try:
    translation = language_translator.translate(
        text='hola bonjour good',
        target='en').get_result()
    print(translation)
except:
    print("Are you sure that's a human language?")
# kks = pykakasi.kakasi()
# t = kks.convert(translation["translations"][0]["translation"])
# # print(json.dumps(translation, indent=2))
# for item in t:
#             print(item['hepburn'])
## IBM TRANSLATE TEST ENDS


### TEST NLTK
# import nltk
# text = nltk.word_tokenize("I need to tell you something very different. The bread tastes good.")
# print(text)
# tokens = nltk.pos_tag(text,tagset="universal")
# print(tokens)


### END TEST NLTK