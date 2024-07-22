import asyncio
import nextcord
import random as r
from nextcord import Interaction, InteractionMessage, SlashOption, SelectOption
# from nextcord.abc import GuildChannel
from nextcord.ext import commands
from nextcord.ui import View, Button
from typing import Optional
from graphql import getTop8, getSeeding
from patreon import getPatrons
import requests
from bs4 import BeautifulSoup
# from buttons import MyButtonMenu
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
import signal
from dotenv import load_dotenv
load_dotenv()

intents = nextcord.Intents.default()
# intents.message_content = True

# ENABLE WHEN MENTIONS APPROVED
# intents.members = True

bot = commands.Bot(intents=intents)

larry_count = 0

judge_dictionary = {}

total_fighters = 86

fighters = ['mario', 'donkey_kong', 'link', 'samus', 'dark_samus', 'yoshi', 'kirby', 'fox', 'pikachu', 'luigi', 'ness', 'captain_falcon', 'jigglypuff', 'peach', 'daisy', 'bowser', 'ice_climbers', 'sheik', 'zelda', 'dr_mario', 'pichu', 'falco', 'marth', 'lucina', 'young_link', 'ganondorf', 'mewtwo', 'roy', 'chrom', 'mr_game_and_watch', 'meta_knight', 'pit', 'dark_pit', 'zero_suit_samus', 'wario', 'snake', 'ike', 'pokemon_trainer', 'diddy_kong', 'lucas', 'sonic', 'king_dedede', 'olimar', 'lucario', 'rob', 'toon_link', 'wolf', 'villager', 'mega_man', 'wii_fit_trainer', 'rosalina_and_luma', 'little_mac', 'greninja', 'mii_brawler', 'mii_swordfighter', 'mii_gunner', 'palutena', 'pac_man', 'robin', 'shulk', 'bowser_jr', 'duck_hunt', 'ryu', 'ken', 'cloud', 'corrin', 'bayonetta', 'inkling', 'ridley', 'simon', 'richter', 'king_k_rool', 'isabelle', 'incineroar', 'piranha_plant', 'joker', 'dq_hero', 'banjo_and_kazooie', 'terry', 'byleth', 'minmin', 'steve', 'sephiroth', 'pyra', 'kazuya', 'sora']

# List of all characters in Smash Bros Ultimate
characters = [
    "Mario", "Donkey Kong", "Link", "Samus", "Dark Samus", "Yoshi", "Kirby", 
    "Fox", "Pikachu", "Luigi", "Ness", "Captain Falcon", "Jigglypuff", "Peach", 
    "Daisy", "Bowser", "Ice Climbers", "Sheik", "Zelda", "Dr. Mario", "Pichu", 
    "Falco", "Marth", "Lucina", "Young Link", "Ganondorf", "Mewtwo", "Roy", 
    "Chrom", "Mr. Game & Watch", "Meta Knight", "Pit", "Dark Pit", "Zero Suit Samus", 
    "Wario", "Snake", "Ike", "Pokémon Trainer", "Diddy Kong", "Lucas", "Sonic", 
    "King Dedede", "Olimar", "Lucario", "R.O.B.", "Toon Link", "Wolf", "Villager", 
    "Mega Man", "Wii Fit Trainer", "Rosalina & Luma", "Little Mac", "Greninja", 
    "Palutena", "Pac-Man", "Robin", "Shulk", "Bowser Jr.", "Duck Hunt", "Ryu", 
    "Ken", "Cloud", "Corrin", "Bayonetta", "Inkling", "Ridley", "Simon", "Richter", 
    "King K. Rool", "Isabelle", "Incineroar", "Piranha Plant", "Joker", "Hero", 
    "Banjo & Kazooie", "Terry", "Byleth", "Min Min", "Steve", "Sephiroth", 
    "Pyra/Mythra", "Kazuya", "Sora", "Mii Brawler", "Mii Swordfighter", "Mii Gunner"
]

