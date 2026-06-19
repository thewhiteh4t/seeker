#!/usr/bin/env python3

import threading
from dataclasses import dataclass, field
from typing import Callable, List, Optional
from time import time


@dataclass
class Session:
    ip: str
    info: Optional[dict] = None
    locations: List[dict] = field(default_factory=list)
    first_seen: float = field(default_factory=time)
    last_seen: float = field(default_factory=time)


class SessionManager:
    def __init__(self):
        self._lock = threading.Lock()
        self._sessions: dict[str, Session] = {}
        self._callbacks: List[Callable] = []

    def on_update(self, callback: Callable):
        self._callbacks.append(callback)

    def _notify(self, event_type: str, session: Session):
        for cb in self._callbacks:
            try:
                cb(event_type, session)
            except Exception:
                pass

    def update_info(self, ip: str, info: dict):
        with self._lock:
            if ip not in self._sessions:
                self._sessions[ip] = Session(ip=ip)
            session = self._sessions[ip]
            session.info = info
            session.last_seen = time()
        self._notify('info', session)

    def update_location(self, ip: str, location: dict):
        with self._lock:
            if ip not in self._sessions:
                self._sessions[ip] = Session(ip=ip)
            session = self._sessions[ip]
            session.locations.append(location)
            session.last_seen = time()
        self._notify('location', session)

    def update_error(self, ip: str, error: dict):
        with self._lock:
            if ip not in self._sessions:
                self._sessions[ip] = Session(ip=ip)
            session = self._sessions[ip]
            session.last_seen = time()
        self._notify('error', session)

    def get_session(self, ip: str) -> Optional[Session]:
        with self._lock:
            return self._sessions.get(ip)

    def get_all_sessions(self) -> List[Session]:
        with self._lock:
            return list(self._sessions.values())

    def get_sessions_dict(self) -> list:
        with self._lock:
            result = []
            for s in self._sessions.values():
                d = {
                    'ip': s.ip,
                    'info': s.info,
                    'locations': s.locations,
                    'first_seen': s.first_seen,
                    'last_seen': s.last_seen,
                }
                result.append(d)
            return result
