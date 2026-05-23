import discord
import asyncio
import os

# ========================= CONFIG =========================
TOKEN = os.getenv("DISCORD_TOKEN")
TRIGGER_USER_ID = 1479793866931568640
# ========================================================

client = discord.Client()

@client.event
async def on_ready():
    print(f"✅ Selfbot logged in as {client.user}")

# Main handler for VC ALERT
@client.event
async def on_message(message):
    if message.author.id != TRIGGER_USER_ID:
        return
    if not message.guild is None:  # Only respond to DMs
        return

    content = message.content.strip()
    if not content.startswith("VC ALERT"):
        return

    try:
        parts = content.split()
        if len(parts) < 4:
            print("❌ Invalid VC ALERT format")
            return

        vc_id = int(parts[1])
        invite_code = parts[2].replace("https://discord.gg/", "").replace("https://discord.com/invite/", "")
        guild_id = int(parts[3])

        print(f"🔴 VC ALERT received! VC: {vc_id} | Server: {guild_id}")

        # Join server if not already in it
        if not client.get_guild(guild_id):
            print("➡️ Joining server via invite...")
            try:
                await client.accept_invite(invite_code)
                await asyncio.sleep(2)
            except Exception as e:
                print(f"Invite error: {e}")

        guild = client.get_guild(guild_id)
        if not guild:
            print("❌ Could not join/find server")
            return

        vc = guild.get_channel(vc_id)
        if not vc or not isinstance(vc, discord.VoiceChannel):
            print("❌ Voice channel not found")
            return

        # Force leave current VC
        for vc_client in client.voice_clients:
            await vc_client.disconnect()
            await asyncio.sleep(1)

        # Join target VC
        await vc.connect(self_deaf=True, self_mute=True)
        print(f"🎤 Successfully joined VC: {vc.name}")

    except Exception as e:
        print(f"❌ Error processing alert: {e}")

# Auto stay in current VC (if dragged out)
@client.event
async def on_voice_state_update(member, before, after):
    if member.id != client.user.id:
        return

    if len(client.voice_clients) == 0:
        return

    current_vc = client.voice_clients[0].channel

    if after.channel is None or after.channel.id != current_vc.id:
        print("⚠️ Dragged out → rejoining in 3s...")
        await asyncio.sleep(3)
        try:
            await current_vc.connect(self_deaf=True, self_mute=True)
            print("✅ Rejoined VC")
        except:
            pass

client.run(TOKEN)