fighter_emojis = {
    "Mario": "<:Mario:919488424212332585>",
    "Donkey Kong": "<:DonkeyKong:1078080099242496081>",
    "Link": "<:Link:1078095420565233796>",
    "Samus": "<:Samus:1078095742507425862>",
    "Dark Samus": "<:DarkSamus:1078080096440680530>",
    "Yoshi": "<:Yoshi:1078128416261410816>",
    "Kirby": "<:Kirby:919488424325578823>",
    "Fox": "<:Fox:1078080116514627594>",
    "Pikachu": "<:Pikachu:1078095698777608222>",
    "Luigi": "<:Luigi:1078095442761494548>",
    "Ness": "<:Ness:1078095551683379260>",
    "Captain Falcon": "<:CaptainFalcon:1078080073493643385>",
    "Jigglypuff": "<:Jigglypuff:1078095389879713792>",
    "Peach": "<:Peach:919488424015188000>",
    "Daisy": "<:Daisy:1078080080355524720>",
    "Bowser": "<:Bowser:1078080023879229530>",
    "Ice Climbers": "<:IceClimbers:1078095364067966986>",
    "Sheik": "<:Sheik:1078128428101947453>",
    "Zelda": "<:Zelda:1078128420514447410>",
    "Dr. Mario": "<:DrMario:1078080101058629793>",
    "Pichu": "<:Pichu:1078095697162817636>",
    "Falco": "<:Falco:1078080114778193922>",
    "Marth": "<:Marth:1078095519680839711>",
    "Lucina": "<:Lucina:1078095441180246096>",
    "Young Link": "<:YoungLink:1078128418064961636>",
    "Ganondorf": "<:Ganondorf:1078095320782749716>",
    "Mewtwo": "<:Mewtwo:1078095516790947840>",
    "Roy": "<:Roy:1078095739034554468>",
    "Chrom": "<:Chrom:1078080075771158649>",
    "Mr. Game & Watch": "<:MrGameWatch:1078095549812707358>",
    "Meta Knight": "<:MetaKnight:1078095515515887707>",
    "Pit": "<:Pit:1078095702669930596>",
    "Dark Pit": "<:DarkPit:1078080094393880597>",
    "Zero Suit Samus": "<:ZeroSuitSamus:1078128423563694161>",
    "Wario": "<:Wario:1078128410074828902>",
    "Snake": "<:Snake:1078128433609048104>",
    "Ike": "<:Ike:1078095365284307055>",
    "Pokémon Trainer": "<:PokemonTrainer:1078095703877886103>",
    "Diddy Kong": "<:DiddyKong:1078080097912901642>",
    "Lucas": "<:Lucas:1078095439758372865>",
    "Sonic": "<:Sonic:1078128434796036139>",
    "King Dedede": "<:KingDedede:1078095413850153051>",
    "Olimar": "<:Olimar:1078095705958273055>",
    "Lucario": "<:Lucario:1078095437510226022>",
    "R.O.B.": "<:ROB:1078095734190116945>",
    "Toon Link": "<:ToonLink:1078128802040905809>",
    "Wolf": "<:Wolf:1078128414550134844>",
    "Villager": "<:Villager:1078128445281812571>",
    "Mega Man": "<:MegaMan:1078095512978325606>",
    "Wii Fit Trainer": "<:WiiFitTrainer:1078128413186986044>",
    "Rosalina & Luma": "<:Rosalina:1078095737805619282>",
    "Little Mac": "<:LittleMac:1078095421286654108>",
    "Greninja": "<:Greninja:1078095322783432774>",
    "Palutena": "<:Palutena:1078095695510257665>",
    "Pac-Man": "<:PacMan:1078095693857701888>",
    "Robin": "<:Robin:1078095735888810105>",
    "Shulk": "<:Shulk:1078128430790492170>",
    "Bowser Jr.": "<:BowserJr:1078080024944582777>",
    "Duck Hunt": "<:DuckHunt:1078080113326968902>",
    "Ryu": "<:Ryu:1078095739865022465>",
    "Ken": "<:Ken:1078095394770255942>",
    "Cloud": "<:Cloud:1078080077276925962>",
    "Corrin": "<:Corrin:1078080078963015711>",
    "Bayonetta": "<:Bayonetta:1078080022662885556>",
    "Inkling": "<:Inkling:1078095368820109312>",
    "Ridley": "<:Ridley:1078095732696961024>",
    "Simon": "<:Simon:1078095774505775188>",
    "Richter": "<:Richter:1078095731619004576>",
    "King K. Rool": "<:KingKRool:1078095416492572672>",
    "Isabelle": "<:Isabelle:1078095387845480488>",
    "Incineroar": "<:Incineroar:1078095366525820978>",
    "Piranha Plant": "<:PiranhaPlant:1078095701470359592>",
    "Joker": "<:Joker:1078095391096053760>",
    "Hero": "<:Hero:1078095361719156736>",
    "Banjo & Kazooie": "<:BanjoKazooie:1078080020741885983>",
    "Terry": "<:Terry:1078128442198990948>",
    "Byleth": "<:Byleth:1078080026865569922>",
    "Min Min": "<:MinMin:1078095548646703266>",
    "Steve": "<:Steve:1078128439908909176>",
    "Sephiroth": "<:Sephiroth:1078128424956211251>",
    "Pyra/Mythra": "<:PyraMythra:1078095744004796576>",
    "Kazuya": "<:Kazuya:1078095392517931068>",
    "Sora": "<:Sora:1078128437539119224>",
    "Mii Brawler": "<:MiiBrawler:1078095517860495410>",
    "Mii Swordfighter": "<:MiiSwordfighter:1078095547480686612>",
    "Mii Gunner": "<:MiiGunner:1078095545568071751>"
}

