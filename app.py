import daemon
from sys import argv

status = argv

def main_mainfunc():
    from data.config import dbsource
    if dbsource == "pg":
        from utils.db_api.database import create_db


    async def on_startup(dp):
        import filters
        import middlewares
        filters.setup(dp)
        middlewares.setup(dp)

        from utils.notify_admins import on_startup_notify
        await on_startup_notify(dp)
        #await create_db()

    if __name__ == '__main__':
        from aiogram import executor
        from handlers import dp
        from loader import MAIN_DIR
        print(MAIN_DIR)
        executor.start_polling(dp, on_startup=on_startup)


if status.pop() == "daemon":
    with daemon.DaemonContext():
        main_mainfunc()
else:
    main_mainfunc()
