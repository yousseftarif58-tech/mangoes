import discord
import asyncio
import os

# ========================= CONFIG =========================
TOKEN = os.getenv("DISCORD_TOKEN")

GUILD_ID = 1419326775573479426
TARGET_VC_ID = 1502621775970828331
# ========================================================

client = discord.Client()   # ← No intents

@client.event
async def on_ready():
    print(f"✅ Selfbot logged in as {client.user}")
    
    guild = client.get_guild(GUILD_ID)
    if guild:
        await join_target_vc(guild)

async def join_target_vc(guild):
    vc = guild.get_channel(TARGET_VC_ID)
    if not vc or not isinstance(vc, discord.VoiceChannel):
        print("❌ Target VC not found")
        return

    # Disconnect from wrong VC
    for vc_client in client.voice_clients:
        if vc_client.channel and vc_client.channel.id != TARGET_VC_ID:
            await vc_client.disconnect()

    try:
        await vc.connect(self_deaf=True, self_mute=True)
        print(f"🎤 Joined locked VC: {vc.name}")
    except Exception as e:
        print(f"❌ Join failed: {e}")

@client.event
async def on_voice_state_update(member, before, after):
    if member.id != client.user.id:
        return

    # If dragged OUT of target VC
    if after.channel is None or (after.channel and after.channel.id != TARGET_VC_ID):
        print("⚠️ Dragged out → forcing back in 3s...")
        await asyncio.sleep(3)
        guild = client.get_guild(GUILD_ID)
        if guild:
            await join_target_vc(guild)
    else:
        print("✅ Staying in target VC (dragged in)")

client.run(TOKEN)
