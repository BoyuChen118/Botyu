import discord
import os
from discord.ext import commands
from confidentials import config
from boto.s3.connection import S3Connection

TOKEN = S3Connection(os.environ['TOKEN'])

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
# Load initial cogs
for filename in os.listdir('./cogs'):       
    if filename.endswith('.py'):
        client.load_extension('cogs.{0}'.format(filename[:-3]))
    
client.run(TOKEN)