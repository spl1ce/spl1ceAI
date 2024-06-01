import discord
from discord.ext import commands
from utils import utils


##################
# TO-DO: ######################################################
# cooldown command -  DONE
# automoderation (still to figure out)
# kick, ban, mute and timout commands - DONE
# some pasta bolognesa at the end
# list of mods and shi



class TimeConverter(commands.Converter):

    def convert(self, ctx, time: str):
        """
        Subclass of a commands.Converter class from the discord.py library. 
        Converts a given amount of time to seconds.

        Args:
            ctx (_type_): _description_ Context in which a command was invoked under.
            time (str): _description_ The string to be parsed and converted. The format should be [number][unit], where unit is 's', 'm', 'h', or 'd'.

        Raises:
            ValueError: _description_ Invalid input format.
            ValueError: _description_ Invalid unit.

        Returns:
            _type_ Seconds: _description_ The converted result. 
        """
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


################
# COOLDOWN
# acho que ta tudo - depois logo se ve


    @commands.has_permissions(manage_channels=True)
    @commands.hybrid_command(name='cooldown', aliases=['slowmode'])
    async def cooldown(self, ctx, time, channel=None):
        """
        Sets the cooldown or slowmode of a channel to a given amount of time. Must have Manage Channel permissions.

        Args:
            ctx (_type_): _description_ Context in which the command was invoked under.
            time (_type_): _description_ Amount of time to set the slowmode to.
            channel (_type_, optional): _description_ Channel where to set the slowmode. Defaults to the channel where the command was invoked.
        """
        


        if not channel:
            channel = ctx.channel

        else: 
            converter = commands.TextChannelConverter()
            try:
                channel = await converter.convert(ctx, channel)
            except commands.ChannelNotFound:
                embed = utils.invalid_embed
                embed.title = "Channel not found"
                embed.description = "Please specify a valid channel.\nFormat should be `channel_name`, `@channel_name` or `channel_id`"
                await ctx.reply(embed=embed, ephemeral=True)
                return


        try:
            timeconverter = TimeConverter()
            seconds = timeconverter.convert(ctx, time)
        except:
            embed = utils.invalid_embed
            embed.title = "Invalid time format"
            embed.description = "The format should be [number][unit], where unit is 's', 'm', 'h', or 'd'. "
            await ctx.reply(embed=embed, ephemeral=True)
            return

        try:
            await channel.edit(slowmode_delay=seconds)
            embed = utils.confirmation_embed
            embed.title = "Slowmode"
            embed.description = f"Set to {seconds} second{'s' if seconds != 1 else ''}."
            await ctx.reply(embed=embed, ephemeral=True)
        except discord.Forbidden:
            embed = utils.perms_embed
            embed.description = f"I need the following permissions to do that: \n• `manage_channels`"
            await ctx.reply(embed=embed, ephemeral=True)
        except discord.HTTPException:
            embed = utils.unexpected_embed
            embed.description = f"Failed to edit the channel, please try again."
            await ctx.reply(embed=embed, ephemeral=True)


###########
# pretty much useless since discord already has a slash commands for these two
#
##


    @commands.has_permissions(kick_members=True)
    @commands.hybrid_command(name="kick")
    async def kick(self, ctx, user, *, reason=""):
        """
        Kicks a given user from the guild in which the command was executed.

        Args:
            ctx (_type_): _description_ Context in which the command was invoked under.
            user (_type_): _description_ User to kick. Gets converted to a member with the MemberConverter and then kicked.
            reason (_type_): _description_ The reason for the kick given by the evoker of the command
        """

        converter = commands.MemberConverter()
        try:
            member = await converter.convert(ctx, user)
        except commands.MemberNotFound:
            embed = utils.invalid_embed
            embed.title = "Member not found"
            embed.description = "Format should be `username`, `@username` or `user_id`"
            await ctx.reply(embed=embed, ephemeral=True)
            return

        try:
            await member.kick(reason)
            embed = utils.confirmation_embed
            embed.title = "Kick"
            embed.description = f"**{member.name}** has been kicked."
            await ctx.reply(embed=embed, ephemeral=True)

        except discord.Forbidden:
            embed = utils.perms_embed
            embed.description = f"I need the following permissions to do that: \n• `kick_members`"
            await ctx.reply(embed=embed, ephemeral=True)
        except discord.HTTPException:
            embed = utils.unexpected_embed
            embed.description = f"Failed to kick the user, please try again."
            await ctx.reply(embed=embed, ephemeral=True)




    @commands.has_permissions(ban_members=True)
    @commands.hybrid_command(name="ban")
    async def ban(self, ctx, user, *, reason=""):
        """
        Bans a given user from the guild in which the command was executed.

        Args:
            ctx (_type_): _description_ Context in which the command was invoked under.
            user (_type_): _description_ User to ban. Gets converted to a member with the MemberConverter and then banned.
            reason (_type_): _description_ The reason for the ban given by the evoker of the command
        """

        converter = commands.MemberConverter()
        try:
            member = await converter.convert(ctx, user)
        except commands.MemberNotFound:
            embed = utils.invalid_embed
            embed.title = "Member not found"
            embed.description = "Format should be `username`, `@username` or `user_id`"
            await ctx.reply(embed=embed, ephemeral=True)
            return

        try:
            await member.ban(reason)
            embed = utils.confirmation_embed
            embed.title = "Ban"
            embed.description = f"**{member.name}** has been banned."
            await ctx.reply(embed=embed, ephemeral=True)

        except discord.Forbidden:
            embed = utils.perms_embed
            embed.description = f"I need the following permissions to do that: \n• `ban_members`"
            await ctx.reply(embed=embed, ephemeral=True)
            return
        except discord.HTTPException:
            embed = utils.unexpected_embed
            embed.description = f"Failed to ban the user, please try again."
            await ctx.reply(embed=embed, ephemeral=True)




    @cooldown.error
    @kick.error
    @ban.error
    async def handler(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = utils.usage_embed
            embed.description = 'Maybe try using slash commands.'
            await ctx.reply(embed=embed, ephemeral=True)

        if isinstance(error, commands.MissingPermissions):
            embed = utils.perms_embed
            embed.description = 'You need the following permissions for that:\n• `' + '`\n• `'.join(error.missing_permissions) + '`'
            await ctx.reply(embed=embed, ephemeral=True)
        else:
            print(error)
    
async def setup(bot):
    await bot.add_cog(Moderation(bot))





# Not much for now