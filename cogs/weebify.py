from discord.ext import commands, tasks
import time
import googletrans
from googletrans import Translator
from googletrans.gtoken import TokenAcquirer
import random
import pykakasi

class weebify(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def trans(self,string):
        pass
    @commands.command()
    async def translate(self, ctx, *args):
        errorcounter = 0
        while errorcounter < 100:         # solve googletrans library api token generation issue 
            try:
                translator = Translator()
                string = []
                for arg in args:
                    string.append(arg)
                tex = " ".join(string)
                detected = translator.detect(tex).lang
                if detected == "en":
                    trans = translator.translate(text=tex, src="en", dest="ja")
                    await ctx.send(trans.text)
                else:
                    trans = translator.translate(
                        text=tex, src=detected, dest="en")
                    await ctx.send(trans.text)

            except:
                print(Exception.args)
                errorcounter += 1
                continue
            break
        if errorcounter > 100:
            await ctx.send("😢")

    @commands.command()
    async def weebify(self,ctx, *args):  # romanizes random words
        words = [arg for arg in args]
        kks = pykakasi.kakasi()
        translator = Translator(service_urls=['translate.googleapis.com'])

        percentage = 0                      # pick which words to be weebified (dependent on percentage, default to 20%)
        if words[0].isdigit():
            percentage = int(words[0])
        else:
            percentage = 30
            if len(words) < 5:
                percentage = 40
        numrand = round(len(words) * (percentage/100))
        randlist = []
        while len(randlist) < numrand:
            rand = random.randint(0,len(words)-1)
            if rand not in randlist:
                randlist.append(rand)

        for r in randlist:                  # weebify them
            trans = translator.translate(text=words[r],src="en",dest="ja")
            t = kks.convert(trans.text)
            words[r] = t[0]['hepburn']
        await ctx.send(" ".join(words))


def setup(bot):
    bot.add_cog(weebify(bot))
