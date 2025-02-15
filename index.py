import aiohttp
from telegram import Update
from telegram.ext import Application, CommandHandler

async def get_github_user(update: Update, context):
    if not context.args:
        await update.message.reply_text("Please provide a GitHub username. Example: /github Nehru")
        return

    username = context.args[0] 
    url = f"https://api.github.com/users/{username}"

    session = aiohttp.ClientSession()  
    response = await session.get(url) 

    if response.status == 200:
        data = await response.json()
        print(data)
        message = (
            f"👤 GitHub User: {data['login']}\n"
            f"📛 Name: {data.get('name', 'Not Available')}\n"
            f"📜 Bio: {data.get('bio', 'No bio available')}\n"
            f"📂 Public Repos: {data['public_repos']}\n"
            f"🔗 Profile: {data['html_url']}"
        )
    else:
        message = "❌ User not found! Please check the username."

    await session.close() 
    await update.message.reply_text(message)

async def stop(update: Update, context):
    await update.message.reply_text("Thank you for using the Telegram Bot!")

app = Application.builder().token("7174542332:AAFvlPbV7M5VHDBfqgx-R_YRFSwtmBObSlE").build()
app.add_handler(CommandHandler("github", get_github_user))
app.add_handler(CommandHandler("stop", stop))

app.run_polling()
