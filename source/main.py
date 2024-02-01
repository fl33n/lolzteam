# - *- coding: utf- 8 - *-
async def on_startup(dp):
	import os, sys
	import aiofiles
	from dotenv import load_dotenv
	load_dotenv()
	db_path = os.environ.get("DB_PATH")
	if not db_path:
		print("Пожалуйста, укажите путь к базе данных как переменную окружения и попробуйте снова.")
		sys.exit(0)
	if not os.path.exists(db_path):
		db_file = await aiofiles.open(db_path, 'w')
		await db_file.close()
	await Tortoise.init(
		db_url=f'sqlite://{db_path}',
		modules={'models': ['data.models']}
	)
	await Tortoise.generate_schemas()


async def on_shutdown(dp):
	await Tortoise.close_connections()


if __name__ == "__main__":
	import logging
	from handlers import dp
	from aiogram import executor
	from tortoise import Tortoise
	logging.basicConfig(
		level=logging.INFO,
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
	)
	executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
