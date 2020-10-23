import discord
from discord.ext import commands
from . import module, client
from .db import db


class AdminCommands(commands.Cog, name="Course Rep only commands"):
    async def cog_check(self, ctx):
        return ctx.guild.get_role(client.course_reps_role_id) in ctx.author.roles

    @commands.command(help="Deletes a module")
    async def delete_module(self, ctx: commands.Context, name: str):
        await module.delete_module(ctx, name)

    @commands.command(help="Creates a module")
    async def create_module(self, ctx: commands.Context, name: str, desc: str):
        await module.create_module(ctx, name, desc)
