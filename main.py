"""
Main file for bot.
"""
import discord

import config

import api

API_INSTANCE = api.WgApiBlitz(config.WG_ID, "eu", "ru")

CLAN_ID = API_INSTANCE.clans_list(config.CLAN_TAG)["data"][0]["clan_id"]
AVAILABLE_NICKS = {}
ROLES_HIERARCHY = {"private": 1, "executive_officer": 2, "commander": 3}


class Bot(discord.Client):
    """
    Bot class.
    """

    async def on_message(self, message):
        """
        Do on message.
        """
        if message.author == self.user:
            return

        if message.channel.name == "вход":
            if message.content[0].isdigit() and int(message.content) <= len(
                AVAILABLE_NICKS
            ):
                nickname = str(list(AVAILABLE_NICKS.keys())[int(message.content) - 1])
                await message.channel.send(
                    str(message.author.mention) + ", твой ник " + nickname,
                    delete_after=5,
                )
                try:
                    await message.author.edit(nick=nickname)
                except discord.errors.Forbidden:
                    await message.channel.send(
                        str(message.author.mention)
                        + ", не могу поменять твой ник, т.к. у меня не достаточно прав.",
                        delete_after=5,
                    )
                roles = message.author.roles
                for i in range(ROLES_HIERARCHY[AVAILABLE_NICKS[nickname]]):
                    roles.append(
                        discord.utils.get(message.guild.roles, name=config.ROLES[i])
                    )
                roles.remove(
                    discord.utils.get(message.guild.roles, name="Новый участник")
                )
                try:
                    await message.author.edit(roles=roles)
                except discord.errors.Forbidden:
                    await message.channel.send(
                        str(message.author.mention)
                        + ", Не могу поменять твою роль, т.к. у меня не достаточно прав.",
                        delete_after=5,
                    )
                del AVAILABLE_NICKS[nickname]
            else:
                text = ", напиши номер ника, который у тебя в игре:\n"

                for number in range(1, len(AVAILABLE_NICKS) + 1):
                    text += (
                        str(number)
                        + ". "
                        + str(list(AVAILABLE_NICKS.keys())[number - 1])
                        + "\n"
                    )

                await message.channel.send(
                    str(message.author.mention) + text, delete_after=30,
                )
            await message.delete()

    async def on_member_join(self, member):
        """
        When someone joins.
        """
        global AVAILABLE_NICKS

        if member == self.user:
            return

        members = API_INSTANCE.clans_accountinfo(
            list(
                API_INSTANCE.clans_info(str(CLAN_ID))["data"][str(CLAN_ID)][
                    "members_ids"
                ]
            )
        )["data"]

        for key in members.keys():
            AVAILABLE_NICKS[members[key]["account_name"]] = members[key]["role"]

        discord_nicks = []

        for current in member.guild.members:
            if current in (self.user, member):
                continue
            discord_nicks.append(str(current.display_name))

        for nick in discord_nicks:
            try:
                del AVAILABLE_NICKS[str(nick)]
            except KeyError:
                pass

        AVAILABLE_NICKS = dict(sorted(AVAILABLE_NICKS.items()))

        channel = discord.utils.get(member.guild.channels, name="вход")

        roles = member.roles
        roles.append(discord.utils.get(member.guild.roles, name="Новый участник"))
        try:
            await member.edit(roles=roles)
        except discord.errors.Forbidden:
            await channel.send(
                str(member.mention)
                + ", Не могу поменять твою роль, т.к. у меня не достаточно прав.",
                delete_after=5,
            )

        text = ", напиши номер ника, который у тебя в игре:\n"

        for number in range(1, len(AVAILABLE_NICKS) + 1):
            text += (
                str(number)
                + ". "
                + str(list(AVAILABLE_NICKS.keys())[number - 1])
                + "\n"
            )

        await channel.send(
            str(member.mention) + text, delete_after=60,
        )


instance = Bot()
instance.run(config.TOKEN)
