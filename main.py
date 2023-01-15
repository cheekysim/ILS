import requests
import json
import os

def getData():
  session = requests.Session()

  try:
    url = "https://api.immersivelabs.online/v1/immersive_auth/sessions"

    with open('creds.json', "r") as f:
      data = json.load(f)

    payload = {"account": {
            "email": f"{data.get('email')}",
            "password": f"{data.get('password')}"
        }}
        
    headers = {
        "authority": "api.immersivelabs.online",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://immersivelabs.online",
        "sec-ch-ua": "Not?A_Brand;v=8, Chromium;v=108, Google Chrome;v=108",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

    response = session.post(url, json=payload, headers=headers)
    token = response.cookies['user-token']
  except Exception as e:
    print(e)
    return {"points": 0, "position": 0}, {"points": 0, "position": 0}
  
  payload = "{\"operationName\":\"GetLeaderboardTableData\",\"variables\":{\"profileId\":null,\"landOnParticipantPage\":true,\"after\":null,\"before\":null,\"first\":12,\"last\":null,\"leaderboardContext\":{\"type\":\"GLOBAL\",\"id\":null},\"participantType\":\"ORGANISATION\"},\"query\":\"query GetLeaderboardTableData($profileId: ID = null, $leaderboardContext: LeaderboardContextInput, $participantType: LeaderboardParticipant, $landOnParticipantPage: Boolean = true, $limit: Int, $after: String = null, $before: String = null, $first: Int = null, $last: Int = null) {\\n  ...GetLeaderboardData\\n}\\n\\nfragment GetLeaderboardData on Query {\\n  leaderboardConnection(profileId: $profileId, leaderboardContext: $leaderboardContext, participantType: $participantType, landOnParticipantPage: $landOnParticipantPage, limit: $limit, after: $after, before: $before, first: $first, last: $last) {\\n    currentPage\\n    totalCount\\n    pageInfo {\\n      startCursor\\n      endCursor\\n      __typename\\n    }\\n    edges {\\n      cursor\\n      position\\n      node {\\n        id\\n        title\\n        points\\n        profileAvatar {\\n          id\\n          versionUrl\\n          __typename\\n        }\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n  __typename\\n}\\n\"}"
  
  headers = {
      'cookie': f"user-token={token}",
      'authority': "api.immersivelabs.online",
      'accept': "*/*",
      'accept-language': "en-GB,en-US;q=0.9,en;q=0.8",
      'api-version': "2022-09-30",
      'authorization': f"Bearer {token}",
      'content-type': "application/json",
      'origin': "https://immersivelabs.online",
      'sec-ch-ua': "Not?A_Brand;v=8, Chromium;v=108, Google Chrome;v=108",
      'sec-ch-ua-mobile': "?0",
      'sec-ch-ua-platform': "Windows",
      'sec-fetch-dest': "empty",
      'sec-fetch-mode': "cors",
      'sec-fetch-site': "same-site",
      'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
      }
    
  response = session.post("https://api.immersivelabs.online/v1/graphql", headers=headers, data=payload)
  data = response.json()
  data = data["data"]["leaderboardConnection"]["edges"]

  final = {"data": []}

  cg = 0
  br = 0

  for event in data:
    node = event.get('node')
    if node.get('id') == "coleg-gwent":
      cg = {
        "points": node.get('points'),
        "position": event.get('position')
        }
    elif node.get('id') == "bridgend-college":
      br = {
        "points": node.get('points'),
        "position": event.get('position')
        }

  session.close()
  return cg, br


if __name__ == "__main__":
  print(getData())