mongo_uri = os.getenv("MONGODB_URI")
client = None
db = None

try:
    client = MongoClient(mongo_uri)
    client.admin.command('ismaster')
    db = client['Database']
    users_collection = db['Users']
    print("MongoDB connection successful.")
except ConnectionFailure:
    print("MongoDB connection failed.")

@bot.event
async def on_ready():
    game = nextcord.Game("SSBU")
    await bot.change_presence(activity=game)
    print("Bot is ready")  


def message_embed_color(embed):
    random_color = r.randint(0, 2)
    if random_color == 0:
        embed.colour = nextcord.Colour.from_rgb(85, 174, 131)
    elif random_color == 1:
        embed.colour = nextcord.Colour.from_rgb(40, 56, 106)
    else:
        embed.colour = nextcord.Colour.from_rgb(154, 38, 38)

@bot.slash_command(name = "my_elite", description = "View your Elite Smash stats")
async def my_elite(interaction: Interaction):
    user = interaction.user
    userID = str(user.id)
    user_data = users_collection.find_one({"userID": userID})

    if not user_data:
        embed = nextcord.Embed(title="Error", description="You do not have Elite Smash stats.")
        message_embed_color(embed)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    eliteRoster = user_data.get("eliteRoster", {})
    not_in_roster = total_fighters - sum(eliteRoster.values())

    percentage = "{:.2f}".format((sum(eliteRoster.values()) / total_fighters) * 100)
    description = "**In Elite:** `" + str(sum(eliteRoster.values())) + "/" + str(total_fighters) + "` - `" + percentage + "%`\n"
    description += "> " + "".join([fighter_emojis[char] if value else "" for char, value in eliteRoster.items()])
    description += "\n\n**Not In Elite:** `" + str(not_in_roster) + "/" + str(total_fighters) + "` - `" + "{:.2f}".format(((total_fighters - sum(eliteRoster.values())) / total_fighters) * 100) + "%`\n"
    description += "> " + "".join([fighter_emojis[char] if not value else "" for char, value in eliteRoster.items()])

    embed = nextcord.Embed(title="Elite Smash Stats", description=description)
    message_embed_color(embed)

    await interaction.response.send_message(embed=embed)


