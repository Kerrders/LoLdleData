import unittest
import requests
from config import champions_version

class TestChampionsParser(unittest.TestCase):
    def test_ddragon_api(self):
        response = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{champions_version}/data/en_US/championFull.json")
        self.assertEqual(response.status_code, 200)

    def test_wiki(self):
        response = requests.get("https://leagueoflegends.fandom.com/wiki/List_of_champions_by_draft_position")
        self.assertEqual(response.status_code, 200)

    def test_region(self):
        example_faction = "bilgewater"
        response = requests.get(f"https://universe-meeps.leagueoflegends.com/v1/en_us/factions/{example_faction}/index.json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("Content-Type"), "application/json")

    def test_release_date(self):
        response = requests.get(f"https://leagueoflegends.fandom.com/wiki/List_of_champions")
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()