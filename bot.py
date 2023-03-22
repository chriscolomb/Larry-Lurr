import nextcord
import random as r
from nextcord import Interaction, SlashOption
# from nextcord.abc import GuildChannel
from nextcord.ext import commands
from typing import Optional
from graphql import getTop8


intents = nextcord.Intents.default()
intents.message_content = True
# intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


judge_dictionary = {}


@bot.event
async def on_ready():
    game = nextcord.Game("SSBU")
    await bot.change_presence(activity=game)


def message_embed_color(embed):
    random_color = r.randint(0, 2)
    if random_color == 0:
        embed.colour = nextcord.Colour.from_rgb(85, 174, 131)
    elif random_color == 1:
        embed.colour = nextcord.Colour.from_rgb(40, 56, 106)
    else:
        embed.colour = nextcord.Colour.from_rgb(154, 38, 38)


@bot.slash_command(name="larry", description="Larry image")
async def larry(interaction: Interaction, image: str = SlashOption(choices={
    "random": "random",
    "finger": "https://github.com/chriscolomb/ssbu/raw/master/larry/larry_11.png",
    "33": "https://github.com/chriscolomb/ssbu/raw/master/larry/larry_51.png",
    "drip": "https://github.com/chriscolomb/ssbu/raw/master/larry/larry_62.png"
    }, description="Choose image type")):

    if image == "random":
        image = "https://github.com/chriscolomb/ssbu/raw/master/larry/larry_" + str(r.randint(0, 66)) + ".png"
    
    embed = nextcord.Embed()    
    embed.set_image(url=image)
    message_embed_color(embed)
    await interaction.response.send_message(embed=embed)


@bot.slash_command(name="random", description="Random character portrait")
async def random(interaction: Interaction):
    random_image = "https://github.com/chriscolomb/ssbu/raw/master/random/random_" + str(r.randint(0, 670)) + ".png"

    embed = nextcord.Embed()
    embed.set_image(url=random_image)
    message_embed_color(embed)
    await interaction.response.send_message(embed=embed)


@bot.slash_command(name="ridley", description="Random Ridley portrait")
async def ridley(interaction: Interaction):
    ridley_image = "https://github.com/chriscolomb/ssbu/raw/master/ridley/ridley_" + str(r.randint(0, 7)) + ".png"

    embed = nextcord.Embed()
    embed.set_image(url=ridley_image)
    message_embed_color(embed)
    await interaction.response.send_message(embed=embed)


@bot.slash_command(name="judge", description="Random judge (cannot get the same number twice in a row)")
async def judge(interaction: Interaction):
    user_id = interaction.user.id
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
    await interaction.response.send_message(embed=embed)


@bot.slash_command(name="top8", description="Top 8 generator")
async def top8(interaction: Interaction, event: Optional[str] = SlashOption(required=True, description="Event URL (https://start.gg/tournament/.../event/...)"), graphic: Optional[str] = SlashOption(required=False, description="Image URL for Top 8 graphic")):
    split = event.split('/')

    for i in range(len(split)):
        if split[i] == "tournament":
            tournament = split[i+1]
        elif split[i] == "event":
            if split[i+1]:
                event = split[i+1]
    
    embed = nextcord.Embed()
        
    if tournament and event:
        top8_info = getTop8(tournament, event)
        if len(top8_info) == 0:
            embed = nextcord.Embed(
                title = "Error: Incorrectly formatted event URL",
                description = "**Example:** `https://start.gg/tournament/some-tourney/event/some-event`"
            )
        elif top8_info[2] < 8:
            embed = nextcord.Embed(
                title = "Error: 8 or more entrants are required"
            )
        else:
            embed = nextcord.Embed(
                title = top8_info[0] + " - " + top8_info[1],
                url = "https://start.gg/tournament/" + tournament + "/event/" + event 
            )
            top8 = "> `1st` " + top8_info[4][0] + "\n" \
                    "> `2nd` " + top8_info[4][1] + "\n" \
                    "> `3rd` " + top8_info[4][2] + "\n" \
                    "> `4th` " + top8_info[4][3] + "\n" \
                    "> `5th` " + top8_info[4][4] + "\n" \
                    "> `5th` " + top8_info[4][5] + "\n" \
                    "> `7th` " + top8_info[4][6] + "\n" \
                    "> `7th` " + top8_info[4][7] + "\n"
            embed.add_field(name="Top 8 - " + str(top8_info[2]) + " Participants", value=top8)
            embed.set_footer(text=top8_info[3])
            if graphic:
                embed.set_image(url=graphic)
    else:
        embed = nextcord.Embed(
            title = "Error: Incorrectly formatted event URL",
            description = "**Example:** `https://start.gg/tournament/some-tourney/event/some-event`"
        )

    # embed = nextcord.Embed(
    #     title = "Stitchface #123 - Ultimate Singles",
    #     url = event,
    #     # description = "**Friday, March 23, 2023**\n",
    # )
    # top_8 = "> `1st`  TeamDuck\n" \
    #         "> `2nd`  Machu\n" \
    #         "> `3rd`  Machu\n" \
    #         "> `4th`  Machu\n" \
    #         "> `5th`  Machu\n" \
    #         "> `5th`  Machu\n" \
    #         "> `7th`  Machu\n" \
    #         "> `7th`  Machu"
    # embed.add_field(name="Top 8 - 100 Participants", value=top_8)
    # embed.set_footer(text="Friday, March 23, 2023")

    
    message_embed_color(embed)
    await interaction.response.send_message(embed=embed)

    


# # @bot.command()
# # async def ironman(ctx):
# #     ongoing = True
# #     percentage = 0
# #     characters_left = 86
# #     while ongoing:
# #         embed = nextcord.Embed(title="Ironman Challenge")
# #         percentage_field = str(percentage/100) + "% Complete"
# #         embed.add_field(name=percentage_field, value="Next Character:")
# #         random_image = "https://github.com/chriscolomb/ssbu/raw/master/random/random_" + str(r.randint(0, 669)) + ".png"
# #         embed.set_image(url=random_image)
# #         footer_text = str(characters_left) + " Characters Left!"
# #         embed.set_footer(text=footer_text)
# #         characters_left -= 1
# #         # buttons = ()
# #         ongoing = False
# #     # await ctx.channel.send(embed=embed, view=buttons)
# #     await ctx.channel.send(embed=embed)

# # @bot.command()
# # async def CB(ctx, user: nextcord.Member, size):
# #     channel = bot.get_channel(ctx.channel.id)
# #     guild_id = ctx.message.guild.id
# #     server = bot.get_guild(guild_id)
# #     p1_username = str(server.get_member(ctx.author.id))
# #     p2_username = str(server.get_member(user.id))

# #     # Error handling
# #     if user.id == ctx.author.id:
# #         embed = nextcord.Embed(
# #                 title="You cannot initiate a Crew Battle with yourself."
# #         )
# #         message_embed_color(embed)
# #         await ctx.channel.send(embed=embed)
# #         return None
# #     elif channel.type == nextcord.ChannelType.public_thread:
# #         embed = nextcord.Embed(
# #             title="Cannot do `!CB` command within a thread!"
# #         )
# #         message_embed_color(embed)
# #         await ctx.channel.send(embed=embed)
# #         return None

# #     await ctx.channel.send("1v1 is size " + str(size))


bot.run('OTk0NzAyMjIyNDE3OTkzODIw.GM_zi3.YmnpRUQEDp6Et_F0n30e5egRYtVRxAZNoAbXZU') #Real
# refresh repo