@bot.slash_command(name="compare_elite", description="Compare Elite Smash stats with another user")
async def compare_elite(interaction: Interaction, user: nextcord.User):
    user1 = interaction.user
    user2 = user
    user1ID = str(user1.id)
    user2ID = str(user2.id)
    user2name = user2.name

    user1_data = users_collection.find_one({"userID": user1ID})
    user2_data = users_collection.find_one({"userID": user2ID})

    if not user1_data or not user2_data:
        embed = nextcord.Embed(title="Error", description="One or both users do not have Elite Smash stats.")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    user1_eliteRoster = user1_data.get("eliteRoster", {})
    user2_eliteRoster = user2_data.get("eliteRoster", {})

    user1_in_elite = sum(user1_eliteRoster.values())
    user2_in_elite = sum(user2_eliteRoster.values())
    fighters_in_common = sum([1 for char in user1_eliteRoster if user1_eliteRoster[char] and user2_eliteRoster[char]])

    user1_percentage = "{:.2f}".format((user1_in_elite / total_fighters) * 100)
    user2_percentage = "{:.2f}".format((user2_in_elite / total_fighters) * 100)
    fighters_in_common_percentage = "{:.2f}".format((fighters_in_common / total_fighters) * 100)

    if user1_in_elite < user2_in_elite:
        description = "`" + user2.name + "` is `" + "{:.1f}".format(user2_in_elite / user1_in_elite) + "x` better than you!\n\n"
    elif user1_in_elite > user2_in_elite:
        description = "`" + user2.name + "` is `" + "{:.1f}".format(user1_in_elite / user2_in_elite) + "x` worse than you!\n\n"
    else:
        description = "You and `" + user2.name + "` have the same number of fighters in Elite Smash!\n\n"
    
    description += "**" + user1.name + ": ** `" + str(user1_in_elite) + "/" + str(total_fighters) + "` - `" + user1_percentage + "%`\n"
    description += "> " + "".join([fighter_emojis[char] if value else "" for char, value in user1_eliteRoster.items()])
    description += "\n\n**" + user2name + ": ** `" + str(user2_in_elite) + "/" + str(total_fighters) + "` - `" + user2_percentage + "%`\n"
    description += "> " + "".join([fighter_emojis[char] if value else "" for char, value in user2_eliteRoster.items()])
    description += "\n\n**Fighters in Common:** `" + str(fighters_in_common) + "/" + str(total_fighters) + "` - `" + fighters_in_common_percentage + "%`\n"
    description += "> " + "".join([fighter_emojis[char] if value and user2_eliteRoster[char] else "" for char, value in user1_eliteRoster.items()])

    embed = nextcord.Embed(title="Elite Smash Stats Comparison", description=description)
    message_embed_color(embed)
    await interaction.response.send_message(embed=embed)


