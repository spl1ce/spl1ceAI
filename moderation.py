import discord
from discord.ext import commands




# TO-DO: ##################
# cooldown command
# automoderation (still to figure out)
# kick, ban, mute and timout commands
# some pasta bolognesa at the end



class Moderation(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.hybrid_command()
    async def cooldown(ctx, units, channel=None):
        pass

    @cooldown.error
    async def handler(ctx, error):
        if isinstance(error, commands.BadArgument):
            pass
    




# Not much for now