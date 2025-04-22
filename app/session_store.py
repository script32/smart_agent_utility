
import json
from semantic_kernel.agents import ChatHistoryAgentThread
import psycopg2


class SessionStore:
    def __init__(self, conn):
        self.conn = conn
        self.ensure_table_exists()

    def ensure_table_exists(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS chat_sessions (
                    session_id TEXT PRIMARY KEY,
                    thread_json TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            self.conn.commit()

    def save(self, session_id: str, thread: ChatHistoryAgentThread):
        thread_json = thread.to_json()
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO chat_sessions (session_id, thread_json, updated_at)
                VALUES (%s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (session_id)
                DO UPDATE SET thread_json = EXCLUDED.thread_json, updated_at = CURRENT_TIMESTAMP;
            """, (session_id, thread_json))
            self.conn.commit()

    def load(self, session_id: str) -> ChatHistoryAgentThread:
        with self.conn.cursor() as cur:
            cur.execute("SELECT thread_json FROM chat_sessions WHERE session_id = %s", (session_id,))
            row = cur.fetchone()
            if row:
                return ChatHistoryAgentThread.from_json(row[0])
            return ChatHistoryAgentThread()
