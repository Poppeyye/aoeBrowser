import os
import discord

from scraper.lobbies import AoeRORLobbyBrowser

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL_ID")
intents = discord.Intents.all()
client = discord.Client(intents=intents)

if __name__ == "__main__":
    browser = AoeRORLobbyBrowser()
    available_lobbies = browser.get_available_lobbies()


    @client.event
    async def on_ready():
        channel = client.get_channel(int(CHANNEL))
        await channel.send("\n".join(available_lobbies))
        # Close the bot
        await client.close()


    if available_lobbies:
        client.run(TOKEN)
        browser.close()
    else:
        browser.close()
        exit(0)
