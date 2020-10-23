from typing import List

import discord
import asyncio
from .token import tok
from .client import client

from .admin import AdminCommands
from .open import OpenCommands

client.add_cog(AdminCommands())
client.add_cog(OpenCommands())


def gen_name(base: str, idx: int):
    return f"{base}{idx}"


async def poll_channel(channels: List[discord.VoiceChannel], base: str):
    # Skip if there's nothing here
    if len(channels) == 0:
        return

    todo = []

    # First, trim any empty channels, renaming the remaining ones
    current_idx = 1
    expected_name = gen_name(base, current_idx)
    for idx, i in enumerate(channels):
        is_empty = (len(i.voice_states.keys()) == 0)
        is_last = (idx == len(channels) - 1)

        # If the final channel is empty, then we need to create a new one
        if is_empty and not is_last:
            todo.append(i.delete(reason="Scaley: Empty"))
            print(f"deleting empty channel {i.name}")
            continue

        # Fix the name
        if i.name != expected_name:
            todo.append(i.edit(reason="Scaley: Filling names", name=expected_name))
            print(f"renaming channel {i.name} to {expected_name}")

        # Delete if empty (and not the last!)
        if not is_empty and is_last:
            todo.append(i.clone(name=gen_name(base, current_idx + 1), reason="Scaley: All full"))
            print(f"cloning final channel {i.name}")

        current_idx += 1
        expected_name = gen_name(base, current_idx)

    if todo:
        await asyncio.wait(todo)


channels = {"768927496196194354": "voice-chat-"}


@client.event
async def on_voice_state_update(*args, **kwargs):  # It's easier to just check the whole thing
    print("Triggered")
    for channel_id, template in channels.items():
        try:
            target: discord.CategoryChannel = await client.fetch_channel(channel_id)
            await poll_channel(target.channels, template)
        except Exception as e:
            print(e)


@client.command()
async def ping(ctx):
    await ctx.send("pong")

client.run(tok)

