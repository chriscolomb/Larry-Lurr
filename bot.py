import nextcord
# import pymongo
import random as r
from nextcord.ext import commands

bot = commands.Bot(command_prefix="!", help_command=None)

# connect to MongoDB
# cluster = pymongo.MongoClient("mongodb+srv://teamduckssb:em-xJFw-97G5mpG@testing-cluster.rzshs.mongodb.net/test")
# larry_lurr_db = cluster["Larry-Lurr"]
# commands_collection = larry_lurr_db["Commands"]
# fake_commands_collection = larry_lurr_db["Fake-Commands"]

judge_dictionary = {}


@bot.event
async def on_ready():
    game = nextcord.Game("!help")
    await bot.change_presence(activity=game)


# @bot.command()
# async def updatedb(ctx):
#     larry_entry = {
#         "_id": "larry",
#         "count": 0
#     }
#     larryfinger_entry = {
#         "_id": "larryfinger",
#         "count": 0
#     }
#     larry33_entry = {
#         "_id": "larry33",
#         "count": 0
#     }
#     larrydrip_entry = {
#         "_id": "larrydrip",
#         "count": 0
#     }
#     random_entry = {
#         "_id": "random",
#         "count": 0
#     }
#     judge_entry = {
#         "_id": "judge",
#         "count": 0
#     }
#     fake_commands_collection.insert_one(larry_entry)
#     fake_commands_collection.insert_one(larry33_entry)
#     fake_commands_collection.insert_one(larrydrip_entry)
#     fake_commands_collection.insert_one(larryfinger_entry)
#     fake_commands_collection.insert_one(random_entry)
#     fake_commands_collection.insert_one(judge_entry)


def message_embed_color(embed):
    random_color = r.randint(0, 2)
    if random_color == 0:
        embed.colour = nextcord.Colour.from_rgb(85, 174, 131)
    elif random_color == 1:
        embed.colour = nextcord.Colour.from_rgb(40, 56, 106)
    else:
        embed.colour = nextcord.Colour.from_rgb(154, 38, 38)


def larry_command(embed):
    larry_image = "https://github.com/chriscolomb/ssbu/raw/master/larry/larry_" + str(r.randint(0, 66)) + ".png"

    embed.set_image(url=larry_image)
    message_embed_color(embed)

    # print(fake_commands_collection.find({"_id":"larry"}))
    # for id in fake_commands_collection.find():
    #     if id["_id"] == user.id:

    # command_query = {
    #     "_id": "larry",
    # }
    # new_command = {
    #     "$set": {
    #         "count":
    #     }
    # }
    # fake_commands_collection.update_one(command_query, new_command)


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
    random_image = "https://github.com/chriscolomb/ssbu/raw/master/random/random_" + str(r.randint(0, 670)) + ".png"

    embed = nextcord.Embed()
    embed.set_image(url=random_image)
    message_embed_color(embed)
    await ctx.channel.send(embed=embed)

@bot.command()
async def ridley(ctx):
    """
    Random Ridley portrait image
    """
    ridley_image = "https://github.com/chriscolomb/ssbu/raw/master/ridley/ridley_" + str(r.randint(0, 7)) + ".png"

    embed = nextcord.Embed()
    embed.set_image(url=ridley_image)
    message_embed_color(embed)
    await ctx.channel.send(embed=embed)


@bot.command()
async def judge(ctx):
    """
    Random judge image
    """
    user_id = ctx.author.id
    judge_number = r.randint(1, 9)
    if user_id not in judge_dictionary.keys():
        judge_dictionary[user_id] = judge_number
    else:
        while judge_dictionary.get(user_id) == judge_number:
            judge_number = r.randint(1, 9)
        judge_dictionary[user_id] = judge_number

    judge_image = "https://github.com/chriscolomb/ssbu/raw/master/judge/judge_" + str(judge_number) + ".png"

    embed = nextcord.Embed()
    embed.set_image(url=judge_image)
    message_embed_color(embed)
    await ctx.channel.send(embed=embed)


# @bot.command()
# async def ironman(ctx):
#     ongoing = True
#     percentage = 0
#     characters_left = 86
#     while ongoing:
#         embed = nextcord.Embed(title="Ironman Challenge")
#         percentage_field = str(percentage/100) + "% Complete"
#         embed.add_field(name=percentage_field, value="Next Character:")
#         random_image = "https://github.com/chriscolomb/ssbu/raw/master/random/random_" + str(r.randint(0, 669)) + ".png"
#         embed.set_image(url=random_image)
#         footer_text = str(characters_left) + " Characters Left!"
#         embed.set_footer(text=footer_text)
#         characters_left -= 1
#         # buttons = ()
#         ongoing = False
#     # await ctx.channel.send(embed=embed, view=buttons)
#     await ctx.channel.send(embed=embed)

# @bot.command()
# async def CB(ctx, user: nextcord.Member, size):
#     channel = bot.get_channel(ctx.channel.id)
#     guild_id = ctx.message.guild.id
#     server = bot.get_guild(guild_id)
#     p1_username = str(server.get_member(ctx.author.id))
#     p2_username = str(server.get_member(user.id))
#
#     # Error handling
#     if user.id == ctx.author.id:
#         embed = nextcord.Embed(
#                 title="You cannot initiate a Crew Battle with yourself."
#         )
#         message_embed_color(embed)
#         await ctx.channel.send(embed=embed)
#         return None
#     elif channel.type == nextcord.ChannelType.public_thread:
#         embed = nextcord.Embed(
#             title="Cannot do `!CB` command within a thread!"
#         )
#         message_embed_color(embed)
#         await ctx.channel.send(embed=embed)
#         return None
#
#     await ctx.channel.send("1v1 is size " + str(size))


@bot.command()
async def help(ctx):
    embed = nextcord.Embed(
        title="Help"
    )
    message_embed_color(embed)

    image_value = "`      !larry` *Random Larry*\n" \
                  "`  !larrydrip` *Larry Drip*\n" \
                  "`    !larry33` *Larry 33rd*\n" \
                  "`!larryfinger` *Larry Finger*\n" \
                  "`     !random` *Random character*\n" \
                  "`     !ridley` *Random Ridley*\n" \
                  "`      !judge` *Random judge*"
    embed.add_field(name="Image Commands", value=image_value)

    embed.set_footer(text="Contact TeamDuck#0876 for questions or requests.", icon_url="https://github.com/chriscolomb/ssbu/blob/master/larry/question.png?raw=true")

    await ctx.channel.send(embed=embed)


bot.run('OTk0NzAyMjIyNDE3OTkzODIw.GM_zi3.YmnpRUQEDp6Et_F0n30e5egRYtVRxAZNoAbXZU') #Real
# bot.run('OTk5Nzc4NjMwMjg2NzA4ODI2.GwaPvU.mHwZ9zrLTwQ1ZiIByD9Yj5yb2Oj008YhbOXfJ0')  # Fake
# refresh repo