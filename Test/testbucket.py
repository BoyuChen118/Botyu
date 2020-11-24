import boto3,os

client = boto3.client(
    's3',
    aws_access_key_id = os.environ['S3_KEY'],
    aws_secret_access_key = os.environ['S3_SECRET'],
    region_name = 'us-west-1'
)

clientResponse = client.list_buckets()

# Print the bucket names one by one
print('Printing bucket names...')
for bucket in clientResponse['Buckets']:
    print(f'Bucket Name: {bucket["Name"]}')


absolute_path = os.path.dirname(os.path.abspath(__file__))
custmeme = client.download_file('botyutoken','custommemes.txt','C:\\Users\\Alex Chen\\Desktop\\DiscordBot\\memes\\backupmemes.txt')

with open('C:\\Users\\Alex Chen\\Desktop\\DiscordBot\\memes\\backupmemes.txt', 'r') as f:       # write it in custom meme templates first
    print(f.readlines())