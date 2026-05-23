import discord
import asyncio
import os

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = 1419326775573479426
TARGET_VC_ID = 1502621775970828331

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    guild = client.get_guild(GUILD_ID)
    if guild:
        await join_vc(guild)

async def join_vc(guild):
    vc = guild.get_channel(TARGET_VC_ID)
    if not vc:
        print("❌ VC not found")
        return

    # Leave wrong VC
    for v in client.voice_clients:
        if v.channel.id != TARGET_VC_ID:
            await v.disconnect()

    try:
        await vc.connect(self_deaf=True, self_mute=True)
        print(f"🎤 Joined locked VC: {vc.name}")
    except Exception as e:
        print(f"Join error: {e}")

@client.event
async def on_voice_state_update(member, before, after):
    if member.id != client.user.id:
        return

    # If dragged OUT → come back
    if after.channel is None or (after.channel and after.channel.id != TARGET_VC_ID):
        print("⚠️ Dragged out → forcing back in 3s...")
        await asyncio.sleep(3)
        guild = client.get_guild(GUILD_ID)
        if guild:
            await join_vc(guild)
    else:
        print("✅ In target VC (including when dragged in)")

client.run(TOKEN)
