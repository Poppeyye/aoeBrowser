from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class AoeRORLobbyBrowser:
    def __init__(self):
        self.url = 'https://aoe2recs.com/browser'
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(self.url)
        self.wait = WebDriverWait(self.driver, 10)

    @staticmethod
    def format_room_message(rooms_list):
        formatted_messages = []

        for room in rooms_list:
            owner_info = room['owner']
            owner = f"{owner_info[0]}({owner_info[1]},{owner_info[2]})"
            lobby_settings = ', '.join([f"{setting[1]}" for setting in room['settings']])
            players = ', '.join([player[0] for player in room['players']])
            opened_time = room['settings'][4][1]  # Extracting "Opened" time from settings

            message = f"- {owner} has opened a room {opened_time}.\n"
            message += f"- Lobby settings: {lobby_settings}\n"

            if players:
                message += f"- Players ({players})\n"

            formatted_messages.append(message)

        return formatted_messages

    def extract_info(self, lobbies):
        data_list = []
        for row in lobbies[2:]:  # delete header rows
            row.click()
            tables = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='game svelte-23rp7e']//table")))
            row_data = {"players": [], "settings": []}

            for i, table in enumerate(tables):
                key = "players" if i == 0 else "settings"
                slots = table.find_elements(By.XPATH, ".//tr")
                for slot in slots:
                    cells = slot.find_elements(By.XPATH, ".//td|.//th")
                    row_data[key].append([cell.text for cell in cells])

            data_list.append(row_data)
        return data_list

    def get_all_lobbies(self, only_ranked: bool = True):
        aoe2check = self.wait.until(EC.presence_of_element_located((By.ID, "aoe2")))
        rankedcheck = self.wait.until(EC.presence_of_element_located((By.ID, "ranked")))
        if only_ranked:
            rankedcheck.click()
        if aoe2check.is_selected():
            aoe2check.click()
        try:
            rows = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//table[@class='columns svelte-23rp7e']//tr")))
        except TimeoutException:
            return "Timeout"  # Return an error code on timeout
        filtered_elements = []
        # Loop through the original element list and filter out elements with unwanted text
        for element in rows:
            if element.text != "":
                filtered_elements.append(element)
        return filtered_elements

    @staticmethod
    def structure_lobbies_info(lobbies):
        output_owner = []
        for lobby in lobbies:
            owner = lobby["players"][0][5]
            elo1v1 = lobby["players"][0][6]
            eloteam = lobby["players"][0][7]
            output_owner.append({"owner": [owner, elo1v1, eloteam],
                                 "settings": lobby["settings"],
                                 "players": [[element for element in player if element is not None and element != ""]
                                             for player in lobby["players"]]})
        return output_owner

    def get_available_lobbies(self):
        table_of_lobbies = self.get_all_lobbies()
        if table_of_lobbies == "Timeout":
            print("Timeout occurred. No active lobbies")
            return None
        lobbies = self.structure_lobbies_info(self.extract_info(table_of_lobbies))
        available_lobbies = self.format_room_message(lobbies)
        return available_lobbies

    def close(self):
        self.driver.quit()
