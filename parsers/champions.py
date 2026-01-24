import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

class Champions:
    version = ""

    def __init__(self, version):
        self.version = version

    def parse(self):
        data = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{self.version}/data/en_US/championFull.json")
        champions = data.json()["data"]

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(self.getGender, champ_id): champ_id for champ_id in champions}

            gender_map = {}
            for future in as_completed(futures):
                champ_id = futures[future]
                gender_map[champ_id] = future.result()

        return self.mapData(champions, gender_map)

    def mapData(self, champions, gender_map):
        mappedData = []
        for champ in champions:
            mappedData.append({
                "id": champions[champ].get("id"),
                "name": champions[champ].get("name"),
                "title": champions[champ].get("title"),
                "resource": champions[champ].get("partype"),
                "genre": ",".join(champions[champ].get("tags")),
                "skinCount": len(champions[champ].get("skins")),
                "image": champions[champ].get("image"),
                "gender": gender_map.get(champ, "divers"),
                "attackType": self.getAttackType(champions[champ]),
            })
            print(f"Data fetched for {champ}", flush=True)

        return mappedData

    def getAttackType(self, champion):
        attackRange = champion.get("stats").get("attackrange")
        return "close" if attackRange < 500 else "range"

    def getGender(self, championId):
        if championId == "Renata":
            championId = "renataglasc"
        try:
            lore = requests.get(f"https://universe-meeps.leagueoflegends.com/v1/en_us/champions/{championId.lower()}/index.json", timeout=5).json()
            bio = lore.get("champion", {}).get("biography", {}).get("full", "").lower().split(" ")

            male_keywords = {"he", "him", "his"}
            female_keywords = {"she", "her", "hers"}

            male_count = sum(chunk in male_keywords for chunk in bio)
            female_count = sum(chunk in female_keywords for chunk in bio)

            if male_count > female_count:
                return "male"
            elif female_count > male_count:
                return "female"
            else:
                return "divers"
        except:
            return "divers"
