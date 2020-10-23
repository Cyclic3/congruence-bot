from .db import db
import discord
from discord.ext import commands
from . import client
import asyncio


class ModuleNotFound(Exception):
    def __init__(self, module: str):
        self.module = module


async def create_module(ctx: commands.Context, module: str, desc: str) -> None:
    # Do this first to prevent race condition
    db.start_add_module(name=module, desc=desc)

    base: discord.CategoryChannel = await ctx.guild.create_category_channel(name=f"{module}: {desc}")
    role = await ctx.guild.create_role(name=module)

    db.finish_add_module(name=module, channel_id=base.id, role_id=role.id)
    template = "subject-chat-"

    await asyncio.gather(
        base.set_permissions(role, read_messages=True),
        base.set_permissions(ctx.guild.get_role(client.bot_role_id), read_messages=True),
        base.set_permissions(ctx.guild.default_role, read_messages=False),

        # Text channels
        base.create_text_channel("announcements"),
        base.create_text_channel("general"),
        base.create_text_channel("vc-text"),

        # Voice channels
        base.create_voice_channel(f"{template}1"),
    )

    db.add_scale_target(base.id, template=template)


async def delete_module(ctx: commands.Context, module: str) -> None:
    # Do this first to prevent race condition
    mod_info = db.get_module(module)
    db.remove_module(module)
    db.remove_scale_target(mod_info.channel_id)

    target_channel: discord.CategoryChannel = ctx.guild.get_channel(mod_info.channel_id)
    target_role: discord.Role = ctx.guild.get_role(mod_info.role_id)

    await asyncio.gather(
        target_role.delete(),
        *[i.delete() for i in target_channel.channels]
    )

    await asyncio.sleep(1)  # Discord GUI gets a bit sad around here

    # Must be done after channel deletion
    await target_channel.delete()


async def get_module_student_role(ctx: commands.Context, module: str) -> discord.Role:
    if not db.check_module(module):
        raise ModuleNotFound(module)
    return discord.utils.get(ctx.guild.roles, name=f"{module}")


async def add_student(ctx: commands.Context, member: discord.Member, module: str):
    await member.add_roles(await get_module_student_role(ctx, module))


async def remove_student(ctx: commands.Context, member: discord.Member, module: str):
    await member.remove_roles(await get_module_student_role(ctx, module))
