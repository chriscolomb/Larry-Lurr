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
from pymongo import MongoClient, errors
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

# Define the fighters dictionary as a global variable
fighters = {
    "Mario": {"url": "mario", "emoji": "<:Mario:919488424212332585>"},
    "Donkey Kong": {"url": "donkey_kong", "emoji": "<:DonkeyKong:1078080099242496081>"},
    "Link": {"url": "link", "emoji": "<:Link:1078095420565233796>"},
    "Samus": {"url": "samus", "emoji": "<:Samus:1078095742507425862>"},
    "Dark Samus": {"url": "dark_samus", "emoji": "<:DarkSamus:1078080096440680530>"},
    "Yoshi": {"url": "yoshi", "emoji": "<:Yoshi:1078128416261410816>"},
    "Kirby": {"url": "kirby", "emoji": "<:Kirby:919488424325578823>"},
    "Fox": {"url": "fox", "emoji": "<:Fox:1078080116514627594>"},
    "Pikachu": {"url": "pikachu", "emoji": "<:Pikachu:1078095698777608222>"},
    "Luigi": {"url": "luigi", "emoji": "<:Luigi:1078095442761494548>"},
    "Ness": {"url": "ness", "emoji": "<:Ness:1078095551683379260>"},
    "Captain Falcon": {"url": "captain_falcon", "emoji": "<:CaptainFalcon:1078080073493643385>"},
    "Jigglypuff": {"url": "jigglypuff", "emoji": "<:Jigglypuff:1078095389879713792>"},
    "Peach": {"url": "peach", "emoji": "<:Peach:919488424015188000>"},
    "Daisy": {"url": "daisy", "emoji": "<:Daisy:1078080080355524720>"},
    "Bowser": {"url": "bowser", "emoji": "<:Bowser:1078080023879229530>"},
    "Ice Climbers": {"url": "ice_climbers", "emoji": "<:IceClimbers:1078095364067966986>"},
    "Sheik": {"url": "sheik", "emoji": "<:Sheik:1078128428101947453>"},
    "Zelda": {"url": "zelda", "emoji": "<:Zelda:1078128420514447410>"},
    "Dr. Mario": {"url": "dr_mario", "emoji": "<:DrMario:1078080101058629793>"},
    "Pichu": {"url": "pichu", "emoji": "<:Pichu:1078095697162817636>"},
    "Falco": {"url": "falco", "emoji": "<:Falco:1078080114778193922>"},
    "Marth": {"url": "marth", "emoji": "<:Marth:1078095519680839711>"},
    "Lucina": {"url": "lucina", "emoji": "<:Lucina:1078095441180246096>"},
    "Young Link": {"url": "young_link", "emoji": "<:YoungLink:1078128418064961636>"},
    "Ganondorf": {"url": "ganondorf", "emoji": "<:Ganondorf:1078095320782749716>"},
    "Mewtwo": {"url": "mewtwo", "emoji": "<:Mewtwo:1078095516790947840>"},
    "Roy": {"url": "roy", "emoji": "<:Roy:1078095739034554468>"},
    "Chrom": {"url": "chrom", "emoji": "<:Chrom:1078080075771158649>"},
    "Mr. Game & Watch": {"url": "mr_game_and_watch", "emoji": "<:MrGameWatch:1078095549812707358>"},
    "Meta Knight": {"url": "meta_knight", "emoji": "<:MetaKnight:1078095515515887707>"},
    "Pit": {"url": "pit", "emoji": "<:Pit:1078095702669930596>"},
    "Dark Pit": {"url": "dark_pit", "emoji": "<:DarkPit:1078080094393880597>"},
    "Zero Suit Samus": {"url": "zero_suit_samus", "emoji": "<:ZeroSuitSamus:1078128423563694161>"},
    "Wario": {"url": "wario", "emoji": "<:Wario:1078128410074828902>"},
    "Snake": {"url": "snake", "emoji": "<:Snake:1078128433609048104>"},
    "Ike": {"url": "ike", "emoji": "<:Ike:1078095365284307055>"},
    "Pokémon Trainer": {"url": "pokemon_trainer", "emoji": "<:PokemonTrainer:1078095703877886103>"},
    "Diddy Kong": {"url": "diddy_kong", "emoji": "<:DiddyKong:1078080097912901642>"},
    "Lucas": {"url": "lucas", "emoji": "<:Lucas:1078095439758372865>"},
    "Sonic": {"url": "sonic", "emoji": "<:Sonic:1078128434796036139>"},
    "King Dedede": {"url": "king_dedede", "emoji": "<:KingDedede:1078095413850153051>"},
    "Olimar": {"url": "olimar", "emoji": "<:Olimar:1078095705958273055>"},
    "Lucario": {"url": "lucario", "emoji": "<:Lucario:1078095437510226022>"},
    "R.O.B.": {"url": "rob", "emoji": "<:ROB:1078095734190116945>"},
    "Toon Link": {"url": "toon_link", "emoji": "<:ToonLink:1078128802040905809>"},
    "Wolf": {"url": "wolf", "emoji": "<:Wolf:1078128414550134844>"},
    "Villager": {"url": "villager", "emoji": "<:Villager:1078128445281812571>"},
    "Mega Man": {"url": "mega_man", "emoji": "<:MegaMan:1078095512978325606>"},
    "Wii Fit Trainer": {"url": "wii_fit_trainer", "emoji": "<:WiiFitTrainer:1078128413186986044>"},
    "Rosalina & Luma": {"url": "rosalina_and_luma", "emoji": "<:Rosalina:1078095737805619282>"},
    "Little Mac": {"url": "little_mac", "emoji": "<:LittleMac:1078095421286654108>"},
    "Greninja": {"url": "greninja", "emoji": "<:Greninja:1078095322783432774>"},
    "Palutena": {"url": "palutena", "emoji": "<:Palutena:1078095695510257665>"},
    "Pac-Man": {"url": "pac_man", "emoji": "<:PacMan:1078095693857701888>"},
    "Robin": {"url": "robin", "emoji": "<:Robin:1078095735888810105>"},
    "Shulk": {"url": "shulk", "emoji": "<:Shulk:1078128430790492170>"},
    "Bowser Jr.": {"url": "bowser_jr", "emoji": "<:BowserJr:1078080024944582777>"},
    "Duck Hunt": {"url": "duck_hunt", "emoji": "<:DuckHunt:1078080113326968902>"},
    "Ryu": {"url": "ryu", "emoji": "<:Ryu:1078095739865022465>"},
    "Ken": {"url": "ken", "emoji": "<:Ken:1078095394770255942>"},
    "Cloud": {"url": "cloud", "emoji": "<:Cloud:1078080077276925962>"},
    "Corrin": {"url": "corrin", "emoji": "<:Corrin:1078080078963015711>"},
    "Bayonetta": {"url": "bayonetta", "emoji": "<:Bayonetta:1078080022662885556>"},
    "Inkling": {"url": "inkling", "emoji": "<:Inkling:1078095368820109312>"},
    "Ridley": {"url": "ridley", "emoji": "<:Ridley:1078095732696961024>"},
    "Simon": {"url": "simon", "emoji": "<:Simon:1078095774505775188>"},
    "Richter": {"url": "richter", "emoji": "<:Richter:1078095731619004576>"},
    "King K. Rool": {"url": "king_k_rool", "emoji": "<:KingKRool:1078095416492572672>"},
    "Isabelle": {"url": "isabelle", "emoji": "<:Isabelle:1078095387845480488>"},
    "Incineroar": {"url": "incineroar", "emoji": "<:Incineroar:1078095366525820978>"},
    "Piranha Plant": {"url": "piranha_plant", "emoji": "<:PiranhaPlant:1078095701470359592>"},
    "Joker": {"url": "joker", "emoji": "<:Joker:1078095391096053760>"},
    "Hero": {"url": "dq_hero", "emoji": "<:Hero:1078095361719156736>"},
    "Banjo & Kazooie": {"url": "banjo_and_kazooie", "emoji": "<:BanjoKazooie:1078080020741885983>"},
    "Terry": {"url": "terry", "emoji": "<:Terry:1078128442198990948>"},
    "Byleth": {"url": "byleth", "emoji": "<:Byleth:1078080026865569922>"},
    "Min Min": {"url": "minmin", "emoji": "<:MinMin:1078095548646703266>"},
    "Steve": {"url": "steve", "emoji": "<:Steve:1078128439908909176>"},
    "Sephiroth": {"url": "sephiroth", "emoji": "<:Sephiroth:1078128424956211251>"},
    "Pyra/Mythra": {"url": "pyra", "emoji": "<:PyraMythra:1078095744004796576>"},
    "Kazuya": {"url": "kazuya", "emoji": "<:Kazuya:1078095392517931068>"},
    "Sora": {"url": "sora", "emoji": "<:Sora:1078128437539119224>"},
    "Mii Brawler": {"url": "mii_brawler", "emoji": "<:MiiBrawler:1078095517860495410>"},
    "Mii Swordfighter": {"url": "mii_swordfighter", "emoji": "<:MiiSwordfighter:1078095547480686612>"},
    "Mii Gunner": {"url": "mii_gunner", "emoji": "<:MiiGunner:1078095545568071751>"}
}
fighters_list = list(fighters.keys())

