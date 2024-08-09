# webhook.py
""" Class to send Discord webhooks """
import discord


class Embed:
    """ Handles sending and parsing Embeds for Discord """
    def __init__(self, treatment: str, companion: str):
        self.treatment = treatment
        self.companion = companion
        self.avatar = "https://i.imgur.com/xdsLwRm.jpeg"
        self.connector()

    def connector(self):
        """ Creates partial webhook from webhook url """
        treatment = self.treatment.split("/")
        companion = self.companion.split("/")

        self.treatment_channel = discord.SyncWebhook.partial(treatment[-2], treatment[-1])
        self.companion_channel = discord.SyncWebhook.partial(companion[-2], companion[-1])

    def __send_treatment_times(self, location : dict, country : str):
        """ Send information to Discord """
        embed = discord.Embed(title=f"Treatment Start Time for {country} (UTC)")
        for site in location:
            start = location[site][0]['times']['twilight_start']
            end = location[site][0]['times']['twilight_end']

            embed.add_field(
                name=site.replace("_", " ").title(),
                value=f"Start: {start} - End: {end}\n",
                inline=False
            )

        embed.set_footer(
            text="Please use 'Companion Start Time' channel for shift start times",
            icon_url="https://i.imgur.com/akbLSLe.png"
        )

        self.treatment_channel.send(embed=embed, avatar_url=self.avatar)

    def __send_companion_times(self, location : dict, country : str):
        """ Send information to Discord """

        embed = discord.Embed(title=f"Companion Shift Start Times for {country} (UTC)")
        for site in location:
            start = location[site][0]['times']['companion_start_time']
            embed.add_field(
                name=site.replace("_", " ").title(),
                value=f"Start Time: {start}\n", inline=False
            )

        embed.set_footer(
            text="Please arrive for the above times to prepare for treatment",
            icon_url="https://i.imgur.com/akbLSLe.png"
        )

        self.companion_channel.send(embed=embed, avatar_url=self.avatar)


    def send_times(self, location : dict, country : str):
        """ Creates Discord embed and sends it to webhook url """
        self.__send_treatment_times(location, country)
        self.__send_companion_times(location, country)
