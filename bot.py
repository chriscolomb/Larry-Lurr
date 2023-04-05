import nextcord
import random as r
from nextcord import Interaction, InteractionMessage, SlashOption
# from nextcord.abc import GuildChannel
from nextcord.ext import commands
from typing import Optional
from graphql import getTop8, getSeeding


intents = nextcord.Intents.default()
intents.message_content = True

# ENABLE WHEN MENTIONS APPROVED
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
    }, description="Choose image type"), message: Optional[str] = SlashOption(required=False, description="Image title")):

    if image == "random":
        image = "https://github.com/chriscolomb/ssbu/raw/master/larry/larry_" + str(r.randint(0, 66)) + ".png"
    
    embed = nextcord.Embed(
        title = message
    )    
    embed.set_image(url=image)
    message_embed_color(embed)
    await interaction.response.send_message(embed=embed)


@bot.slash_command(name="random", description="Random character portrait")
async def random(interaction: Interaction, message: Optional[str] = SlashOption(required=False, description="Image title")):
    random_image = "https://github.com/chriscolomb/ssbu/raw/master/random/random_" + str(r.randint(0, 670)) + ".png"

    embed = nextcord.Embed(
        title = message
    )
    embed.set_image(url=random_image)
    message_embed_color(embed)
    await interaction.response.send_message(embed=embed)


@bot.slash_command(name="ridley", description="Random Ridley portrait")
async def ridley(interaction: Interaction, message: Optional[str] = SlashOption(required=False, description="Image title")):
    ridley_image = "https://github.com/chriscolomb/ssbu/raw/master/ridley/ridley_" + str(r.randint(0, 7)) + ".png"

    embed = nextcord.Embed(
        title = message
    )
    embed.set_image(url=ridley_image)
    message_embed_color(embed)
    await interaction.response.send_message(embed=embed)


@bot.slash_command(name="judge", description="Random judge (cannot get the same number twice in a row)")
async def judge(interaction: Interaction, message: Optional[str] = SlashOption(required=False, description="Image title")):
    user_id = interaction.user.id
    judge_number = r.randint(1, 9)
    if user_id not in judge_dictionary.keys():
        judge_dictionary[user_id] = judge_number
    else:
        while judge_dictionary.get(user_id) == judge_number:
            judge_number = r.randint(1, 9)
        judge_dictionary[user_id] = judge_number

    judge_image = "https://github.com/chriscolomb/ssbu/raw/master/judge/judge_" + str(judge_number) + ".png"

    embed = nextcord.Embed(
        title = message
    )
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
            # ENABLE WHEN MENTIONS APPROVED
            # -----------------------------
            # server_members = interaction.user.guild.fetch_members()
            # member_strings = []

            # async for member in server_members:
            #     member_strings.append([str(member), member.mention])

            # for top8er in top8_info[4]:
            #     for member in member_strings:    
            #         if member[0] == top8er[1]:
            #             top8er[1] = member[1]

            #     if top8er[1]:
            #         if top8er[1][:2] != "<@":
            #             top8er[1] = ""
            # -----------------------------

            embed = nextcord.Embed(
                title = top8_info[0] + " - " + top8_info[1],
                url = "https://start.gg/tournament/" + tournament + "/event/" + event 
            )
            
            top8 = ""
            for i in range(len(top8_info[4])):
                if i == 0:
                    top8 = top8 + "> `1st` "
                elif i == 1:
                    top8 = top8 + "> `2nd` "
                elif i == 2:
                    top8 = top8 + "> `3rd` "
                elif i == 3:
                    top8 = top8 + "> `4th` "
                elif i == 4 or i == 5:
                    top8 = top8 + "> `5th` "
                else:
                    top8 = top8 + "> `7th` "

                # ENABLE WHEN MENTIONS APPROVED
                # -----------------------------
                # if top8_info[4][i][1]:
                #     top8 = top8 + top8_info[4][i][1] + "\n"
                # else:
                #     top8 = top8 + top8_info[4][i][0] + "\n"
                # -----------------------------
                
                # DISABLE WHEN MENTIONS APPROVED
                top8 = top8 + top8_info[4][i][0] + "\n"

            embed.add_field(name="Top 8 - " + str(top8_info[2]) + " Participants", value=top8)
            embed.set_footer(text=top8_info[3])
            if graphic:
                embed.set_image(url=graphic)
            else:
                embed.set_image(url=top8_info[5])
    else:
        embed = nextcord.Embed(
            title = "Error: Incorrectly formatted event URL",
            description = "**Example:** `https://start.gg/tournament/some-tourney/event/some-event`"
        )
    
    message_embed_color(embed)
    await interaction.response.send_message(embed=embed)