mongo_uri = os.getenv("MONGODB_URI")
client = None
db = None

try:
    client = MongoClient(mongo_uri)
    client.admin.command('ismaster')
    db = client['Database']
    users_collection = db['Users']
    print("MongoDB connection successful.")
except errors.ConnectionFailure as e:
    print(f"MongoDB connection failed: {e}")
except errors.ConfigurationError as e:
    print(f"MongoDB configuration error: {e}")
except errors.ServerSelectionTimeoutError as e:
    print(f"MongoDB server selection timeout: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

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
    description += "> " + "".join([fighters[char]["emoji"] if value else "" for char, value in eliteRoster.items()])
    if not_in_roster != 0:
        description += "\n\n**Not In Elite:** `" + str(not_in_roster) + "/" + str(total_fighters) + "` - `" + "{:.2f}".format(((total_fighters - sum(eliteRoster.values())) / total_fighters) * 100) + "%`\n"
        description += "> " + "".join([fighters[char]["emoji"] if not value else "" for char, value in eliteRoster.items()])

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
        description1 = "`" + user2.name + "` is `" + "{:.1f}".format(user2_in_elite / user1_in_elite) + "x` better than you!\n\n"
    elif user1_in_elite > user2_in_elite:
        description1 = "`" + user2.name + "` is `" + "{:.1f}".format(user1_in_elite / user2_in_elite) + "x` worse than you!\n\n"
    else:
        description1 = "You and `" + user2.name + "` have the same number of fighters in Elite Smash!\n\n"
    
    description1 += "**" + user1.name + ": ** `" + str(user1_in_elite) + "/" + str(total_fighters) + "` - `" + user1_percentage + "%`\n"
    description1 += "> " + "".join([fighters[char]["emoji"] if value else "" for char, value in user1_eliteRoster.items()])
    description2 = "**" + user2name + ": ** `" + str(user2_in_elite) + "/" + str(total_fighters) + "` - `" + user2_percentage + "%`\n"
    description2 += "> " + "".join([fighters[char]["emoji"] if value else "" for char, value in user2_eliteRoster.items()])

    description3 = "**Fighters in Common:** `" + str(fighters_in_common) + "/" + str(total_fighters) + "` - `" + fighters_in_common_percentage + "%`\n"
    description3 += "> " + "".join([fighters[char]["emoji"] if value and user2_eliteRoster[char] else "" for char, value in user1_eliteRoster.items()])

    if (len(description1)+len(description2)+len(description3)) < 4096:
        embed = nextcord.Embed(title="Elite Smash Stats Comparison", description=description1 + "\n\n" + description2 + "\n\n" + description3)
        message_embed_color(embed)
        await interaction.response.send_message(embed=embed)
        return

    embed1 = nextcord.Embed(title="Elite Smash Stats Comparison", description=description1)
    embed2 = nextcord.Embed(title="Elite Smash Stats Comparison (Continued)", description=description2)
    embed3 = nextcord.Embed(title="Elite Smash Stats Comparison (Continued)", description=description3)
    reaction_help = "⬇ Reactions don't work? Use \"/help reactions\""
    embed1.set_footer(text=reaction_help)
    embed2.set_footer(text=reaction_help)
    embed3.set_footer(text=reaction_help)
    message_embed_color(embed1)
    message_embed_color(embed2)
    message_embed_color(embed3)

    embeds = [embed1, embed2, embed3]
    
    cur = 0
    await interaction.response.send_message(embed=embeds[cur])
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
            eliteRoster = {char: False for char in fighters_list}
            eliteRoster[fighter] = True
            users_collection.insert_one({"userID": userID, "eliteRoster": eliteRoster})
        else:
            eliteRoster = user_data["eliteRoster"]
            eliteRoster[fighter] = True
            users_collection.update_one({"userID": userID}, {"$set": {"eliteRoster": eliteRoster}})
        description = "Added " + fighters[fighter]["emoji"] + " to your Elite roster!\n\n"
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
            description = "Removed " + fighters[fighter]["emoji"] + " from your Elite roster!\n\n"
    elif action == "Add All":
        user_data = users_collection.find_one({"userID": userID})
        if not user_data:
            eliteRoster = {char: True for char in fighters_list}
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
    description += "> " + "".join([fighters[char]["emoji"] if value else "" for char, value in eliteRoster.items()])
    if not_in_roster != 0:
        description += "\n\n**Not In Elite:** `" + str(not_in_roster) + "/" + str(total_fighters) + "` - `" + "{:.2f}".format(((total_fighters - sum(eliteRoster.values())) / total_fighters) * 100) + "%`\n"
        description += "> " + "".join([fighters[char]["emoji"] if not value else "" for char, value in eliteRoster.items()])

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
        await interaction.response.send_autocomplete(fighters_list[:25])
        return
    
    # Send a list of nearest matches from the list of fighters
    get_near_fighter = [char for char in fighters_list if char.lower().startswith(fighter.lower())]
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
        fighter = fighters[r.choice(fighters_list)]["url"]
    
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


class ChallengeView(View):
    def __init__(self, interaction, completed_fighters, remaining_fighters, current_fighter, timeout=900):
        super().__init__(timeout=timeout)
        self.interaction = interaction
        self.completed_fighters = completed_fighters
        self.remaining_fighters = remaining_fighters
        self.current_fighter = current_fighter

    @nextcord.ui.button(label="Win", style=nextcord.ButtonStyle.green)
    async def win_button(self, button: Button, interaction: Interaction):
        if interaction.user != self.interaction.user:
            await interaction.response.send_message("You are not authorized to use this button.", ephemeral=True)
            return

        self.completed_fighters[self.current_fighter] = True
        self.remaining_fighters.remove(self.current_fighter)
        if len(self.remaining_fighters) == 0:
            description = "Congrats, `" + interaction.user.name + "`! You completed the Ironman Challenge!"
            description += "\n\n**Completed Fighters:**\n"
            description += "> " + "".join([fighters[char]["emoji"] for char, value in self.completed_fighters.items() if value])
            embed = nextcord.Embed(
                title="Ironman Challenge",
                description=description
            )
            message_embed_color(embed)
            await interaction.message.edit(embed=embed, view=None)
        else:
            self.current_fighter = self.remaining_fighters[0]
            await self.update_embed(interaction)

    @nextcord.ui.button(label="Lose", style=nextcord.ButtonStyle.red)
    async def lose_button(self, button: Button, interaction: Interaction):
        if interaction.user != self.interaction.user:
            await interaction.response.send_message("You are not authorized to use this button.", ephemeral=True)
            return

        completed_count = sum(self.completed_fighters.values())
        percentage = "{:.2f}".format((completed_count / len(self.completed_fighters)) * 100)
        description = "Thanks for playing! You completed " + str(completed_count) + "/86 (" + percentage + "%) fighters!"
        description += "\n\n**Completed Fighters:**\n"
        if not any(self.completed_fighters.values()):
            description += "> `None`"
        else:
            description += "> " + "".join([fighters[char]["emoji"] if value else "" for char, value in self.completed_fighters.items()])
        description += "\n\n**Remaining Fighters:**\n"
        description += "> " + "".join([fighters[char]["emoji"] for char in self.remaining_fighters])
        embed = nextcord.Embed(
            title="Ironman Challenge",
            description=description
        )
        message_embed_color(embed)
        await interaction.message.edit(embed=embed, view=None)

    async def update_embed(self, interaction: Interaction):
        fighter = self.current_fighter
        fighter_url = fighters[fighter]["url"]

        if fighter_url == "mii_brawler":
            alt = str(r.randint(0, 1))
        elif fighter_url == "mii_swordfighter":
            alt = '0'
        elif fighter_url == "mii_gunner":
            alt = str(r.randint(0, 2))
        else:
            alt = str(r.randint(0, 7))

        random_image = "https://github.com/chriscolomb/ssbu/raw/master/portraits/fighters/" + fighter_url + '/' + alt + ".png"

        description = "Play as " + fighters[fighter]["emoji"] + " in your next match!"
        description += "\n\n**Completed Fighters:**\n"
        description += "> " + "".join([fighters[char]["emoji"] for char, value in self.completed_fighters.items() if value])
        description += "\n\n**Remaining Fighters:**\n"
        description += "> " + "".join([fighters[char]["emoji"] for char in self.remaining_fighters])

        embed = nextcord.Embed(
            title="Ironman Challenge",
            description=description
        )
        embed.set_image(url=random_image)
        completed_count = sum(self.completed_fighters.values())
        percentage = "{:.2f}".format((completed_count / len(self.completed_fighters)) * 100)
        footer = str(completed_count) + "/86 (" + percentage + "%) fighters completed!\nWin or Lose?"
        embed.set_footer(text=footer)
        message_embed_color(embed)
        await interaction.message.edit(embed=embed, view=self)

@bot.slash_command(name="ironman", description="Ironman challenge")
async def ironman(interaction: Interaction):
    remaining_fighters = list(fighters.keys())
    r.shuffle(remaining_fighters)
    completed_fighters = {fighter: False for fighter in remaining_fighters}

    current_fighter = remaining_fighters[0]
    fighter_url = fighters[current_fighter]["url"]

    if fighter_url == "mii_brawler":
        alt = str(r.randint(0, 1))
    elif fighter_url == "mii_swordfighter":
        alt = '0'
    elif fighter_url == "mii_gunner":
        alt = str(r.randint(0, 2))
    else:
        alt = str(r.randint(0, 7))

    random_image = "https://github.com/chriscolomb/ssbu/raw/master/portraits/fighters/" + fighter_url + '/' + alt + ".png"

    description = "Play as " + fighters[current_fighter]["emoji"] + " in your next match!"
    description += "\n\n**Completed Fighters:**\n"
    description += "> `None`"
    description += "\n\n**Remaining Fighters:**\n"
    description += "> " + "".join([fighters[char]["emoji"] for char in remaining_fighters])

    embed = nextcord.Embed(
        title="Ironman Challenge",
        description=description
    )
    embed.set_image(url=random_image)
    embed.set_footer(text="Win or Lose?")
    message_embed_color(embed)
    view = ChallengeView(interaction, completed_fighters, remaining_fighters, current_fighter)
    await interaction.response.send_message(embed=embed, view=view)


def shutdown_handler(signum, frame):
    print('Received signal {}. Shutting down...'.format(signum))
    if client:
        client.close()
        print("MongoDB connection closed.")
    exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

bot.run(os.getenv('PROD_BOT_TOKEN'))  # Production
# bot.run(os.getenv('TEST_BOT_TOKEN'))  # Testing
