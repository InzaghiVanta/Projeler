import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import random

intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True  # Sunucuya katılma olayları için

bot = commands.Bot(command_prefix="!", intents=intents)

# ------------------- BOT HAZIR -------------------
@bot.event
async def on_ready():
    print(f'Bot giriş yaptı: {bot.user}')
    await bot.change_presence(activity=nextcord.Game(name="⚡ Wakanda #FOREVER ⚡"))

# ------------------- DM HOŞGELDİN MESAJI -------------------
@bot.event
async def on_member_join(member):
    try:
        embed = nextcord.Embed(
            title="🖤✨ Wakanda'ya Hoşgeldin! ✨🖤",
            description=f"Selam {member.name}! Sunucuya katıldığın için teşekkürler.\n" +
                        "Burada seni Wakanda’nın ruhu karşılıyor. 👑\n" +
                        "Komutları görmek için `/yardim` yazabilirsin!",
            color=nextcord.Color.dark_purple()
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text="⚡ Wakanda #FOREVER ⚡")
        embed.add_field(name="🎯 İlk Adım", value="Sunucuda keyifli vakit geçir! 🖤", inline=False)
        embed.add_field(name="📜 Kurallar", value="Her zaman saygılı ol! Wakanda ruhu burada.", inline=False)
        embed.add_field(name="💡 İpuçları", value="Komutları deneyerek eğlenceli içeriklere ulaşabilirsin!", inline=False)
        await member.send(embed=embed)
    except:
        print(f"{member.name} kullanıcısına DM gönderilemedi.")

# ------------------- EĞLENCE & BİLGİ KOMUTLARI -------------------
@bot.slash_command(name="merhaba", description="Bot sana selam verir.")
async def merhaba(interaction: Interaction):
    await interaction.response.send_message(f"Merhaba {interaction.user.mention}! 👋 Wakanda Forever!")

@bot.slash_command(name="ping", description="Bot gecikmesini gösterir.")
async def ping(interaction: Interaction):
    await interaction.response.send_message(f"Ping! 🏓 {round(bot.latency * 1000)} ms")

@bot.slash_command(name="sunucu-say", description="Sunucudaki üye sayısını gösterir.")
async def sunucu_say(interaction: Interaction):
    await interaction.response.send_message(f"Sunucuda toplam {interaction.guild.member_count} üye var. 🖤")

@bot.slash_command(name="rastgele-sayi", description="Belirtilen aralıkta rastgele sayı üretir.")
async def rastgele_sayi(interaction: Interaction, min_sayi: int = SlashOption(description="Minimum sayı"), max_sayi: int = SlashOption(description="Maksimum sayı")):
    if min_sayi > max_sayi:
        min_sayi, max_sayi = max_sayi, min_sayi
    sayi = random.randint(min_sayi, max_sayi)
    await interaction.response.send_message(f"🎲 Rastgele sayı: {sayi}")

@bot.slash_command(name="avatar", description="Kullanıcının avatarını gösterir.")
async def avatar(interaction: Interaction, member: nextcord.Member = None):
    member = member or interaction.user
    await interaction.response.send_message(f"{member.mention} avatarı: {member.avatar.url}")

@bot.slash_command(name="bilgi", description="Sunucu hakkında bilgi verir.")
async def bilgi(interaction: Interaction):
    embed = nextcord.Embed(title=f"{interaction.guild.name} Sunucu Bilgisi", color=nextcord.Color.dark_purple())
    embed.add_field(name="Toplam Üye", value=str(interaction.guild.member_count))
    embed.add_field(name="Oluşturulma Tarihi", value=str(interaction.guild.created_at.date()))
    embed.set_footer(text="Wakanda Forever ✨")
    await interaction.response.send_message(embed=embed)

# ------------------- MODERASYON KOMUTLARI -------------------
@bot.slash_command(name="ban", description="Kullanıcıyı banlar ❌")
async def ban(interaction: Interaction, member: nextcord.Member, reason: str = "Sebep belirtilmedi"):
    if interaction.user.guild_permissions.ban_members:
        await member.ban(reason=reason)
        await interaction.response.send_message(f"❌ {member.mention} banlandı! Sebep: {reason}")
    else:
        await interaction.response.send_message("❌ Bu işlemi yapmak için yetkin yok!", ephemeral=True)

@bot.slash_command(name="unban", description="Banı açar ✅")
async def unban(interaction: Interaction, user_id: int):
    if interaction.user.guild_permissions.ban_members:
        user = await bot.fetch_user(user_id)
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"✅ {user.mention} banı açıldı!")
    else:
        await interaction.response.send_message("❌ Bu işlemi yapmak için yetkin yok!", ephemeral=True)

# ------------------- SES KANALI KOMUTLARI -------------------
@bot.slash_command(name="gir", description="Botu ses kanalına sokar ve bekletir 🎵")
async def gir(interaction: Interaction):
    if not interaction.user.voice:
        await interaction.response.send_message("❌ Önce bir ses kanalına girmen gerekiyor!", ephemeral=True)
        return

    kanal = interaction.user.voice.channel
    vc = interaction.guild.voice_client

    if vc:
        await vc.move_to(kanal)
    else:
        await kanal.connect()

    await interaction.response.send_message(f"🎵 Ses kanalına bağlandım: {kanal.name}. Sessizce bekliyorum.")

@bot.slash_command(name="cik", description="Botu ses kanalından çıkar ❌")
async def cik(interaction: Interaction):
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("🎵 Ses kanalından çıktım!")
    else:
        await interaction.response.send_message("❌ Şu an herhangi bir ses kanalında değilim!", ephemeral=True)

# ------------------- YARDIM MENÜSÜ -------------------
@bot.slash_command(name="yardim", description="Wakanda temalı komut listesi")
async def yardim(interaction: Interaction):
    embed = nextcord.Embed(
        title="🖤 Wakanda Komut Menüsü 🖤",
        description="Selam ⬛ Burada tüm komutları bulabilirsin:",
        color=nextcord.Color.dark_purple()
    )
    embed.set_footer(text="Wakanda Forever ✨")

    komutlar = {
        "/merhaba": "Bot sana selam verir 👋",
        "/ping": "Bot gecikmesini gösterir 🏓",
        "/sunucu-say": "Sunucudaki üye sayısını gösterir 🧑‍🤝‍🧑",
        "/rastgele-sayi": "Belirtilen aralıkta rastgele sayı üretir 🎲",
        "/avatar": "Kullanıcının avatarını gösterir 🖼️",
        "/bilgi": "Sunucu hakkında bilgi verir 🏰",
        "/ban": "Kullanıcıyı banlar ❌",
        "/unban": "Banı açar ✅",
        "/gir": "Ses kanalına girer ve bekler 🎵",
        "/cik": "Ses kanalından çıkar ❌"
    }

    for komut, aciklama in komutlar.items():
        embed.add_field(name=komut, value=aciklama, inline=False)

    await interaction.response.send_message(embed=embed)

# ------------------- BOTU ÇALIŞTIR -------------------
bot.run("MTM3MzI5MTMyNjA2NTYxMDgxMg.GGhLf7.SQ27eMNAeGouiKPf-P7gSq6sYRU1ghgHS2BhO4")
