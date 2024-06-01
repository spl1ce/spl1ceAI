import discord
from discord.ext import commands




###########################
# just help command subclass
# A bunch to do here too
# 
# NEXT THING TO DO IS HELP COMMAND GOGOGOGO
#
# Main Menu






class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    

async def setup(bot):
    await bot.add_cog(Help(bot))