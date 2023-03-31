import json
from graphqlclient import GraphQLClient
import datetime as dt
import pytz

authToken = "7fe548df9f13fc189caa59a8c299aff9"

client = GraphQLClient('https://api.start.gg/gql/alpha')
client.inject_token('Bearer ' + authToken)

def getTop8(tournament, event):
    event_slug = "tournament/" + tournament + "/event/" + event

    top8 = client.execute('''
        query EventStandings($eventSlug: String!) {
            event(slug: $eventSlug) {
                tournament {
                    name
                    timezone
                    images {
                        url
                        ratio
                    }
                }
                name
                numEntrants
                startAt
                standings(query: {
                    perPage: 8,
                    page: 1
                }){
                nodes {
                    placement
                    entrant {
                    name
                    participants {
                        player {
                        user {
                            authorizations(types: [DISCORD]) {
                                externalUsername
                            }
                        }
                        }
                    }
                    }
                }
                }
            }
        }
        ''',
        {
        "eventSlug": event_slug
        }
    )
    parsed = json.loads(top8)

    if not parsed["data"]["event"]:
        # errors = parsed["errors"]
        return ()
    else:
        tournament_name = parsed["data"]["event"]["tournament"]["name"]
        tournament_tz = parsed["data"]["event"]["tournament"]["timezone"]
        images = parsed["data"]["event"]["tournament"]["images"]

        event_name = parsed["data"]["event"]["name"]
        event_numEntrants = parsed["data"]["event"]["numEntrants"]
        event_timestamp = parsed["data"]["event"]["startAt"]
        entrants = parsed["data"]["event"]["standings"]["nodes"]

        if tournament_tz == None:
            event_date = dt.datetime.fromtimestamp(event_timestamp).strftime("%A, %B %-d, %Y")
        else:
            event_date = dt.datetime.fromtimestamp(event_timestamp).astimezone(pytz.timezone(tournament_tz)).strftime("%A, %B %-d, %Y")

        entrant_names = []
        for e in entrants:
            discord = e["entrant"]["participants"][0]["player"]["user"]["authorizations"]
            if discord:
                entrant_names.append([e["entrant"]["name"], discord[0]["externalUsername"]])
            else:
                entrant_names.append([e["entrant"]["name"], ""])

        image = ""
        for i in images:
            if i["ratio"] > 1:
                image = i["url"]
                break
            image = i["url"]

    return tournament_name, event_name, event_numEntrants, event_date, entrant_names, image


def getSeeding(tournament, event):
    event_slug = "tournament/" + tournament + "/event/" + event

    phases = client.execute('''
        query getPhases($eventSlug: String!) {
            event(slug: $eventSlug) {
                tournament {
                    name
                    timezone
                    images {
                        url
                        ratio
                    }
                }
                name
                numEntrants
                startAt
                phases {
                    id
                }
            }
        }
        ''',
        {
            "eventSlug": event_slug
        }
    )
    phases_parsed = json.loads(phases)
    
    if not phases_parsed["data"]["event"]:
        return []
    elif not phases_parsed["data"]["event"]["phases"]:
        return ("", "", "", "", [])
    else:
        phaseID = phases_parsed["data"]["event"]["phases"][0]["id"]
        numEntrants = phases_parsed["data"]["event"]["numEntrants"]

        tournament_name = phases_parsed["data"]["event"]["tournament"]["name"]
        tournament_tz = phases_parsed["data"]["event"]["tournament"]["timezone"]
        event_name = phases_parsed["data"]["event"]["name"]
        event_timestamp = phases_parsed["data"]["event"]["startAt"]
        images = phases_parsed["data"]["event"]["tournament"]["images"]

        if tournament_tz == None:
            event_date = dt.datetime.fromtimestamp(event_timestamp).strftime("%A, %B %-d, %Y")
        else:
            event_date = dt.datetime.fromtimestamp(event_timestamp).astimezone(pytz.timezone(tournament_tz)).strftime("%A, %B %-d, %Y")
        
        image = ""
        for i in images:
            if i["ratio"] > 1:
                image = i["url"]
                break
            image = i["url"]

        i = 0
        page = 1
        seeding = []

        while True:
            if i > numEntrants:
                break
            else:
                i = i + 100
                seeding_query = client.execute('''
                    query getPhaseSeeds($phaseID: ID!, $pageNum: Int!) {
                        phase(id: $phaseID) {
                            seeds(query: {page: $pageNum, perPage: 100}) {
                            nodes {
                                entrant {
                                    initialSeedNum
                                    name
                                }
                            }
                            }
                        }
                    }
                    ''',
                    {
                        "phaseID": phaseID,
                        "pageNum": page
                    }
                )
                seeding_parsed = json.loads(seeding_query)
                # print(seeding_parsed)

                page = page + 1

                entrants = seeding_parsed["data"]["phase"]["seeds"]["nodes"]

                # print(entrants)
                for e in entrants:
                    seeding.append([e["entrant"]["initialSeedNum"], e["entrant"]["name"]])
        
    seeding.sort(key=lambda x: x[0])
    
    return tournament_name, event_name, numEntrants, event_date, seeding, image


# ----- TESTING -----
# event = "https://www.start.gg/tournament/the-coinbox-55-ultimate-steve-banned/event/ultimate-singles"
# split = event.split('/')

# for i in range(len(split)):
#     if split[i] == "tournament":
#         tournament = split[i+1]
#     elif split[i] == "event":
#         if split[i+1]:
#             event = split[i+1]

# top8 = getTop8(tournament, event)
# for item in top8:
#     print(item)

# seeding = getSeeding(tournament, event)
# print(seeding[0])
# print(seeding[1])
# print(seeding[2])
# print(seeding[3])
# for seed in seeding[4]:
#     print(seed)
