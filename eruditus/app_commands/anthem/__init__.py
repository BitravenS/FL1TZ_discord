import os

import discord
from discord import app_commands


ASSETS = f"{os.path.dirname(__file__)}/assets"


class Anthem(app_commands.Command):
    def __init__(self) -> None:
        super().__init__(
            name="anthem",
            description="The national anthem for the Frou5 li Tnaggez",
            callback=self.cmd_callback,  # type: ignore
        )

    async def cmd_callback(self, interaction: discord.Interaction) -> None:
        """Show bot instructions for newcomers.

        Args:
            interaction: The interaction that triggered this command.
        """
        embed = discord.Embed(
            title="Nachid Lwatani 🫡",
            description=(
                "Frou5 li Tnaggez\n"
                "Rapek bech nefehmou yelzemni ntaggez\n"
                "Ommek Tji 9oddemi wetfagges...\n\n"
                "Frou5 li Tnaggez\n"
                "Rapek bech nefehmou yelzemni ntaggez\n"
                "Ommek Tji 9oddemi wetfagges\n"
                "W 7wemna ki tachna3 tfayyedh ennil\n"
                "N3ichou kel film, ne7mou l9ellil\n"
                "Ki yti7 ellil na7seb 9addech tayya7t men kill\n\n...\n\n"
            ),
            colour=discord.Colour.blurple(),
        ).set_thumbnail(
            url="attachment://theOG.png"
        )  # type: ignore

        await interaction.response.send_message(embed=embed)
