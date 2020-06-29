import discord
import json

import config

import api

API_INSTANCE = api.WgApiBlitz(config.WG_ID, "eu", "ru")

CLAN_ID = API_INSTANCE.clans_list(config.CLAN_TAG)["data"][0]["clan_id"]
AVAILABLE_NICKS = []


class Bot(discord.Client):
    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.channel.name == "вход":
            if message.content[0].isdigit() and int(message.content) <= len(
                AVAILABLE_NICKS
            ):
                nickname = str(AVAILABLE_NICKS[int(message.content) - 1])
                await message.channel.send(
                    str(message.author.mention)
                    + ", твой ник "
                    + str(AVAILABLE_NICKS[int(message.content) - 1]),
                    delete_after=5,
                )
                try:
                    await message.author.edit(nick=nickname)
                    AVAILABLE_NICKS.remove(nickname)
                except discord.errors.Forbidden:
                    await message.channel.send(
                        str(message.author.mention)
                        + ", не могу поменять твой ник, т.к. у меня не достаточно прав.",
                        delete_after=5,
                    )
                roles = message.author.roles
                roles.append(discord.utils.get(message.guild.roles, name="Участник"))
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
            else:
                text = ", напиши номер ника, который у тебя в игре:\n"

                for number in range(1, len(AVAILABLE_NICKS) + 1):
                    text += str(number) + ". " + str(AVAILABLE_NICKS[number - 1]) + "\n"

                await message.channel.send(
                    str(message.author.mention) + text, delete_after=30,
                )
            await message.delete()

    async def on_member_join(self, member):
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

        AVAILABLE_NICKS = []

        for key in members.keys():
            AVAILABLE_NICKS.append(members[key]["account_name"])

        discord_nicks = []

        for current in member.guild.members:
            if current in (self.user, member):
                continue
            discord_nicks.append(str(current.display_name))

        for nick in discord_nicks:
            try:
                AVAILABLE_NICKS.remove(str(nick))
            except ValueError:
                pass

        AVAILABLE_NICKS = sorted(AVAILABLE_NICKS)

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
            text += str(number) + ". " + str(AVAILABLE_NICKS[number - 1]) + "\n"

        await channel.send(
            str(member.mention) + text, delete_after=60,
        )


instance = Bot()
instance.run(config.TOKEN)