@bot.slash_command(name="modify_elite", description="Add or remove Elite Smash fighters")
async def modify_elite(interaction: Interaction, 
                action: str = SlashOption(
                    name="action",
                    description="Add or remove your fighter from Elite roster",
                    choices={"Add": "Add", "Remove": "Remove", "Add All": "Add All", "Remove All": "Remove All"},
                    required=True
                ),
                fighter: str = SlashOption(
                    name="fighter",
                    description="Choose your fighter",
                    required=True
                )):
    user = interaction.user
    userID = str(user.id)
    eliteRoster = {}
    description = ""

    if action == "Add":
        user_data = users_collection.find_one({"userID": userID})
        if not user_data:
            eliteRoster = {char: False for char in characters}
            eliteRoster[fighter] = True
            users_collection.insert_one({"userID": userID, "eliteRoster": eliteRoster})
        else:
            eliteRoster = user_data["eliteRoster"]
            eliteRoster[fighter] = True
            users_collection.update_one({"userID": userID}, {"$set": {"eliteRoster": eliteRoster}})
        description = "Added " + fighter_emojis[fighter] + " to your Elite roster!\n\n"
    elif action == "Remove":
        user_data = users_collection.find_one({"userID": userID})
        if not user_data:
            embed = nextcord.Embed(title="Error: User not found")
            message_embed_color(embed)
            await interaction.response.send_message(embed=embed)
            return
        else:
            eliteRoster = user_data["eliteRoster"]
            eliteRoster[fighter] = False
            users_collection.update_one({"userID": userID}, {"$set": {"eliteRoster": eliteRoster}})
            description = "Removed " + fighter_emojis[fighter] + " from your Elite roster!\n\n"
    elif action == "Add All":
        user_data = users_collection.find_one({"userID": userID})
        if not user_data:
            eliteRoster = {char: True for char in characters}
            users_collection.insert_one({"userID": userID, "eliteRoster": eliteRoster})
        else:
            eliteRoster = user_data["eliteRoster"]
            eliteRoster = {char: True for char in eliteRoster}
            users_collection.update_one({"userID": userID}, {"$set": {"eliteRoster": eliteRoster}})
        description = "Added all fighters to your Elite roster!\n\n"
    elif action == "Remove All":
        user_data = users_collection.find_one({"userID": userID})
        if not user_data:
            embed = nextcord.Embed(title="Error: User not found")
            message_embed_color(embed)
            await interaction.response.send_message(embed=embed)
            return
        else:
            eliteRoster = user_data["eliteRoster"]
            eliteRoster = {char: False for char in eliteRoster}
            users_collection.update_one({"userID": userID}, {"$set": {"eliteRoster": eliteRoster}})
            description = "Removed all fighters from your Elite roster!\n\n"
    
    not_in_roster = total_fighters - sum(eliteRoster.values())

    percentage = "{:.2f}".format((sum(eliteRoster.values()) / total_fighters) * 100)
    description += "**In Elite:** `" + str(sum(eliteRoster.values())) + "/" + str(total_fighters) + "` - `" + percentage + "%`\n"
    description += "> " + "".join([fighter_emojis[char] if value else "" for char, value in eliteRoster.items()])
    description += "\n\n**Not In Elite:** `" + str(not_in_roster) + "/" + str(total_fighters) + "` - `" + "{:.2f}".format(((total_fighters - sum(eliteRoster.values())) / total_fighters) * 100) + "%`\n"
    description += "> " + "".join([fighter_emojis[char] if not value else "" for char, value in eliteRoster.items()])

    embed = nextcord.Embed(title="Elite Smash Stats", description=description)
    message_embed_color(embed)

    await interaction.response.send_message(embed=embed)



@modify_elite.on_autocomplete("fighter")
async def fighter_autocomplete(interaction: Interaction, fighter: str, action: str):
    if action == "Add All" or action == "Remove All":
        await interaction.response.send_autocomplete(["All Fighters"])
        return

    if not fighter:
        # Send the full autocomplete list trimmed to 25
        await interaction.response.send_autocomplete(characters[:25])
        return
    
    # Send a list of nearest matches from the list of fighters
    get_near_fighter = [char for char in characters if char.lower().startswith(fighter.lower())]
    await interaction.response.send_autocomplete(get_near_fighter[:25])



@bot.slash_command(name="larry", description="Larry image")
async def larry(interaction: Interaction, image: str = SlashOption(choices={
    "random": "random",
    "finger": "https://github.com/chriscolomb/ssbu/raw/master/larry/larry_11.png",
    "33": "https://github.com/chriscolomb/ssbu/raw/master/larry/larry_51.png",
    "drip": "https://github.com/chriscolomb/ssbu/raw/master/larry/larry_62.png"
    }, description="Choose image type"), message: Optional[str] = SlashOption(required=False, description="Image title")):

    global larry_count
    if image == "random":
        if larry_count == 0 or message == "refresh":
            # Fetch the text file from the URL
            url = "https://raw.githubusercontent.com/chriscolomb/ssbu/master/larry/larry_count.txt"
            response = requests.get(url)
            text_content = response.text
            larry_count = int(text_content.strip())

        image = "https://github.com/chriscolomb/ssbu/raw/master/larry/larry_" + str(r.randint(0, larry_count)) + ".png"
    
    embed = nextcord.Embed(
        title = message
    )    
    embed.set_image(url=image)
    message_embed_color(embed)
    await interaction.response.send_message(embed=embed)


