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

@client.event
async def on_message(message):
    if message.author.id != TRIGGER_USER_ID:
        return
    if message.guild is not None:          # Only DMs
        return

    content = message.content.strip().upper()

    if not content.startswith("VC ALERT"):
        return

    print(f"🔴 VC ALERT received: {message.content}")

    try:
        # Better parsing
        parts = message.content.split()
        if len(parts) < 4:
            print("❌ Not enough arguments in VC ALERT")
            return

        # Find the numbers
        vc_id = None
        guild_id = None
        invite = None

        for i, part in enumerate(parts):
            if part.isdigit() and vc_id is None:
                vc_id = int(part)
            elif part.isdigit() and guild_id is None and vc_id is not None:
                guild_id = int(part)
            elif "discord.gg" in part.lower() or "discord.com/invite" in part.lower():
                invite = part

        if not vc_id or not guild_id:
            print("❌ Could not parse VC ID or Guild ID")
            return

        print(f"📌 Parsed → VC: {vc_id} | Guild: {guild_id} | Invite: {invite}")

        # Join server if needed
        if not client.get_guild(guild_id):
            if invite:
                try:
                    invite_code = invite.split("/")[-1]
                    await client.accept_invite(invite_code)
                    print("✅ Joined server via invite")
                    await asyncio.sleep(3)
                except Exception as e:
                    print(f"Invite failed: {e}")

        guild = client.get_guild(guild_id)
        if not guild:
            print("❌ Could not find server")
            return

        vc = guild.get_channel(vc_id)
        if not vc or not isinstance(vc, discord.VoiceChannel):
            print("❌ Voice channel not found")
            return

        # Force leave any current VC
        for vc_client in client.voice_clients:
            await vc_client.disconnect()
            await asyncio.sleep(1)

        # Join target
        await vc.connect(self_deaf=True, self_mute=True)
        print(f"🎤 Successfully joined VC: {vc.name}")

    except Exception as e:
        print(f"❌ Error processing alert: {e}")

# Stay logic
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
        except:
            pass

client.run(TOKEN)
