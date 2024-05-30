import discord
from discord.ext import commands

#####################################################
# A sweet logging system that doesn't exist... yet! #
#####################################################

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Logging(bot))