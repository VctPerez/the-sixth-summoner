import asyncio
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    base_accounts_url = "https://europe.api.riotgames.com/"
    headers = {
        "X-Riot-Token": f"{os.getenv('RIOT_API_KEY')}"
    }
    print("Headers:", headers)
    game_name = "ceodeprolongo"
    tag_line = "eing"
    request = httpx.get(base_accounts_url + f"riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}", headers=headers)

    body = request.json()
    print("Account: ", body)
    puuid = body.get("puuid")
    if id:
        base_summoner_url = "https://euw1.api.riotgames.com/"
        request = httpx.get(base_accounts_url + f"lol/match/v5/matches/by-puuid/{puuid}/ids", headers=headers)
        print(request.json())

        match_id = request.json()[0]
        request = httpx.get(base_accounts_url + f"lol/match/v5/matches/{match_id}", headers=headers)
        print(request.json())