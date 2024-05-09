import asyncio
import aiosqlite
import logging

# Initialize the logger
logging.basicConfig(level=logging.INFO)

async def init_db():
    database_path = 'chat_memory.db'
    try:
        async with aiosqlite.connect(database_path) as db:
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
        logging.error(f"Failed to initialize the database: {e}")

async def update_response_frequency(response):
    database_path = 'chat_memory.db'
    try:
        async with aiosqlite.connect(database_path) as db:
            await db.execute('''
                UPDATE Responses
                SET frequency = frequency + 1, last_used = CURRENT_TIMESTAMP
                WHERE response = ?
            ''', (response,))
            await db.commit()
            logging.info(f"Updated frequency for response: {response}")
    except Exception as e:
        logging.error(f"Failed to update response frequency: {e}")

if __name__ == "__main__":
    asyncio.run(init_db())