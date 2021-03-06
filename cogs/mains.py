import discord
from discord.ext import commands, tasks
import random

# contains all the main functions
class mains(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.games = ["You"," ","Your mom","you sleep","Valortne"]
        self.checks1 = ["it's all", "its always","always has","has been","it's always","its all","its there","it's there","it's been there","its been there","it been there","its been","it's been", "wait,","wait it's", "was it like","have you been","has it been","have it been"]
        self.checks2 = []
        self.me = 455948790239723530
    # below are events
    @commands.Cog.listener()
    async def on_ready(self):
        self.loopstatus.start()
        print('Logged on as {0}!'.format(self.bot.user))

    @commands.Cog.listener()
    async def on_connect(self):
        print("bot is connected!")

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.id != 775963765627289630:
            
            content = message.content.lower()   # content of the message in lower case

            if any(word in content for word in self.checks1):
                await message.channel.send("Always Has Been")
                authorid = message.author.id
                await message.channel.send("<:earth_americas:776635947647107072>"+"<@{0}>".format(authorid)+"<:gun:776635947647107072><:astronaut:776635947647107072>")
                await message.channel.send("https://tenor.com/view/always-has-been-gif-18932176")



            if "raid" in content:
                await message.channel.send("raid?")
            
    # below are commands
    @commands.command()
    async def help(self,ctx):
        await ctx.send("Hope you find this helpful")


    @commands.command()
    async def helloworld(self,ctx):
        if ctx.author.id == self.me:
            await ctx.send("Hello World!")
        else:
            await ctx.send("huh?")
        

    @tasks.loop(seconds=5.0)
    async def loopstatus(self):
        r = random.randint(0,5)
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching,name=self.games[r]))

    @commands.command()
    async def ping(self,ctx):
        latency = round(self.bot.latency)
        if latency != 0:
            await ctx.send("Your latency is {}ms".format(latency))
        else:
            await ctx.send("Ur hosting me bruhass")

    @commands.command()
    async def roll(self,ctx,num1,num2):
        rand = random.randint(int(num1),int(num2))
        await ctx.send(rand)
    @commands.command()
    async def brain(self,ctx):
        await ctx.send('https://tenor.com/view/feel-me-think-about-it-gif-7715402')

    @commands.command()
    async def valortne(self,ctx,*args):
        if len(args) != 1:
            await ctx.send('https://tenor.com/view/jojo-jotaro-darby-play-valorant-gif-17386898')
            return
        
        if int(args[0]) > 4:
            await ctx.send('no')
        else:
            for i in range(int(args[0])):
                await ctx.send('https://tenor.com/view/jojo-jotaro-darby-play-valorant-gif-17386898')
   
def setup(bot):
    bot.add_cog(mains(bot))

