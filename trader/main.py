import discord
import asyncio
import json
import os
import aiologger
from dotenv import load_dotenv
from binance_trade_bot import BinanceTradeBot
from logger import embed
from db.connection import get_db_engine
from db.services import insert_objects, select_and_update_objects


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

    async def setup_hook(self) -> None:
        self.bg_task = self.loop.create_task(self.binance_script())

    async def binance_script(self):
        await self.wait_until_ready()
        channel = self.get_channel(877341571173986325)  # channel ID goes here
        while True:
            bot = BinanceTradeBot(api_key, api_secret, crypto, info)
            if bot.get_status():
                order = bot.create_order()
                message = bot.trade(order)
                logger.info(message)
                await channel.send(embed=embed(message))
            info['status'] = bot.status
            info['last_buy'] = bot.last_buy
            info['last_sell'] = bot.last_sell
            await asyncio.sleep(300)


async def main():
    db_engine, db_session = await get_db_engine()
    await insert_objects(db_session)
    await select_and_update_objects(db_session)

    await db_engine.dispose()


if __name__ == '__main__':
    data = "data.json"
    load_dotenv()
    logger = aiologger.Logger.with_default_handlers(level=10)
    api_key = os.environ.get('BINANCE_API')
    api_secret = os.environ.get('BINANCE_SECRET')
    discord_key = os.environ.get('DISCORD_API')
    intents = discord.Intents.default()
    intents.message_content = True

    # client = MyClient(intents=intents)
    # client.run(discord_key)
    asyncio.run(main())
