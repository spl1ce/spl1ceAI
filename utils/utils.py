import discord


######################
# Pre-made embeds    #
######################


confirmation_embed = discord.Embed(color=discord.Color.green())
invalid_embed = discord.Embed(color=discord.Color.red())
unexpected_embed = discord.Embed(color=discord.Color.red(), title="Unexpected Error")
perms_embed = discord.Embed(color=discord.Color.dark_red(), title="Missing Permissions")
usage_embed = discord.Embed(color=discord.Color.dark_blue(), title="Invalide Usage")