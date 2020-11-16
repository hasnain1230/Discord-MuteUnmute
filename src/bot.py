from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from src import config

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user} has logged in successfully!')


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


bot.run(config.DISCORD_SECRET_TOKEN)
