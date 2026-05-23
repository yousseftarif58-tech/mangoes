import discord
import asyncio
import os

# ========================= CONFIG =========================
TOKEN = os.getenv("DISCORD_TOKEN")

GUILD_ID = 1419326775573479426
VOICE_CHANNEL_ID = 1502621775970828331
# ========================================================

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f"✅ Selfbot logged in as {client.user}")
    
    guild = client.get_guild(GUILD_ID)
    if not guild:
        print("❌ Guild not found")
        return
    
    vc = guild.get_channel(VOICE_CHANNEL_ID)
    if not vc or not isinstance(vc, discord.VoiceChannel):
        print(f"❌ Voice channel not found (ID: {VOICE_CHANNEL_ID})")
        return

    # Disconnect from any old connections
    for vc_client in client.voice_clients:
        await vc_client.disconnect()

    try:
        await vc.connect(self_deaf=True, self_mute=True)
        print(f"🎤 Joined voice channel: {vc.name}")
    except Exception as e:
        print(f"❌ Failed to join VC: {e}")

# Auto reconnect if disconnected
@client.event
async def on_voice_state_update(member, before, after):
    if member.id != client.user.id:
        return
    
    if before.channel is not None and after.channel is None:
        print("⚠️ Disconnected from VC, rejoining in 3s...")
        await asyncio.sleep(3)
        
        guild = client.get_guild(GUILD_ID)
        if guild:
            vc = guild.get_channel(VOICE_CHANNEL_ID)
            if vc:
                try:
                    await vc.connect(self_deaf=True, self_mute=True)
                    print("✅ Rejoined VC")
                except Exception as e:
                    print(f"Rejoin failed: {e}")

client.run(TOKEN)
