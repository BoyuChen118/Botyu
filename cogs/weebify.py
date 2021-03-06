from discord.ext import commands, tasks
import time
import os
import googletrans
from googletrans import Translator
import random
import pykakasi
import nltk
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


class weebify(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.installation = False
        apikey = os.environ["IBMTOKEN"]
        version = "2018-05-01"
        authenticator = IAMAuthenticator(f"{apikey}")
        self.language_translator = LanguageTranslatorV3(
            version=f'{version}',
            authenticator=authenticator
        )
        self.language_translator.set_service_url(
            'https://api.us-south.language-translator.watson.cloud.ibm.com')

    def trans(self, string):
        pass

    @commands.command()
    async def translate(self, ctx, *args):
       
        errorcounter = 0
        while errorcounter < 10:         # solve googletrans library api token generation issue
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
                    detected = translator.detect(trans.text).lang
                    if detected == "en":                # check again for translation accuracy 
                        await ctx.send(trans.text)
                        
                    else:
                        await ctx.send("Are you sure that's a human language?")
                break
                

            except:
                print(Exception.args)
                errorcounter += 1
                continue
        if errorcounter >= 10:  # defer to ibm to translate
            string = []
            for arg in args:
                string.append(arg)
            tex = " ".join(string)
            try:
                translation = self.language_translator.translate(
                    text=tex,
                    target='en').get_result()["translations"][0]["translation"]
                await ctx.send(translation)
            except:
                await ctx.send("Are you sure that's a human language?")

    @commands.command()
    async def weebify(self, ctx, *args):  # romanizes random words

        if self.installation == False:
            nltk.download('universal_tagset')
            nltk.download('averaged_perceptron_tagger')
            self.installation = True

        try:
            # set up translation tools and make sure user input isn't too long
            words = [arg for arg in args]

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

            # pick which words to be weebified (dependent on percentage, default to 20%)
            percentage = 0
            if words[0].isdigit():
                percentage = int(words[0])
                words[0] = " "
            else:
                percentage = 20
                if len(words) < 5:
                    percentage = 40

            tokens = nltk.pos_tag(words, tagset="universal")
            randlist = []   # index of all to-be-weebified words
            forbitlist = ["him", "her", "yours", "mine",
                        "with", "why", "who", "what", "when"]
            for index, token in enumerate(tokens):
                if token[1] == "PRON" or token[1] == "ADJ" or "yes" in token[0].lower():
                    if token[0].lower() not in forbitlist:
                        randlist.append(index)
            randnum = round(len(randlist) * (percentage/100))

            # rand = random.randint(0, len(words)-1)
            # if rand not in randlist:
            #     randlist.append(rand)

            for r in randlist:                  # weebify them
                translation = self.language_translator.translate(
                    text=words[r],
                    model_id='en-ja').get_result()
                transtext = translation["translations"][0]["translation"]
                if transtext[0] == "(":
                    translator = Translator(
                        service_urls=['translate.googleapis.com'])
                    transtext = translator.translate(
                        text=words[r], src="en", dest="ja").text
                t = kks.convert(transtext)
                words[r] = t[0]['hepburn']
                if words[r] == "I":
                    words[r] = "watashi"  # had to hardcode this one smh
            await ctx.send(" ".join(words))
        except:
            await ctx.send("fix the format bruh")


def setup(bot):
    bot.add_cog(weebify(bot))
