from datetime import datetime, timedelta
import threading

class SessionCache:
    """
    In-Memory Session Cache for Chat History.
    Stores fetched message history to avoid repeated Firestore reads during an active session.
    """
    def __init__(self):
        # Structure: { user_id: { 'history': [], 'last_active': datetime } }
        self._sessions = {}
        self._lock = threading.Lock()
        self._timeout_minutes = 2
    def get_history(self, user_id):
        """
        Returns cached history if session exists and is valid.
        Returns None if session is missing or expired.
        """
        with self._lock:
            if user_id in self._sessions:
                session = self._sessions[user_id]
                
                # Check expiration
                if datetime.now() - session['last_active'] > timedelta(minutes=self._timeout_minutes):
                    print(f"[SessionCache] Session for {user_id} expired. Clearing.")
                    del self._sessions[user_id]
                    return None
                
                # Update activity timestamp on access
                session['last_active'] = datetime.now()
                return session['history']
            return None

    def update_history(self, user_id, history_messages):
        """
        Creates or updates a session with the latest full history.
        """
        with self._lock:
            self._sessions[user_id] = {
                'history': history_messages,
                'last_active': datetime.now()
            }

    def append_message(self, user_id, message):
        """
        Appends a single message to the active session history.
        """
        with self._lock:
            if user_id in self._sessions:
                self._sessions[user_id]['history'].append(message)
                self._sessions[user_id]['last_active'] = datetime.now()

# Global instance
session_cache = SessionCache()
