import discord
import asyncio
import os
from discord.ext import commands

# ========================= CONFIG =========================
TOKEN = os.getenv("DISCORD_TOKEN")

GUILD_ID = 1419326775573479426
VOICE_CHANNEL_ID = 1502621775970828331
# ========================================================

# Selfbots usually don't need intents like normal bots
bot = commands.Bot(command_prefix="!", self_bot=True)

@bot.event
async def on_ready():
    print(f"✅ Selfbot logged in as {bot.user}")
    
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("❌ Could not find guild")
        return
    
    vc = guild.get_channel(VOICE_CHANNEL_ID)
    if not vc or not isinstance(vc, discord.VoiceChannel):
        print(f"❌ Could not find voice channel (ID: {VOICE_CHANNEL_ID})")
        return

    # Disconnect from any existing voice
    for vc_client in bot.voice_clients:
        await vc_client.disconnect()

    try:
        await vc.connect(self_deaf=True, self_mute=True)
        print(f"🎤 Successfully joined VC: {vc.name}")
    except Exception as e:
        print(f"❌ Failed to join VC: {e}")

# Auto-reconnect if kicked/disconnected
@bot.event
async def on_voice_state_update(member, before, after):
    if member.id != bot.user.id:
        return

    if before.channel is not None and after.channel is None:
        print("⚠️ Got disconnected, attempting to rejoin in 3 seconds...")
        await asyncio.sleep(3)
        
        guild = bot.get_guild(GUILD_ID)
        if guild:
            vc = guild.get_channel(VOICE_CHANNEL_ID)
            if vc:
                try:
                    await vc.connect(self_deaf=True, self_mute=True)
                    print("✅ Rejoined voice channel")
                except Exception as e:
                    print(f"Rejoin failed: {e}")

bot.run(TOKEN, bot=False)
