import discord
from discord.ext import commands
from . import module
from .db import db


class AdminCommands(commands.Cog, name="Course Rep only commands"):
    async def cog_check(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name="Course Reps")
        return role in ctx.author.roles

    @commands.command(help="Deletes a module")
    async def delete_module(self, ctx: commands.Context, name: str):
        await module.delete_module(ctx, name)

    @commands.command(help="Creates a module")
    async def create_module(self, ctx: commands.Context, name: str, desc: str):
        await module.create_module(ctx, name, desc)
