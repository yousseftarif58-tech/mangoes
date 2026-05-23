import discord
import asyncio
import os
from discord.ext import commands

# ========================= CONFIG =========================
TOKEN = os.getenv("DISCORD_TOKEN")  # Put your token in Railway Variables

GUILD_ID = 1419326775573479426      # From your link
VOICE_CHANNEL_ID = 1502621775970828331  # The VC you want to stay in
# ========================================================

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", self_bot=True, intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Selfbot logged in as {bot.user}")
    
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("❌ Could not find guild")
        return
    
    vc = guild.get_channel(VOICE_CHANNEL_ID)
    if not vc or not isinstance(vc, discord.VoiceChannel):
        print("❌ Could not find voice channel")
        return

    # Join / Rejoin logic
    if bot.voice_clients:
        for vc_client in bot.voice_clients:
            await vc_client.disconnect()
    
    try:
        await vc.connect(self_deaf=True, self_mute=True)
        print(f"🎤 Successfully joined VC: {vc.name}")
    except Exception as e:
        print(f"❌ Failed to join VC: {e}")

# Reconnect if disconnected
@bot.event
async def on_voice_state_update(member, before, after):
    if member.id != bot.user.id:
        return
    
    if before.channel is not None and after.channel is None:
        print("⚠️ Disconnected from VC, trying to rejoin...")
        await asyncio.sleep(3)
        guild = bot.get_guild(GUILD_ID)
        vc = guild.get_channel(VOICE_CHANNEL_ID)
        if vc:
            try:
                await vc.connect(self_deaf=True, self_mute=True)
                print("✅ Rejoined VC")
            except:
                pass

bot.run(TOKEN, bot=False)
