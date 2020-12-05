
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


### WEEBIFY TEST BEGINS

# from googletrans import Translator
# from googletrans.gtoken import TokenAcquirer
# import time
# import pykakasi


# translator = Translator(service_urls=['translate.googleapis.com'])
# texts = ["bruh","this","translator","sucks"]
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

### IBM TRANSLATE TEST BEGINS
import time,pykakasi,json,os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
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


translation = language_translator.translate(
    text='yes master',
    model_id='en-ja').get_result()
t = translation["translations"][0]["translation"]
print(json.dumps(translation, indent=2))

### IBM TRANSLATE TEST ENDS