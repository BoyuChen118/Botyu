import discord
import os
from discord.ext import commands
from confidentials import config

TOKEN = os.environ["TOKEN"]

client = commands.Bot(command_prefix = 'boi ',help_command=None)

@client.command()
async def load(ctx,extension):
    client.load_extension('cogs.{0}'.format(extension))

@client.command()
async def unload(ctx,extension):
    client.unload_extension('cogs.{0}'.format(extension))

@client.command()
async def reload(ctx,extension):
    await ctx.invoke(client.get_command('unload'),extension)
    await ctx.invoke(client.get_command('load'),extension)

@client.command()
async def die(ctx):
    if ctx.author.id == 455948790239723530:
        await ctx.send("<:skull:777710892736970802> \*menacing death noises\* <:skull:777710892736970802>")
        await client.close()
    else:
        await ctx.send("I can never be killed")
# Load initial cogs
for filename in os.listdir('./cogs'):       
    if filename.endswith('.py'):
        client.load_extension('cogs.{0}'.format(filename[:-3]))
    
client.run(TOKEN)