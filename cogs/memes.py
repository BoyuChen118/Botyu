import requests
import json
import boto3,os
from discord.ext import commands, tasks


class memes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.amazonclient = boto3.client(
    's3',
    aws_access_key_id = os.environ['S3_KEY'],
    aws_secret_access_key = os.environ['S3_SECRET'],
    region_name = 'us-west-1'
)
    
    @commands.command()
    async def ok(self, ctx):
        print("memes is ok")

    @commands.command()
    async def meme(self, ctx, *args):

        possiblecommands = ["submit", "delete"]
        response = requests.get("https://api.imgflip.com/get_memes")
        memetemplates = ["", "", "", "", "", "", "", ""]
        memedic = {}  # {num: (id,boxcount)}

        # test code
        clientResponse = self.amazonclient.list_buckets()

        # Print the bucket names one by one
        print('Printing bucket names...')
        for bucket in clientResponse['Buckets']:
            await ctx.send(f'Bucket Name: {bucket["Name"]}')
        
        # test ^

        post2 = {
            "template_id": "112126428",
            "username": "boyuchen",
            "password": "kfq9aWrP#KFtviR",
        }
        
        if response.status_code == 200:  # ok
            res = response.json()
            count = 0
            pointer = 0
            self.amazonclient.download_file('botyutoken','custommemes.txt','C:\\Users\\Alex Chen\\Desktop\\DiscordBot\\memes\\custommemes.txt')
            with open('memes/custommemes.txt', 'r') as f:
                lines = f.readlines()
                # iterate through custom templates
                for num, line in enumerate(lines):
                    try:
                        if count >= 20:
                            pointer += 1
                            count = 0
                        elif count < len(lines):
                            num = num + 100
                            firstcomma = line.index(",")
                            secondcomma = line.index(
                                ",", firstcomma+1, len(line))
                            name = line[0:firstcomma]
                            # break down each entry
                            memetemplates[pointer] = memetemplates[pointer] + \
                                str(num)+":  "+name+"\n"
                            memedic[num] = (
                                int(line[firstcomma+1:secondcomma]), int(line[secondcomma+1:]))
                            count += 1
                    except:
                        continue

            pointer += 1
            # iterate through premade templates
            for num, temp in enumerate(res["data"]["memes"]):
                if count >= len(res["data"]["memes"])//5:
                    pointer += 1
                    count = 0
                if count < len(res["data"]["memes"])//5:
                    memetemplates[pointer] = memetemplates[pointer] + \
                        str(num)+":  "+temp["name"]+"\n"
                    memedic[num] = (temp["id"], temp["box_count"])
                    count += 1
                else:
                    print("error in memes")

        else:
            print("network issue")

        if len(args) == 0:
            for i in range(len(memetemplates)):
                if len(memetemplates[i]) != 0:
                    p = "```{0}```".format(memetemplates[i])
                    await ctx.send(p, delete_after=30)
                    await ctx.author.send(p)

        elif len(args) == 1:
            if not args[0].isdigit():
                if str(args[0]) in possiblecommands:  # unknown commands
                    if possiblecommands.index(str(args[0])):
                        await ctx.send("format: boi meme delete name")
                    else:
                        await ctx.send("format: boi meme submit \"name\" ID numberoftextboxes")
                else:
                    await ctx.send("ur kinda a 米姆")
                    return
            elif int(args[0]) > 500:    # it's an id
                await ctx.send("format for instant custom template: boi meme ID numberoftextboxes text1 text2 ....")
            else:
                memeid = memedic[int(args[0])][0]
                post2["template_id"] = memeid
                text = ""
                for i in range(memedic[int(args[0])][1]):
                    text += (" text"+str(i))
                    post2[f"boxes[{i}][text]"] = f"text{i}"
                    post2[f"boxes[{i}][type]"] = "text"

                postresponse = requests.request(
                    'POST', url='https://api.imgflip.com/caption_image', params=post2).json()
                image = postresponse["data"]["url"].replace("\\", "")
                await ctx.send("boi meme {0}{1}".format(args[0], text))
                await ctx.send(image)

        elif len(args) >= 2 and len(args) < 20:
            if not args[0].isdigit() and str(args[0]) not in possiblecommands:
                await ctx.send("ur kinda a 米姆")
            # submit a custom meme template for later use  index 1: name, index 2: id ,index 3: boxcount
            elif str(args[0]).lower() == "submit":
                if len(args) == 4:
                    self.amazonclient.download_file('botyutoken','custommemes.txt','C:\\Users\\Alex Chen\\Desktop\\DiscordBot\\memes\\custommemes.txt')
                    self.amazonclient.download_file('botyutoken','backupmemes.txt','C:\\Users\\Alex Chen\\Desktop\\DiscordBot\\memes\\backupmemes.txt')
                    with open('memes/custommemes.txt', 'a') as f:       # write it in custom meme templates first
                        f.write("\"{0}\",{1},{2}\n".format(
                            str(args[1]), str(args[2]), str(args[3])))
                    with open('memes/backupmemes.txt', 'a') as f:       # save of copy in backup
                        f.write("\"{0}\",{1},{2}\n".format(
                            str(args[1]), str(args[2]), str(args[3])))
                    self.amazonclient.upload_file('C:\\Users\\Alex Chen\\Desktop\\DiscordBot\\memes\\custommemes.txt','botyutoken','custommemes.txt')
                    self.amazonclient.upload_file('C:\\Users\\Alex Chen\\Desktop\\DiscordBot\\memes\\backupmemes.txt','botyutoken','backupmemes.txt')
                    await ctx.send("submission successful")
                    return
                else:
                    await ctx.send("format: boi meme submit \"name\" ID numberoftextboxes")
                    return
              

            # delete a meme template index 1: name of template to be deleted
            elif str(args[0]).lower() == "delete":

                if len(args) == 2:
                    self.amazonclient.download_file('botyutoken','custommemes.txt','C:\\Users\\Alex Chen\\Desktop\\DiscordBot\\memes\\custommemes.txt')
                    self.amazonclient.download_file('botyutoken','backupmemes.txt','C:\\Users\\Alex Chen\\Desktop\\DiscordBot\\memes\\backupmemes.txt')
                    with open("memes/custommemes.txt", "r") as f:
                        lines = f.readlines()
                    with open("memes/custommemes.txt", "w") as f:
                        for line in lines:
                            if str(args[1]).lower() not in line.lower():
                                f.write(line)
                    self.amazonclient.upload_file('C:\\Users\\Alex Chen\\Desktop\\DiscordBot\\memes\\custommemes.txt','botyutoken','custommemes.txt')
                    self.amazonclient.upload_file('C:\\Users\\Alex Chen\\Desktop\\DiscordBot\\memes\\backupmemes.txt','botyutoken','backupmemes.txt')
                    await ctx.send("delete successful")
                    return
                else:
                    await ctx.send("format: boi meme delete name")
                    return
            elif int(args[0]) > 500:  # custom template  index 0: id, index 1:boxcount
                post2["template_id"] = int(args[0])
                firstargument = 2
                boxcount = 0
                if not args[1].isdigit():
                    firstargument = 1
                    boxcount = 2
                else:
                    boxcount = int(args[1])
                for i in range(boxcount):
                    argument = ""
                    if len(str(args[i+firstargument])) == 0:
                        argument = " "
                    else:
                        argument = str(args[i+firstargument])
                    post2[f"boxes[{i}][text]"] = argument.upper()
                    post2[f"boxes[{i}][type]"] = "text"
            else:
                memeid = memedic[int(args[0])][0]
                boxnum = len(args)-1
                if boxnum < memedic[int(args[0])][1]:
                    await ctx.send("This template needs more arguments")
                    return
                elif boxnum > memedic[int(args[0])][1]:
                    await ctx.send("Too many argument, but still works")
                post2["template_id"] = memeid
                for i in range(memedic[int(args[0])][1]):
                    argument = ""
                    if len(str(args[i+1])) == 0:
                        argument = " "
                    else:
                        argument = str(args[i+1])
                    post2[f"boxes[{i}][text]"] = argument.upper()
                    post2[f"boxes[{i}][type]"] = "text"

            postresponse = requests.request(
                'POST', url='https://api.imgflip.com/caption_image', params=post2).json()
            if not postresponse["success"]:
                await ctx.send("You just got memed on son")
                return
            image = postresponse["data"]["url"].replace("\\", "")
            await ctx.send(image)

        else:
            await ctx.send("ur kinda a 米姆")


def setup(bot):
    bot.add_cog(memes(bot))
