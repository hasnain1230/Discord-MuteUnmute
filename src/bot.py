from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

from src import config

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('We have logged in as {}'.format(bot.user))
    # Would like to learn how to send a message to all channels.


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        return
    raise error


@bot.command()
@has_permissions(administrator=True)
async def mute(ctx):
    channel = ctx.message.author.voice.channel
    for member in channel.members:
        if not member.voice.mute:
            await member.edit(mute=True)
        else:
            await member.edit(mute=False)


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to do that!")
        return
    raise error

TOKEN = config.DISCORD_SECRET_TOKEN
bot.run(TOKEN)