# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from discord.ext import commands
from Twig.TwigCore import *

# ====================================

client = commands.AutoShardedBot(command_prefix=BOT_PREFIX)

logging.basicConfig(level=logging.INFO)

# logger = logging.getLogger('discord')
# logger.setLevel(logging.INFO)
# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)

# ====================================

def Cogs_Loader():
    for filename in os.listdir('./Twig/Cogs'):  # LOADING COGS
        if filename.endswith('.py'):
            client.load_extension(f'Twig.Cogs.{filename[:-3]}')
            print(f'[CORE:COGS] {filename[:-3]} ready!')


Cogs_Loader()


@client.event
async def on_ready():
    # Инициализация базы данных
    await sqlite_data()

    try:
        log_chan = client.get_channel(BOT_MAIN_LOGS)

        playing_now = discord.Activity(name=BOT_PLAYING_GAME_NAME + ' | %shelp' % BOT_PREFIX,
                                       type=discord.ActivityType.playing)

        message = await log_chan.send(":arrows_counterclockwise: " +
                                      "Почти проснулся, ещё пять минуточек, ну...")
        await client.change_presence(activity=playing_now)

        await message.edit(content=":white_check_mark: " + "Всё, к труду и обороне готов!")
    except Exception as err:
        print("It's alive! \nAlso, an error has happened: \n" + str(err))


@client.event
async def on_guild_join(guild):
    log_chan = client.get_channel(BOT_MAIN_LOGS)

    try:
        json_file = open('./config/whitelist.json', "r", encoding='utf-8')
        whitelist = json.load(json_file)
        json_file.close()

        if guild.id not in whitelist:
            await log_chan.send(f':warning: **Обнаружена попытка добавить меня!**\n' +
                                f'Сервер {guild.name} ({guild.id}) не находится в белом списке \n'
                                f'The owner is: {guild.owner} ({guild.owner_id})')
            return await guild.leave()

        await log_chan.send(f":inbox_tray: Я присоединился к {guild.name} ({guild.id})" +
                            f"\nВладелец: {guild.owner} ({guild.owner_id})")
    except Exception as err:
        await log_chan.send("Произошла непреждвиденная ошибка " +
                            "```\n" + str(err) + "```")


@client.event
async def on_guild_remove(guild):
    log_chan = client.get_channel(BOT_MAIN_LOGS)

    try:
        await log_chan.send(f':outbox_tray: Я покинул сервер {guild.name} ({guild.id})')
    except Exception as err:
        await log_chan.send("Произошла непредвиденная ошибка: " +
                            "```\n" + str(err) + "```")


@client.command(brief='Загрузка конкретного модуля', help='Загрузка конкретного модуля')
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'Twig.Cogs.{extension}')
    await ctx.send(f'Loaded {extension}')
    print(f'[CORE] {ctx.author.id} just LOADED a cog {extension}')


@client.command(brief='Выгрузка конкретного модуля', help='Выгрузка конкретного модуля')
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'Twig.Cogs.{extension}')
    await ctx.send(f'Unloaded {extension}')
    print(f'[CORE] {ctx.author.id} just UNLOADED a cog {extension}')


@client.command(brief='Перезагрузка всех модулей', help='Перезагрузка всех модулей')
@commands.is_owner()
async def hot_reload(ctx):
    message = await ctx.send(":repeat: Перезагрузка...")
    cog_lister = "Модули:"

    for FILENAME in os.listdir('./Twig/Cogs'):
        if FILENAME.endswith('.py'):
            client.unload_extension(f'Twig.Cogs.{FILENAME[:-3]}')
            client.load_extension(f'Twig.Cogs.{FILENAME[:-3]}')

            cog_lister = cog_lister + "\n" + f"  + Модуль {FILENAME} успешно перезагружен."

    elapsed_time = time.time() - start_time
    elapsed_time = time.strftime("%Hh %Mm %Ss", time.gmtime(elapsed_time))

    await message.edit(
        content=f":gear: **Модули успешно перезагружены!**\n```yaml\n{cog_lister} \n\nАптайм: {elapsed_time}\n```")

    print(f'[CORE] {ctx.author.id} just did a HOT RELOAD')


# ====================================

client.run(BOT_TOKEN)

# ====================================

if __name__ == '__main__':
    print('Enabling...')
