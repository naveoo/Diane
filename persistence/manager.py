import sqlite3
import time
import uuid
from typing import Optional, List
from .serializer import to_json
from deltas.types import WorldDelta
from domains.world import World
from core.defaults import Defaults

class PersistenceManager:
    def __init__(self, db_path: str = "simulation.db"):
        self.db_path = db_path
        self.init_schema()
        
    def get_connection(self):
        return sqlite3.connect(self.db_path)
        
    def init_schema(self):
        with self.get_connection() as conn:
            conn.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                created_at REAL,
                name TEXT,
                config_json TEXT
            );

            CREATE TABLE IF NOT EXISTS ticks (
                session_id TEXT,
                tick_number INTEGER,
                timestamp REAL,
                PRIMARY KEY (session_id, tick_number),
                FOREIGN KEY(session_id) REFERENCES sessions(id)
            );

            CREATE TABLE IF NOT EXISTS deltas (
                session_id TEXT,
                tick_number INTEGER,
                delta_json TEXT,
                FOREIGN KEY(session_id, tick_number) REFERENCES ticks(session_id, tick_number)
            );

            CREATE TABLE IF NOT EXISTS snapshots (
                session_id TEXT,
                tick_number INTEGER,
                world_json TEXT,
                PRIMARY KEY (session_id, tick_number),
                FOREIGN KEY(session_id, tick_number) REFERENCES ticks(session_id, tick_number)
            );
            """)
            
    def create_session(self, name: str, config: Defaults = None) -> str:
        session_id = str(uuid.uuid4())
        created_at = time.time()
        config_json = to_json(config) if config else "{}"
        
        with self.get_connection() as conn:
            conn.execute(
                "INSERT INTO sessions (id, created_at, name, config_json) VALUES (?, ?, ?, ?)",
                (session_id, created_at, name, config_json)
            )
        return session_id
        
    def save_step(self, session_id: str, tick: int, delta: WorldDelta, world_snapshot: Optional[World] = None):
        timestamp = time.time()
        delta_json = to_json(delta)
        
        with self.get_connection() as conn:
            conn.execute(
                "INSERT INTO ticks (session_id, tick_number, timestamp) VALUES (?, ?, ?)",
                (session_id, tick, timestamp)
            )
            
            if delta:
                conn.execute(
                    "INSERT INTO deltas (session_id, tick_number, delta_json) VALUES (?, ?, ?)",
                    (session_id, tick, delta_json)
                )
            
            if world_snapshot:
                world_json = to_json(world_snapshot)
                conn.execute(
                    "INSERT INTO snapshots (session_id, tick_number, world_json) VALUES (?, ?, ?)",
                    (session_id, tick, world_json)
                )

    def load_session_metadata(self, session_id: str):
        with self.get_connection() as conn:
            return conn.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()

    def get_latest_tick(self, session_id: str) -> int:
        with self.get_connection() as conn:
            res = conn.execute("SELECT MAX(tick_number) FROM ticks WHERE session_id = ?", (session_id,)).fetchone()
            return res[0] if res and res[0] is not None else 0

    def get_snapshot(self, session_id: str, tick: int) -> Optional[str]:
        with self.get_connection() as conn:
            res = conn.execute("SELECT world_json FROM snapshots WHERE session_id = ? AND tick_number = ?", 
                             (session_id, tick)).fetchone()
            return res[0] if res else None

    def get_deltas(self, session_id: str, start_tick: int, end_tick: int) -> List[str]:
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT delta_json FROM deltas WHERE session_id = ? AND tick_number >= ? AND tick_number <= ? ORDER BY tick_number",
                (session_id, start_tick, end_tick)
            )
            return [row[0] for row in cursor.fetchall()]

    def get_all_snapshots(self, session_id: str) -> List[tuple]:
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT tick_number, world_json FROM snapshots WHERE session_id = ? ORDER BY tick_number",
                (session_id,)
            )
            return cursor.fetchall()
    
    def get_tick_range(self, session_id: str) -> tuple:
        with self.get_connection() as conn:
            res = conn.execute(
                "SELECT MIN(tick_number), MAX(tick_number) FROM ticks WHERE session_id = ?",
                (session_id,)
            ).fetchone()
            return (res[0] or 0, res[1] or 0)
