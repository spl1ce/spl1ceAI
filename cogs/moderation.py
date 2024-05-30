import discord
from discord.ext import commands
from utils import utils



# TO-DO: ##################
# cooldown command
# automoderation (still to figure out)
# kick, ban, mute and timout commands
# some pasta bolognesa at the end
# list of mods and shi 





class TimeConverter(commands.Converter):

    def convert(self, ctx, time: str):
        import re
        pattern = r"^(\d+)([smhd])?$"
        myMatch = re.match(pattern, time)

        if not myMatch:
            raise ValueError("Invalid input format. The format should be [number][unit], where unit is 's', 'm', 'h', or 'd'.")

        value = int(myMatch.group(1))
        unit = myMatch.group(2)
        unit_dict = {"s": 1, "m": 60, "h": 3600, "d": 86400, None: 1}

        if unit in unit_dict:
            return value * unit_dict[unit]
        else:
            raise ValueError("Invalid unit. The unit should be 's', 'm', 'h', or 'd'.")


class Moderation(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot




    @commands.hybrid_command(name='cooldown', aliases=['slowmode'])
    async def cooldown(self, ctx, time, channel=None):
        
        if not channel:
            channel = ctx.channel
            
        else: 
            converter = commands.TextChannelConverter()
            channel = converter.convert(ctx, channel)

        try:
            timeconverter = TimeConverter()
            seconds = timeconverter.convert(ctx, time)
        except ValueError as error:
            embed = utils.error_embed
            embed.description = str(error)
            await ctx.reply(embed=embed, ephemeral=True)
            return

        await channel.edit(slowmode=seconds)

    @cooldown.error
    async def handler(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            print('pila')
            pass
        elif isinstance(error, commands.ChannelNotFound):
            print('pau')
            pass
        elif isinstance(error, discord.Forbidden):
            if error.code == 50013:
                embed = utils.perms_embed
                embed.description = f"I can do that without these permissions: {', '.join(error.missing_permissions)}"
                await ctx.reply(embed=embed)
        else:
            print(error)
    
async def setup(bot):
    await bot.add_cog(Moderation(bot))



# Not much for now