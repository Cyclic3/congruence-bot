import discord
from discord.ext import commands
from . import module
import asyncio


class OpenCommands(commands.Cog, name="Course Rep only commands"):
    @commands.command(help="Adds you to the group for the give modules")
    async def join(self, ctx: commands.Context, *args):
        await asyncio.gather(*[module.add_student(ctx, ctx.author, i.upper()) for i in args])

    @commands.command(help="Removes you from the group for the give modules")
    async def leave(self, ctx: commands.Context, *args):
        await asyncio.gather(*[module.remove_student(ctx, ctx.author, i.upper()) for i in args])

# CAN BE MATHnnn or COMPnnn, so we can't just use number