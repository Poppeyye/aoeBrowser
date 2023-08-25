import asyncio
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Import the discord.py library
import discord

from discord.ext import commands
TOKEN = ""

intents = discord.Intents.all()
client = discord.Client(intents=intents)
def lobbies():
    url = 'https://aoe2recs.com/browser'
    driver = webdriver.Chrome()
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    checkbox = wait.until(EC.presence_of_element_located((By.ID, "aoe2")))
    if checkbox.is_selected():
        checkbox.click()
    rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table[@class='columns svelte-23rp7e']//tr")))

    data_list = []
    for row in rows[2:-3]:
        row.click()
        tables = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='game svelte-23rp7e']//table")))
        row_data = {"players": [], "settings": []}

        for i, table in enumerate(tables):
            key = "players" if i == 0 else "settings"
            rows = table.find_elements(By.XPATH, ".//tr")
            for row in rows:
                cells = row.find_elements(By.XPATH, ".//td|.//th")
                row_data[key].append([cell.text for cell in cells])

        data_list.append(row_data)
    return data_list

@client.event
async def on_ready():
    channel = client.get_channel(1144263332245819484)
    await channel.send(lobbies())
client.run(TOKEN)
#
#


