import discord
from discord.ext import commands

from utils import utils
import json
import os

with open("key.json", "r") as config:
    key = json.load(config)

intents = discord.Intents.all()

class Bot(commands.Bot):
    async def setup_hook(self):

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"{filename} loaded!")

            else:
                print(f"{filename} is not a cog.")
        
        print('Bot is setup.')

bot = Bot(command_prefix=":", activity=discord.Activity(type = discord.ActivityType.playing, name="with you"), intents=intents)

############################
# Bot boot events          #
############################

@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.event
async def on_connect():
    print('Bot is connected to Discord.')


############################
# Commands for development #
############################

@commands.is_owner()
@bot.command(name='reload', help='Reloads a cog')
async def reload(ctx, extension):

    await bot.reload_extension(f'cogs.{extension}')
    embed = utils.confirmation_embed
    embed.description=f'```🔄 Reloaded cogs.{extension} ```'


    await ctx.reply(embed=embed, ephemeral=True)



@commands.is_owner()
@commands.guild_only()
@bot.command(name='sync', help='Syncs the bots commands with Discord API.')
async def sync(ctx: commands.Context):

    synced = await ctx.bot.tree.sync()
    embed = utils.confirmation_embed
    embed.description=f"Synced {len(synced)} commands 'globally'"

    await ctx.reply(embed=embed, ephemeral=True)



@reload.error
async def handler(ctx, error):
    if isinstance(error, commands.NotOwner):
        pass


bot.run(key["token"])