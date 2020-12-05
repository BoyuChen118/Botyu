from discord.ext import commands, tasks
import time
import os
import googletrans
from googletrans import Translator
import random
import pykakasi
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


class weebify(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def trans(self, string):
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
    async def weebify(self, ctx, *args):  # romanizes random words

        words = [arg for arg in args]       # set up translation tools and make sure user input isn't too long

        charcount = 0
        if len(words) > 300:
            await ctx.send("input too long my brain too small")
            return
        else:
            for w in words:
                charcount += len(w)
            if charcount > 2000:
                await ctx.send("input too long my brain too small")
                return
        
        kks = pykakasi.kakasi()
        apikey = os.environ["IBMTOKEN"]
        version = "2018-05-01"
        authenticator = IAMAuthenticator(f"{apikey}")
        language_translator = LanguageTranslatorV3(
            version=f'{version}',
            authenticator=authenticator
        )
        language_translator.set_service_url(
            'https://api.us-south.language-translator.watson.cloud.ibm.com')

        # pick which words to be weebified (dependent on percentage, default to 20%)
        percentage = 0
        if words[0].isdigit():
            percentage = int(words[0])
            words[0] = ""
        else:
            percentage = 20
            if len(words) < 5:
                percentage = 40
        numrand = round(len(words) * (percentage/100))
        randlist = []
        while len(randlist) < numrand:
            rand = random.randint(0, len(words)-1)
            if rand not in randlist:
                randlist.append(rand)

        for r in randlist:                  # weebify them
            translation = language_translator.translate(
                text=words[r],
                model_id='en-ja').get_result()
            transtext = translation["translations"][0]["translation"]
            if transtext[0] == "(":
                translator = Translator(service_urls=['translate.googleapis.com'])
                transtext = translator.translate(text=words[r],src="en",dest="ja").text
            t = kks.convert(transtext)
            words[r] = t[0]['hepburn']
        await ctx.send(" ".join(words))


def setup(bot):
    bot.add_cog(weebify(bot))