@bot.slash_command(name="random", description="Random character portrait")
async def random(interaction: Interaction, message: Optional[str] = SlashOption(required=False, description="Image title")):
    
    fighter = None

    # For Bree Custom Command
    if message:
        if str(interaction.user.id) == "246065356773392385" and "ike" in message.lower():
            fighter = "ike"
    
    if not fighter:
        fighter = fighters[r.randint(0, len(fighters) - 1)]
    
    if fighter == "mii_brawler":
        alt = str(r.randint(0, 1))
    elif fighter == "mii_swordfighter":
        alt = '0'
    elif fighter == "mii_gunner":
        alt = str(r.randint(0, 2))
    else:
        alt = str(r.randint(0, 7))
    
    random_image = "https://github.com/chriscolomb/ssbu/raw/master/portraits/fighters/" + fighter + '/' + alt + ".png"

    embed = nextcord.Embed(
        title = message
    )
    embed.set_image(url=random_image)
    message_embed_color(embed)
    await interaction.response.send_message(embed=embed)


# @bot.slash_command(name="ridley", description="Random Ridley portrait")
# async def ridley(interaction: Interaction, message: Optional[str] = SlashOption(required=False, description="Image title")):
#     ridley_image = "https://github.com/chriscolomb/ssbu/raw/master/ridley/ridley_" + str(r.randint(0, 7)) + ".png"

#     embed = nextcord.Embed(
#         title = message
#     )
#     embed.set_image(url=ridley_image)
#     message_embed_color(embed)
#     await interaction.response.send_message(embed=embed)


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
    event = ""

    for i in range(len(split)):
        if split[i] == "tournament":
            tournament = split[i+1]
        elif split[i] == "event":
            if split[i+1]:
                event = split[i+1]
    
    if event == "":
        event = "ultimate-singles"
    
    embed = nextcord.Embed()
        
    if tournament and event:
        top8_info = getTop8(tournament, event)
        if len(top8_info) == 0:
            event = "super-smash-bros-ultimate-singles"
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
            # print(top8_info)
            if "ladder" in event:
                for i in range(len(top8_info[4])):
                    if i == 0:
                        top8 = top8 + "> `1st` "
                    elif i == 1:
                        top8 = top8 + "> `2nd` "
                    elif i == 2:
                        top8 = top8 + "> `3rd` "
                    elif i == 3:
                        top8 = top8 + "> `4th` "
                    elif i == 4:
                        top8 = top8 + "> `5th` "
                    elif i == 5:
                        top8 = top8 + "> `6th` "
                    elif i == 6:
                        top8 = top8 + "> `7th` "
                    else:
                        top8 = top8 + "> `8th` "
                    top8 = top8 + top8_info[4][i][0] + "\n"
            else:
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
    event = ""

    for i in range(len(split)):
        if split[i] == "tournament":
            tournament = split[i+1]
        elif split[i] == "event":
            if split[i+1]:
                event = split[i+1]
    
    if event == "":
        event = "ultimate-singles"
    
    embed = nextcord.Embed()

    await interaction.response.defer()
        
    if tournament and event:
        seeding = getSeeding(tournament, event)
        if len(seeding) == 0:
            event = "super-smash-bros-ultimate-singles"
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
                if seeding[2] > 16:
                    embed.set_footer(text=seeding[3] + "\n" + "⬇ Reactions don't work? Use \"/help reactions\"")
                else: embed.set_footer(text=seeding[3])
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
        embed = nextcord.Embed(
            title = "Help with Reactions",
            description = "Due to timeout, you may need to run the command again"
        ) 
        general_description = "> - Only the user who used the command can change pages\n"\
                        + "> - Reactions expire in 60 seconds of inactivity"
        permissions_description = "Make sure Larry Lurr Bot has the following permissions:\n"\
                        + "> - Add Reactions\n"\
                        + "> - Manage Messages"
        embed.add_field(name="General", value=general_description)
        embed.add_field(name="Permissions", value=permissions_description)
    
       
    message_embed_color(embed)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.slash_command(name="patrons", description="See patrons of Larry Lurr Bot")
