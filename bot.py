import nextcord
import random as r
from nextcord.ext import commands

bot = commands.Bot(command_prefix="!", help_command=None)


def message_embed_color(embed):
    random_color = r.randint(0, 2)
    if random_color == 0:
        embed.colour = nextcord.Colour.from_rgb(85, 174, 131)
    elif random_color == 1:
        embed.colour = nextcord.Colour.from_rgb(40, 56, 106)
    else:
        embed.colour = nextcord.Colour.from_rgb(154, 38, 38)


def larry_command(embed):
    larry_image = "https://github.com/chriscolomb/ssbu/raw/master/larry/larry_" + str(r.randint(0, 64)) + ".png"

    embed.set_image(url=larry_image)
    message_embed_color(embed)


@bot.command()
async def larry(ctx):
    """
    Random Larry image
    """

    embed = nextcord.Embed()
    larry_command(embed)
    await ctx.channel.send(embed=embed)


@bot.command()
async def Larry(ctx):
    """
    Random Larry image
    """

    embed = nextcord.Embed()
    larry_command(embed)
    await ctx.channel.send(embed=embed)


@bot.command()
async def larryfinger(ctx):
    """
    Larry Finger image
    """

    larry_image = "https://github.com/chriscolomb/ssbu/raw/master/larry/larry_11.png"

    embed = nextcord.Embed()
    embed.set_image(url=larry_image)
    message_embed_color(embed)
    await ctx.channel.send(embed=embed)


@bot.command()
async def larry33(ctx):
    """
    Larry 33rd image
    """

    larry_image = "https://github.com/chriscolomb/ssbu/raw/master/larry/larry_51.png"

    embed = nextcord.Embed()
    embed.set_image(url=larry_image)
    message_embed_color(embed)
    await ctx.channel.send(embed=embed)


@bot.command()
async def larrydrip(ctx):
    """
    Larry Drip image
    """

    larry_image = "https://github.com/chriscolomb/ssbu/raw/master/larry/larry_62.png"

    embed = nextcord.Embed()
    embed.set_image(url=larry_image)
    message_embed_color(embed)
    await ctx.channel.send(embed=embed)


@bot.command()
async def random(ctx):
    """
    Random character image
    """

    random_image = "https://github.com/chriscolomb/ssbu/raw/master/random/random_" + str(r.randint(0, 669)) + ".png"

    embed = nextcord.Embed()
    embed.set_image(url=random_image)
    message_embed_color(embed)
    await ctx.channel.send(embed=embed)


@bot.command()
async def help(ctx):
    embed = nextcord.Embed(
        title="Bot Commands"
    )
    message_embed_color(embed)

    image_value = "`      !larry` *Random Larry image*\n" \
                  "`      !Larry` *Random Larry image*\n" \
                  "`  !larrydrip` *Larry Drip image*\n" \
                  "`    !larry33` *Larry 33rd image*\n" \
                  "`!larryfinger` *Larry Finger image*\n" \
                  "`     !random` *Random character image*"
    embed.add_field(name="Image Commands", value=image_value)

    await ctx.channel.send(embed=embed)


bot.run('OTk0NzAyMjIyNDE3OTkzODIw.GM_zi3.YmnpRUQEDp6Et_F0n30e5egRYtVRxAZNoAbXZU') #Real
# bot.run('OTk5Nzc4NjMwMjg2NzA4ODI2.GwaPvU.mHwZ9zrLTwQ1ZiIByD9Yj5yb2Oj008YhbOXfJ0') #Fake
