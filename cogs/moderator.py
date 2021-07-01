import discord
from discord.ext import commands
from discord.ext.commands import has_permissions


class Moderator(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1)

    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.send(f'**The user** {member.mention} **has been kicked by** {ctx.message.author.mention}**.**'
                       f'\n**Reason:** \t{reason}')
        await ctx.message.delete()
        await member.kick(reason=reason)

    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.send(f'**The user** {member.mention} **has been banned by** {ctx.message.author.mention}**.**'
                       f'\n**Reason:** \t{reason}')
        await ctx.message.delete()
        await member.ban(reason=reason)

    @commands.command()
    @has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.message.delete()
                await ctx.send(f'**Unbanned** {user.mention}')
                return

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            message = "We couldn't find the specified member"
        else:
            raise error
        await ctx.send(message, delete_after=5)
        await ctx.message.delete()


def setup(client):
    client.add_cog(Moderator(client))
