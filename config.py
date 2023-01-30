"""Config fill properly"""
import os

API_ID = int(os.environ.get("API_ID", "2757157"))
API_HASH = os.environ.get("API_HASH", "cfc4996ef11975132e6af9040e2f0c21")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "1821123783:AAGLi7Hn7jup06uXJE9vVOpw6RwBhTmlEKg")
MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "mongodb+srv://kk:kk@cluster0.qgpzaa7.mongodb.net/?retryWrites=true&w=majority")
DB_URI = os.environ.get("ELEPHANT_SQL", "postgres://jluskqgo:Z2ypbAGtMfTbACyDPwkjd1clYDZlGk2R@chunee.db.elephantsql.com/jluskqgo")
OWNER_ID = int(os.environ.get("OWNER_ID", "1137799257"))
BOT_ID = int(os.environ.get("BOT_ID", "1821123783"))