async def patrons(interaction: Interaction):
    patrons = getPatrons()
    embed = nextcord.Embed(
        title = "Patrons of Larry Lurr Bot",
        description = "A special thanks to these patrons for supporting the bot!"
    )
    tier_count = 0
    
    for tier in patrons:
        if len(tier) != 0:
            if tier_count == 0:
                tier_name = "Commandin' Larry"
            elif tier_count == 1:
                tier_name = "Livin' Like Larry"
            else:
                tier_name = "Tippin' Larry"
            
            tier_patrons = ""
            for patron in tier:
                tier_patrons = tier_patrons + "> " + patron + "\n"    
            embed.add_field(name=tier_name, value=tier_patrons)
        
        tier_count += 1
    
    embed.set_footer(text="Want to become a patron? Visit the Patreon link in Larry's bio!")
    embed.set_thumbnail(url="https://github.com/chriscolomb/ssbu/raw/master/larry/patreon_logo.png")

    message_embed_color(embed)
    await interaction.response.send_message(embed=embed)



# @bot.slash_command(name="matchbox", description="See MatchBox ranking")
# async def matchbox(interaction: Interaction):
#     url = "https://smashpros.gg/user/teamduck"

#     # Fetch the HTML content from the URL
#     response = requests.get(url)
#     html_content = response.text

#     # Parse the HTML using BeautifulSoup
#     soup = BeautifulSoup(html_content, 'html.parser')

#     # Extract the desired information
#     mmr_element = soup.find('div', class_='v-list-item-subtitle')  # Assuming the MMR is inside a div with this class
#     mmr = mmr_element.text.strip().split()[0]  # Extracting the numerical part of the MMR

#     win_loss_element = soup.find('span', class_='font-weight-bold text-green')  # Assuming the win count is inside a span with this class
#     win_count = win_loss_element.text.strip().split()[0]  # Extracting the numerical part of the win count

#     loss_element = soup.find('span', class_='font-weight-bold text-red')  # Assuming the loss count is inside a span with this class
#     loss_count = loss_element.text.strip().split()[0]  # Extracting the numerical part of the loss count


#     embed = nextcord.Embed(
#         title = "MatchBox Ranking for TeamDuck",
#         description = "MMR: " + mmr + "\n" + "Wins: " + win_count + "\n" + "Losses: " + loss_count
#     )
    
    
#     message_embed_color(embed)
#     await interaction.response.send_message(embed=embed)


# @bot.slash_command(name="workout", description="Workout and Smash!")
# @bot.command()
# async def menu_example(interaction: Interaction, user: nextcord.User):
#     await MyButtonMenu().start(interaction)
# async def workout(interaction: Interaction, user: nextcord.User):
#     p1 = interaction.user
#     p2 = user
#     embed = nextcord.Embed(
#         description = f"{p2.mention}, **Workout and Smash** with {p1.name}?",
#     )
#     message_embed_color(embed)
#     await interaction.response.send_message(embed=embed)

#     # Create a yes/no button view
#     view = View()
#     view.add_item(Button(style=nextcord.ButtonStyle.green, label="Yes", custom_id="yes"))
#     view.add_item(Button(style=nextcord.ButtonStyle.red, label="No", custom_id="no"))

#     await interaction.edit_original_message(view=view, embed=embed)

#     if interaction.custom_id == "yes":
#             # Modify the view or perform an action here
#             embed = nextcord.Embed(
#                 description = "You clicked yes!",
#             )
#             await interaction.edit_original_message(view=view, embed=embed)

#     # @bot.event
#     # async def on_yes(interaction):
        
#             # await interaction.message.edit("You clicked the Yes button!", ephemeral=True)
#             # You can modify the view or take further action as needed

#     try:
#         response = await bot.wait_for("button_click", timeout=900, check=lambda i: i.custom_id in ["yes", "no"])
#         if response.custom_id == "yes":
#             await interaction.send(f"What workouts do you want to include, {target.mention}?")

