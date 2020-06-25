import discord

import config


class Bot(discord.Client):
    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.channel.name == "вход":
            if message.content.startswith("!nick"):
                nickname = str(message.content).split(" ")[-1]
                await message.channel.send(
                    str(message.author.mention) + ", твой ник " + str(nickname),
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
                await message.channel.send(
                    str(message.author.mention)
                    + ", напиши !nick Твой-ник-в-игре (например: !nick VadVergasov_EU). После этого тебе выдадут роль участника.",
                    delete_after=30,
                )
            await message.delete()

    async def on_member_join(self, member):
        if member == self.user:
            return

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

        await channel.send(
            str(member.mention)
            + ", напиши !nick Твой-ник-в-игре (например: !nick VadVergasov_EU). После этого тебе выдадут роль участника.",
            delete_after=30,
        )


instance = Bot()
instance.run(config.TOKEN)
