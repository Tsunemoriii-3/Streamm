import sys
from platform import python_version
from traceback import format_exc

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client, __version__
from pyrogram.raw.all import layer

from Powers import load_channels, load_support_users, update_cache
from Powers.config import *
from Powers.logger import LOGGER
from Powers.plugins.auto_del_posts import auto_ddel_postss

schedule = AsyncIOScheduler()
class DENDENMUSHI(Client):

    def __init__(self):
        super().__init__(
            "DENDENMUSHI",
            API_ID,
            API_HASH,
            plugins=dict(root="Powers.plugins"),
            bot_token=BOT_TOKEN
        )

    async def start(self):
        LOGGER.info("Starting the bot...")
        await super().start()
        await load_support_users()
        try:
            await load_channels(self)
        except Exception as e:
            LOGGER.error(e)
            LOGGER.error(format_exc())
            LOGGER.info("Shutting down bot...")
            sys.exit(1)
        await update_cache()
        LOGGER.info("Adding scheduler to auto delete post...")
        schedule.add_job(auto_ddel_postss,'interval', [self], seconds = 100)
        LOGGER.info("Scheduler added starting the scheduler")
        schedule.start()
        LOGGER.info("Scheduler started")
        LOGGER.info(
            f"Pyrogram v{__version__} (Layer - {layer}) started on @{self.me.username}")
        LOGGER.info(f"Python Version: {python_version()}\n")
        LOGGER.info("Started bot")

    async def stop(self):
        """Stop the bot"""
        LOGGER.info("Stop command recieved stopping the bot...")
        await super().stop()
        LOGGER.info("Removing all schedule jobs...")
        schedule.remove_all_jobs()
        LOGGER.info("Removed all scheduled jobs")
        LOGGER.info("Bot stopped.")
