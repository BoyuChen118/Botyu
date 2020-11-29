from discord.ext import commands, tasks
import time
import googletrans
from googletrans import Translator
from googletrans.gtoken import TokenAcquirer


class weebify(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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
        await ctx.send("😢")

    @commands.command()
    async def weebify(self,ctx, *args):
        pass

def setup(bot):
    bot.add_cog(weebify(bot))
