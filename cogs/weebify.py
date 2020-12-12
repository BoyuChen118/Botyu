from discord.ext import commands, tasks
import time
import os
import googletrans
from googletrans import Translator
import random
import pykakasi,nltk
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


class weebify(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        nltk.download("popular")

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
            words[0] = " "
        else:
            percentage = 20
            if len(words) < 5:
                percentage = 40
        
        tokens = nltk.pos_tag(words,tagset="universal")
        randlist = []   # index of all to-be-weebified words
        forbitlist = ["him","her","yours","mine","with","why","who","what","when"]
        for index,token in enumerate(tokens):
            if token[1] == "PRON" or token[1] == "ADJ" or "yes" in token[0].lower():
                if token[0].lower() not in forbitlist:
                    randlist.append(index)
        numdeleted = round(len(randlist) * (percentage/100))
        
            # rand = random.randint(0, len(words)-1)
            # if rand not in randlist:
            #     randlist.append(rand)
            

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
            if words[r] == "I":
                words[r] = "watashi"  # had to hardcode this one smh
        await ctx.send(" ".join(words))


def setup(bot):
    bot.add_cog(weebify(bot))
