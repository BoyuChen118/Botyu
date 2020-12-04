
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

from googletrans import Translator
from googletrans.gtoken import TokenAcquirer
import time
import pykakasi
# while True:
#     try:
#         acquirer = TokenAcquirer()
#         text = 'test'
#         tk = acquirer.do(text)
#         print(tk)
#     except:
#         print("bruh1")
#         continue
#     break


translator = Translator(service_urls=['translate.googleapis.com'])
texts = ["bruh","this","translator","sucks"]
tex = " ".join(texts)   
detected = "en"
# try:
#     detected = translator.detect("bruh").lang
# except:
#     print("error in detect")
kks = pykakasi.kakasi()
if detected == "en":
    time.sleep(1)           # suppress timeout errors
    try:
        trans = translator.translate(text=tex,src="en",dest="ja")
        t = kks.convert(trans.text)
        print(trans.text)
        for item in t:
            print(item['hepburn'])
    except:
        print("bruh2")


### WEEBIFY TEST ENDS