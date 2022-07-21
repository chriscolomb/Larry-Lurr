import nextcord
import random
from nextcord.ext import commands

bot = commands.Bot(command_prefix="!")


def message_embed_color(embed):
    random_color = random.randint(0, 2)
    if random_color == 0:
        embed.colour = nextcord.Colour.from_rgb(85, 174, 131)
    elif random_color == 1:
        embed.colour = nextcord.Colour.from_rgb(40, 56, 106)
    else:
        embed.colour = nextcord.Colour.from_rgb(154, 38, 38)


def larry_command(embed):
    """
    See a random Larry image
    """

    larry_image = "https://github.com/chriscolomb/ssbu/raw/master/larry/larry_" + str(random.randint(0, 64)) + ".png"

    embed.set_image(url=larry_image)
    message_embed_color(embed)


@bot.command()
async def larry(ctx):
    embed = nextcord.Embed()
    larry_command(embed)
    await ctx.channel.send(embed=embed)


@bot.command()
async def Larry(ctx):
    embed = nextcord.Embed()
    larry_command(embed)
    await ctx.channel.send(embed=embed)


@bot.command()
async def larryfinger(ctx):
    """
    See a Larry Finger image
    """

    larry_image = "https://github.com/chriscolomb/ssbu/raw/master/larry/larry_11.png"

    embed = nextcord.Embed()
    embed.set_image(url=larry_image)
    message_embed_color(embed)
    await ctx.channel.send(embed=embed)


@bot.command()
async def larry33(ctx):
    """
    See a Larry 33rd image
    """

    larry_image = "https://github.com/chriscolomb/ssbu/raw/master/larry/larry_51.png"

    embed = nextcord.Embed()
    embed.set_image(url=larry_image)
    message_embed_color(embed)
    await ctx.channel.send(embed=embed)


@bot.command()
async def larrydrip(ctx):
    """
    See a Larry Drip image
    """

    larry_image = "https://github.com/chriscolomb/ssbu/raw/master/larry/larry_62.png"

    embed = nextcord.Embed()
    embed.set_image(url=larry_image)
    message_embed_color(embed)
    await ctx.channel.send(embed=embed)


@bot.command()
async def random(ctx):
    """
    See a random Smash character image
    """

    random_image = "https://github.com/chriscolomb/ssbu/raw/master/random/random_" + str(random.randint(0, 666)) + ".png"

    embed = nextcord.Embed()
    embed.set_image(url=random_image)
    message_embed_color(embed)
    await ctx.channel.send(embed=embed)


bot.run('OTk0NzAyMjIyNDE3OTkzODIw.GM_zi3.YmnpRUQEDp6Et_F0n30e5egRYtVRxAZNoAbXZU')
