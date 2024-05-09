import asyncio
import aiosqlite
import logging

class ChatDatabase:
    def __init__(self, database_path):
        self.database_path = database_path
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    async def init_db(self):
        try:
            async with aiosqlite.connect(self.database_path) as db:
                await db.executescript('''
                    CREATE TABLE IF NOT EXISTS Responses (
                        pattern TEXT NOT NULL,
                        response TEXT NOT NULL,
                        frequency INTEGER DEFAULT 1,
                        last_used DATETIME DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (pattern, response)
                    );
                    CREATE TABLE IF NOT EXISTS Contexts (
                        session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        context_key TEXT NOT NULL,
                        context_value TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    );
                ''')
                await db.commit()
                logging.info("Database initialized and tables created.")
        except Exception as e:
            logging.error(f"Error initializing database: {e}")

    async def update_response_frequency(self, response):
        try:
            async with aiosqlite.connect(self.database_path) as db:
                await db.execute('''
                    UPDATE Responses
                    SET frequency = frequency + 1, last_used = CURRENT_TIMESTAMP
                    WHERE response = ?
                ''', (response,))
                await db.commit()
                logging.info(f"Updated frequency for response: {response}")
        except Exception as e:
            logging.error(f"Error updating response frequency: {e}")

    async def close(self):
        try:
            async with aiosqlite.connect(self.database_path) as db:
                await db.close()
                logging.info("Database connection closed successfully.")
        except Exception as e:
            logging.error(f"Error closing database connection: {e}")

if __name__ == "__main__":
    database = ChatDatabase('chat_memory.db')
    asyncio.run(database.init_db())