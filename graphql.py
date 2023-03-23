import json
from graphqlclient import GraphQLClient
import datetime as dt

authToken = "7fe548df9f13fc189caa59a8c299aff9"

client = GraphQLClient('https://api.start.gg/gql/alpha')
client.inject_token('Bearer ' + authToken)

def getTop8(tournament, event):
    event_slug = "tournament/" + tournament + "/event/" + event

    top8 = client.execute('''
        query EventStandings($eventSlug: String!, $page: Int!, $perPage: Int!) {
            event(slug: $eventSlug) {
                tournament {
                    name
                }
                name
                numEntrants
                startAt
                standings(query: {
                    perPage: $perPage,
                    page: $page
                }){
                nodes {
                    placement
                    entrant {
                    name
                    # participants {
                    #     player {
                    #     user {
                    #         authorizations(types: [DISCORD]) {
                    #             externalUsername
                    #         }
                    #     }
                    #     }
                    # }
                    }
                }
                }
            }
        }
        ''',
        {
        "eventSlug": event_slug,
        "page": 1,
        "perPage": 8
        }
    )
    parsed = json.loads(top8)

    if not parsed["data"]["event"]:
        # errors = parsed["errors"]
        return ()
    else:
        tournament_name = parsed["data"]["event"]["tournament"]["name"]
        event_name = parsed["data"]["event"]["name"]
        event_numEntrants = parsed["data"]["event"]["numEntrants"]
        event_timestamp = parsed["data"]["event"]["startAt"]
        entrants = parsed["data"]["event"]["standings"]["nodes"]

        event_date = dt.date.fromtimestamp(event_timestamp).strftime("%A, %B %-d, %Y")

        entrant_names = []
        for e in entrants:
            entrant_names.append(e["entrant"]["name"])
        
        return tournament_name, event_name, event_numEntrants, event_date, entrant_names

# if 'errors' in resData:
#     print('Error:')
#     print(resData['errors'])
# else:
#     print('Success!')
#     print(resData)