@bot.slash_command(name="seeding", description="Seeding for an event")
async def seeding(interaction: Interaction, event: Optional[str] = SlashOption(required=True, description="Event URL (https://start.gg/tournament/.../event/...)")):
    split = event.split('/')

    for i in range(len(split)):
        if split[i] == "tournament":
            tournament = split[i+1]
        elif split[i] == "event":
            if split[i+1]:
                event = split[i+1]
    
    embed = nextcord.Embed()

    await interaction.response.defer()
        
    if tournament and event:
        seeding = getSeeding(tournament, event)
        if len(seeding) == 0:
            embed = nextcord.Embed(
                title = "Error: Incorrectly formatted event URL",
                description = "**Example:** `https://start.gg/tournament/some-tourney/event/some-event`"
            )
        elif len(seeding[4]) == 0:
            embed = nextcord.Embed(
                title = "Error: Bracket is not published",
            )
        else:
            embeds = []

            for i in range(0, seeding[2], 16):
                

                embed = nextcord.Embed(
                    title = seeding[0] + " - " + seeding[1],
                    url = "https://start.gg/tournament/" + tournament + "/event/" + event 
                )

                seeding_message = ""

                for i2 in range(16):
                    if i+i2 >= seeding[2]:
                        break
                    else:
                        if seeding[2] >= 1000:
                            seeding_message = seeding_message + "> `" + f'{str(seeding[4][i+i2][0]):0>4}' + "` " + seeding[4][i+i2][1] + "\n"
                        elif seeding[2] >= 100:
                            seeding_message = seeding_message + "> `" + f'{str(seeding[4][i+i2][0]):0>3}' + "` " + seeding[4][i+i2][1] + "\n"
                        elif seeding[2] >= 10:
                            seeding_message = seeding_message + "> `" + f'{str(seeding[4][i+i2][0]):0>2}' + "` " + seeding[4][i+i2][1] + "\n"
                        else:
                            seeding_message = seeding_message + "> `" + str(seeding[4][i+i2][0]) + "` " + seeding[4][i+i2][1] + "\n"
                
                embed.add_field(name="Seeding - " + str(seeding[2]) + " Participants", value=seeding_message)
                embed.set_footer(text=seeding[3] + "\n" + "⬇ Reactions don't work? Use \"/help reactions\"")
                embed.set_image(url=seeding[5])
                # print(seeding_message)

                embeds.append(embed)
            
            if len(embeds) == 1:
                message_embed_color(embed)
                await interaction.followup.send(embed=embed)
            else:
                cur = 0
                for i in range(len(embeds)):
                    message_embed_color(embeds[i])
                
                await interaction.followup.send(embed=embeds[cur])
                message = await interaction.original_message()

                await message.add_reaction('⏪')
                await message.add_reaction('◀️')
                await message.add_reaction('▶️')
                await message.add_reaction('⏩')

                def check(reaction, user):
                    return user == interaction.user and str(reaction.emoji) in ['⏪', '◀️', '▶️', '⏩']

                while True:
                    try:
                        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                        if str(reaction.emoji) == '▶️' and cur < len(embeds) - 1:
                            cur += 1
                            await message.edit(embed=embeds[cur])
                        elif str(reaction.emoji) == '◀️' and cur > 0:
                            cur -= 1
                            await message.edit(embed=embeds[cur])
                        elif str(reaction.emoji) == '⏪':
                            cur = 0
                            await message.edit(embed=embeds[cur])
                        elif str(reaction.emoji) == '⏩':
                            cur = len(embeds) - 1
                            await message.edit(embed=embeds[cur])
                        
                        await message.remove_reaction(reaction, user)
                        
                    except nextcord.NotFound:
                        break

            return
            
    else:
        embed = nextcord.Embed(
            title = "Error: Incorrectly formatted event URL",
            description = "**Example:** `https://start.gg/tournament/some-tourney/event/some-event`"
        )
    
    message_embed_color(embed)
    await interaction.followup.send(embed=embed)


@bot.slash_command(name="help", description="Help with Larry Lurr Bot")
async def help(interaction: Interaction, option: str = SlashOption(choices={
    "reactions": "reactions"
    }, description="Choose help option")):
    if option == "reactions":
        title = "If reactions are not working, please run the command again"
        description = "> - Only the user who used the command can change pages\n> - Reactions expire in 60 seconds of inactivity"
    
    embed = nextcord.Embed(
        title = title,
        description = description
    )    
    message_embed_color(embed)
    await interaction.response.send_message(embed=embed, ephemeral=True)

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
# bot.run('OTk5Nzc4NjMwMjg2NzA4ODI2.GwaPvU.mHwZ9zrLTwQ1ZiIByD9Yj5yb2Oj008YhbOXfJ0')  # Test

# refresh repo