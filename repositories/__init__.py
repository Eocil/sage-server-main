import asyncio
import aiomysql

from config import mysql

pool = None
pool_initialized = asyncio.Event()

async def init_pool():
    global pool
    print("[Server] Initializing MySQL connection pool...")
    pool = await aiomysql.create_pool(
        host=mysql.MYSQL_HOST,
        port=mysql.MYSQL_PORT,
        user=mysql.MYSQL_USER,
        password=mysql.MYSQL_PASSWORD,
        db=mysql.MYSQL_DB,
        charset=mysql.MYSQL_CHARSET,
        autocommit=True,
        cursorclass=aiomysql.DictCursor,  # 使用字典游标
    )
    pool_initialized.set()  # 标记连接池已初始化

async def close_pool():
    global pool
    if pool:
        pool.close()
        await pool.wait_closed()

async def get_pool():
    await pool_initialized.wait()  # 等待连接池初始化完成
    return pool

if not pool:
    asyncio.create_task(init_pool())