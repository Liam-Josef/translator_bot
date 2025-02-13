import discord
from discord.ext import commands
import json
from googletrans import Translator
import asyncio

# ✅ Enable necessary bot permissions
intents = discord.Intents.default()
intents.messages = True
intents.reactions = True  # Enable reaction tracking
intents.message_content = True  # Required to read messages

bot = commands.Bot(command_prefix="!", intents=intents)
translator = Translator()

# ✅ Load user preferences from a JSON file
def load_preferences():
    try:
        with open("preferences.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_preferences(prefs):
    with open("preferences.json", "w") as f:
        json.dump(prefs, f, indent=4)

user_preferences = load_preferences()

# ✅ Log when the bot is ready
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    print("🔍 Bot is online and ready to detect reactions!")

# ✅ Handle reactions to translate messages
@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:  # Ignore bot reactions
        return

    print(f"✅ Reaction detected: {reaction.emoji} by {user.name} on message: {reaction.message.content}")

    if str(reaction.emoji) == "🌍":  # Earth emoji triggers translation
        message = reaction.message

        # Get user's preferred language (default: English)
        lang = user_preferences.get(str(user.id), "en")

        try:
            print(f"🔍 Attempting translation to {lang}: {message.content}")
            translated_text = translator.translate(message.content, dest=lang).text
            await message.channel.send(f"{user.mention} 🌍 **Translation ({lang.upper()}):** {translated_text}")
            print(f"✅ Translated message: {translated_text}")
        except Exception as e:
            print(f"❌ Translation failed: {e}")
            await message.channel.send(f"❌ Translation failed: {e}")

# ✅ Command for users to set their preferred language
@bot.command()
async def setlang(ctx, lang_code):
    user_preferences[str(ctx.author.id)] = lang_code
    save_preferences(user_preferences)
    await ctx.send(f"✅ {ctx.author.mention}, your preferred language is now set to `{lang_code}`.")
    print(f"✅ {ctx.author.name} set language to: {lang_code}")

# ✅ Start the bot using asyncio event loop
def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(bot.start("MTMzOTQ1NzIzNTkzNTU1OTczMQ.Goa4_D.zn_3JTw-VwBAqhoHIRlt1IfLOgzfHOQ253m-5M"))
    except KeyboardInterrupt:
        print("❌ Bot stopped gracefully.")
    finally:
        loop.close()

if __name__ == "__main__":
    run_bot()
