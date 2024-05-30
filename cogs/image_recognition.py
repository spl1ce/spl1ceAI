import discord
from discord.ext import commands

###################################
# some image recognition type shi #


class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(AI(bot))