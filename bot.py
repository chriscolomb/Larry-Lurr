import nextcord
import random
from nextcord.ext import commands

bot = commands.Bot(command_prefix="!")

@bot.command()
async def larry(ctx):
    """
    See a random Larry image
    """

    larry_image = "https://github.com/chriscolomb/ssbu/raw/master/larry/larry_" + str(random.randint(0, 61)) + ".png"

    embed = nextcord.Embed()
    embed.set_image(url=larry_image)
    embed.colour = nextcord.Colour.from_rgb(85, 174, 131)
    await ctx.channel.send(embed=embed)


@bot.command()
async def larryfinger(ctx):
    """
    See a Larry Finger image
    """

    larry_image = "https://github.com/chriscolomb/ssbu/raw/master/larry/larry_11.png"

    embed = nextcord.Embed()
    embed.set_image(url=larry_image)
    embed.colour = nextcord.Colour.from_rgb(85, 174, 131)
    await ctx.channel.send(embed=embed)


bot.run('OTk0NzAyMjIyNDE3OTkzODIw.GM_zi3.YmnpRUQEDp6Et_F0n30e5egRYtVRxAZNoAbXZU')