#             # Create a picklist with workout options
#             workout_options = [
#                 SelectOption(label="Push-Ups", value="pushups"),
#                 SelectOption(label="Squats", value="squats"),
#                 SelectOption(label="Pull-Ups", value="pullups"),
#             ]
#             workout_select = SelectOption(options=workout_options, custom_id="workout_select")

#             await interaction.response.edit_message("Choose the workouts you want to include:", view=workout_select)

#             try:
#                 workout_response = await bot.wait_for("select_option", timeout=900, check=lambda i: i.custom_id == "workout_select")
#                 selected_workouts = [option.value for option in workout_response.selected_options]

#                 if not selected_workouts:
#                     await interaction.send("No workouts selected.")
#                 else:
#                     await interaction.send("Do you want to include more workouts?")

#                     # Create a picklist with yes/no options for more workouts
#                     more_workouts_options = [
#                         SelectOption(label="No", value="no"),
#                         SelectOption(label="Not selected workouts", value="not_selected"),
#                     ]
#                     more_workouts_select = Select(options=more_workouts_options, custom_id="more_workouts_select")

#                     await interaction.send("Choose an option:", view=more_workouts_select)

#                     try:
#                         more_workouts_response = await bot.wait_for("select_option", timeout=900, check=lambda i: i.custom_id == "more_workouts_select")
#                         if more_workouts_response.values[0] == "no":
#                             await interaction.send("No more workouts will be added.")
#                         elif more_workouts_response.values[0] == "not_selected":
#                             await interaction.send("How many reps per stock taken? (Please reply with a number)")

#                             def is_valid_number(message):
#                                 return message.content.isdigit()

#                             reps_message = await bot.wait_for("message", timeout=900, check=is_valid_number)
#                             reps_per_stock = int(reps_message.content)

#                             await interaction.send("Let the workout begin! How many stocks left?")

#                             # Create buttons for stock count
#                             view = View()
#                             for i in range(4):
#                                 view.add_item(Button(style=nextcord.ButtonStyle.primary, label=str(i), custom_id=str(i)))
#                             await interaction.send(view=view)

#                             async def wait_for_buttons():
#                                 while True:
#                                     try:
#                                         button_response = await bot.wait_for("button_click", timeout=900, check=lambda i: i.custom_id in ["0", "1", "2", "3"])
#                                         await interaction.send(
#                                             f"{author.mention} has taken {button_response.custom_id} stocks, and {target.mention} has taken {button_response.custom_id} stocks. "
#                                             f"They each did {reps_per_stock} reps per stock."
#                                         )
#                                     except nextcord.errors.NotFound:
#                                         break

#                             await wait_for_buttons()
#                     except asyncio.TimeoutError:
#                         await interaction.send("Timed out. No more workouts will be added.")
#             except asyncio.TimeoutError:
#                 await interaction.send("Timed out. No workouts selected.")
#         elif response.custom_id == "no":
#             await interaction.send(f"{target.mention} declined the workout.")
#     except asyncio.TimeoutError:
#         await interaction.send("Timed out. No response received.")




# @bot.slash_command(name="edit", description="Edit Larry's message")
# async def edit(interaction: Interaction, option: str = SlashOption(choices = {"graphic": "graphic"}, description="Choose edit option")):
#     # get the message object by ID
#     message = await ctx.channel.fetch_message(message_id)
    
#     # modify the image in the embed
#     embed = message.embeds[0]  # assuming there's only one embed in the message
#     embed.set_image(url=image_url)

#     # update the message with the modified embed
#     await message.edit(embed=embed)

#     # send a confirmation message
#     await ctx.send(f"Image of message {message_id} has been updated to {image_url}")


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

def shutdown_handler(signum, frame):
    print('Received signal {}. Shutting down...'.format(signum))
    if client:
        client.close()
        print("MongoDB connection closed.")
    exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

# bot.run(os.getenv('PROD_BOT_TOKEN'))  # Production
bot.run(os.getenv('TEST_BOT_TOKEN'))  # Testing



# refresh repo

