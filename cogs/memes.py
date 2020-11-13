import requests,json
from discord.ext import commands, tasks

class memes(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def ok(self,ctx):
        print("memes is ok")

    @commands.command()
    async def meme(self,ctx,*args):
        
        response = requests.get("https://api.imgflip.com/get_memes")
        memetemplates = ["","","","","",""]
        memedic = {}  #{num: (id,boxcount)}


        # post = {
        #     "template_id": "",
        #     "username": "boyuchen",
        #     "password": "kfq9aWrP#KFtviR",
        #     "boxes":[],
        # }

        post2 = {
            "template_id": "112126428",
            "username": "boyuchen",
            "password": "kfq9aWrP#KFtviR",
            "text0": "text0",
            "text1": "text1",
        }

        box = {
        "text": "",
        "x": 10,
        "y": 10,
        "width": 548,
        "height": 100,
        "color": "#ffffff",
        "outline_color": "#000000"
        }

        if response.status_code == 200: # ok
            res = response.json()
            count = 0
            pointer = 0
            for num,temp in enumerate(res["data"]["memes"]):
                if count < len(res["data"]["memes"])//5:
                    memetemplates[pointer] = memetemplates[pointer] + str(num)+":  "+temp["name"]+"\n"
                    memedic[num] = (temp["id"],temp["box_count"])
                    count += 1
                else:
                    pointer += 1
                    count = 0
                        
        else:
            print("network issue")


        if len(args) == 0:    
            for i in range(len(memetemplates)):
                if len(memetemplates[i]) != 0:
                    p = "```{0}```".format(memetemplates[i])
                    await ctx.send(p,delete_after = 20)
        elif len(args) == 1:
            memeid = memedic[int(args[0])][0]
            post2["template_id"] = memeid


        # boxes doesn't work :(
        #     text = ""
        #     for i in range(memedic[int(args[0])][1]):
        #         text += (" "+str(i))
        #         abox = {
        # "text": str(i),
        # "x": 10,
        # "y": 10,
        # "width": 548,
        # "height": 100,
        # "color": "#ffffff",
        # "outline_color": "#000000"
        # }
        #         post["boxes"].append(abox)
            
            postresponse = requests.request('POST', url='https://api.imgflip.com/caption_image',params=post2).json()
            image = postresponse["data"]["url"].replace("\\","")
            await ctx.send("boi meme {0}{1}".format(args[0]," \"text0\" \"text1\" "))
            await ctx.send(image)

        elif len(args) == 3:
            memeid = memedic[int(args[0])][0]
            post2["template_id"] = memeid
            post2["text0"] = args[1]    
            post2["text1"] = args[2]
            postresponse = requests.request('POST', url='https://api.imgflip.com/caption_image',params=post2).json()
            image = postresponse["data"]["url"].replace("\\","")
            await ctx.send(image)
            
        else:
            await ctx.send("ur kind of a meme")



def setup(bot):
    bot.add_cog(memes(bot))