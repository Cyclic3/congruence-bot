import discord
from discord.ext import commands
from . import module
import asyncio
import requests
import urllib.parse


class OpenCommands(commands.Cog, name="Commands anyone can use"):
    @commands.command(help="Adds you to the group for the give modules")
    async def join(self, ctx: commands.Context, *args):
        await asyncio.gather(*[module.add_student(ctx, ctx.author, i.upper()) for i in args])

    @commands.command(help="Removes you from the group for the give modules")
    async def leave(self, ctx: commands.Context, *args):
        await asyncio.gather(*[module.remove_student(ctx, ctx.author, i.upper()) for i in args])

    @commands.command(help="Renders a LaTeX equation")
    async def maths(self, ctx, *args):
        latex = urllib.parse.quote(' '.join(args))
        await ctx.send(f'https://latex.codecogs.com/gif.latex?\\dpi{{200}}\\bg_white{latex}')


# CAN BE MATHnnn or COMPnnn, so we can't just use number