from aiogram.types import BotCommand, BotCommandScopeDefault


async def setup_bot_commands(bot):
    bot_commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/report", description="Отправить репорт")
    ]
    await bot.set_my_commands(bot_commands, BotCommandScopeDefault())
