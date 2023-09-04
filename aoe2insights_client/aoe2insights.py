import requests

class AOE2Client:
    def __init__(self, base_url="https://www.aoe2insights.com/lobbies/api"):
        self.base_url = base_url

    def get_data(self):
        response = requests.get(self.base_url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            # Raise an exception if the response status code is not 200
            raise Exception(f"Error: {response.status_code}")

    def only_ror_maps(self, data):
        return [d for d in data if d["map_type"] in [range(30100, 301028), -1]]

    def determine_if_is_ror(self, data):
        filtered_list = []
        for lobby in data:
            if lobby['map_type'] == -1 and lobby['max_pop'] == 250 and lobby['game_type'] == 0 and lobby['speed'] == 2:
                filtered_list.append(lobby)
        return filtered_list




aoe = AOE2Client()
data = aoe.get_data()
aoe_lobbies = aoe.only_ror_maps(data)
lobbies = aoe.determine_if_is_ror(aoe_lobbies)

print(lobbies)