from typing import List

import discord
import asyncio
from .token import tok
from .client import client
from .db import db

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
            todo.append(i.delete())
            print(f"deleting empty channel {i.name}")
            continue

        # Fix the name
        if i.name != expected_name:
            todo.append(i.edit(name=expected_name))
            print(f"renaming channel {i.name} to {expected_name}")

        # Delete if empty (and not the last!)
        if not is_empty and is_last:
            todo.append(i.clone(name=gen_name(base, current_idx + 1)))
            print(f"cloning final channel {i.name}")

        current_idx += 1
        expected_name = gen_name(base, current_idx)

    if todo:
        await asyncio.wait(todo)


@client.event
async def on_voice_state_update(member, before, after):  # It's easier to just check the whole thing
    await client.change_presence(activity=discord.Game(name="Ke2"))
    all_targets = db.get_scale_targets()

    # A dict enforces uniqueness
    affected_targets = {}

    for i in [before, after]:
        if i.channel is None:
            continue
        category = i.channel.category
        template = all_targets.get(category.id)
        if template is not None:
            affected_targets[category] = template

    coros = []

    for channel, template in affected_targets.items():
        try:
            coros.append(poll_channel(channel.voice_channels, template))
        except Exception as e:
            print(e)

    await asyncio.wait(coros)


client.run(tok)

