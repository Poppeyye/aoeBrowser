import os

# Import the discord.py library
import discord
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TOKEN = os.getenv("BOT_TOKEN")
intents = discord.Intents.all()
client = discord.Client(intents=intents)


def format_room_message(rooms_list):
    formatted_messages = []

    for room in rooms_list:
        owner_info = room['owner']
        owner = f"{owner_info[0]}({owner_info[1]},{owner_info[2]})"
        lobby_settings = ', '.join([f"{setting[1]}" for setting in room['settings']])
        players = ', '.join([player[0] for player in room['players']])
        opened_time = room['settings'][4][1]  # Extracting "Opened" time from settings

        message = f"- Owner {owner} has opened a room {opened_time}.\n"
        message += f"- Lobby settings: {lobby_settings}\n"

        if players:
            message += f"- Players ({players})\n"

        formatted_messages.append(message)

    return formatted_messages


def lobbies():
    url = 'https://aoe2recs.com/browser'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    wait = WebDriverWait(driver, 10)
    checkbox = wait.until(EC.presence_of_element_located((By.ID, "aoe2")))
    if checkbox.is_selected():
        checkbox.click()
    rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table[@class='columns svelte-23rp7e']//tr")))
    filtered_elements = []

    # Loop through the original element list and filter out elements with unwanted text
    for element in rows:
        if element.text != "":
            filtered_elements.append(element)
    data_list = []
    for row in filtered_elements[2:]:
        row.click()
        tables = wait.until(
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


def open_rooms(lobbies: list[dict]):
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


available_lobbies = format_room_message(open_rooms(lobbies()))

@client.event
async def on_ready():
    channel = client.get_channel(1144263332245819484)
    await channel.send("\n".join(available_lobbies))
    # Close the bot
    await client.close()

if available_lobbies:
    client.run(TOKEN)
else:
    exit(0)
