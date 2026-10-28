import os

import discord
from dotenv import load_dotenv

import MAL

load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
commandTree = discord.app_commands.CommandTree(client=client)


@discord.app_commands.command(
    name="anime",
    description="get details for requested anime",
    nsfw=False,
    auto_locale_strings=True,
)
async def anime(interaction: discord.Interaction, title: str):
    data = await MAL.malAnimeMainRequest(query=title)
    card = discord.Embed()
    parsedStatus = "Unknown"
    if data is not None:
        card.set_image(url=data["main_picture"]["large"])
        card.add_field(name="Title", value=data["title"])
        card.add_field(name="Rating", value=data["mean"])
        card.add_field(name="Ranking", value=data["rank"])
        status = data["status"]

        match status:
            case "finished_airing":
                parsedStatus = "Finished"
            case "currently_airing":
                parsedStatus = "Airing"
            case "not_yet_aired":
                parsedStatus = "Not Yet Aired"

        card.add_field(name="Status", value=parsedStatus)

        if parsedStatus != "Airing":
            card.add_field(name="Number of Episodes", value=data["num_episodes"])
        else:
            card.add_field(
                name="Note",
                value="Series that are still airing don't show current number of episodes.",
            )

        await interaction.response.send_message(embed=card)
    else:
        await interaction.response.send_message(f"No data came back for {title}")


commandTree.add_command(anime)


@discord.app_commands.command(
    name="manga",
    description="get details for requested manga",
    nsfw=False,
    auto_locale_strings=True,
)
async def manga(interaction: discord.Interaction, title: str):
    data = await MAL.malMangaMainRequest(query=title)
    card = discord.Embed()
    parsedStatus = "Unknown"
    if data is not None:
        card.set_image(url=data["main_picture"]["large"])
        card.add_field(name="Title", value=data["title"])
        card.add_field(name="Rating", value=data["mean"])
        card.add_field(name="Ranking", value=data["rank"])
        if data["num_volumes"] != 0:
            card.add_field(name="Volumes", value=data["num_volumes"])

        if data["num_chapters"] != 0:
            card.add_field(name="Chapters", value=data["num_chapters"])

        if data["num_chapters"] and data["num_volumes"] == 0:
            card.add_field(
                name="Note",
                value="Series that are still publishing don't show current number of volumes/chapter.",
            )
        else: pass

        status = data["status"]
        match status:
            case "finished":
                parsedStatus = "Finished"
            case "currently_publishing":
                parsedStatus = "Currently Publishing"
            case "not_yet_published":
                parsedStatus = "TBP"
        card.add_field(name="Status", value=parsedStatus)
        await interaction.response.send_message(embed=card)
    else:
        await interaction.response.send_message(f"No data came back for {title}")


commandTree.add_command(manga)


async def syncup():
    return await commandTree.sync()


@client.event
async def on_ready():
    response = await syncup()
    print(f"syncup response: {response}")
    print(f"We have logged in as {client.user}")


client.run(f"{BOT_TOKEN}")
