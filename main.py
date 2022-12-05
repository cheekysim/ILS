import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

def getData():

  session = requests.Session()


  url = "https://api.immersivelabs.online/v1/immersive_auth/sessions"

  payload = {"account": {
          "email": f"{os.getenv('email')}",
          "password": f"{os.getenv('password')}"
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
    temp = {}
    node = event.get('node')
    temp["position"] = event.get('position')
    temp["name"] = node.get('title')
    temp["id"] = node.get('id')
    temp["points"] = node.get('points')
    if temp.get('id') == "coleg-gwent":
      cg = temp.get('points')
    elif temp.get('id') == "bridgend-college":
      br = temp.get('points')
    final["data"].append(temp)

  with open('data.json', 'w') as f:
    json.dump(final, f, indent=4)

  session.close()
  return cg, br

if __name__ == "__main__":
  getData()