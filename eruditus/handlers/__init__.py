import discord
import os
from config import GHACHA_CHANNEL


KEYWORD_RESPONSES = {
    ("chnwa", "chnowa", "chnoua", "chnouwa"): "7LOWWWAAAAA",
    ("chnia", "chnaya", "chnaia", "chniya"): "TRIYYYYYAAAAAA",
    ("nabel", "nabl", "nabeul", "nabil"): "ZBOUB 3LIK TETHABEL",
    ("bouch", "bocsh", "boush", "bousch"): "ENTA TABBES W HOWA Y5OUCH",
    ("rawa7", "rawwa7"): "TALGEH MLAWA7",
    ("wnos", "noss", " nos "): "TCHEDDOU W TMOSS",
    ("ah?", "eh?"): "3ASBA"
}

GHACHA_ROOM = os.getenv("GHACHA_CHANNEL","")
async def message_handler(message: discord.Message) -> None:
    """
    Checks for keywords in a message and sends a corresponding reply.
    """
    lower_content = message.content.lower()

    for keywords, response in KEYWORD_RESPONSES.items():
        if any(keyword in lower_content for keyword in keywords):
            await message.channel.send(response)
            await message.add_reaction("🤡")
            ghacha_channel = message.guild.get_channel(GHACHA_CHANNEL) # type: ignore
            embed = discord.Embed(
                title="Ghacha Alert",
                description=f"{message.author.mention} ta7 fih 🥀\n"
                f"> {message.content}\n\n"
                f"> ***{response}***",
                color=discord.Color.red()
            )
            if ghacha_channel:
                resp = await ghacha_channel.send(embed=embed)
                await resp.add_reaction("🤡")

            break