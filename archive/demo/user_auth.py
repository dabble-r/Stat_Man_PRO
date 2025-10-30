from flask import Flask
from pymongo import MongoClient
import socket
import sys
import contextlib


class KillSwitch:
    def __init__(self):
        """
        Initialize KillSwitch with fixed values.
        """
        # Fixed MongoDB connection values
        self.db_uri = "mongodb://localhost:27017"
        self.db_name = "auth_db"
        self.collection_name = "users"

        # Fixed expected credentials
        self.expected_username = "test_user"
        self.expected_hash = "abc123hash"

        self.client = None
        self.app = Flask(__name__)
        self.port = self._get_free_port()  # dynamically pick a free port

    def _get_free_port(self):
        """Find a free port on the local machine."""
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(('', 0))  # let OS pick a free port
            return s.getsockname()[1]

    def check_internet(self, host="8.8.8.8", port=53, timeout=3):
        """
        Check internet connection by attempting to connect to a known DNS server.
        Returns True if connected, False otherwise.
        """
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error:
            return False

    def connect_db(self):
        """Connect to MongoDB."""
        try:
            self.client = MongoClient(self.db_uri, serverSelectionTimeoutMS=5000)
            db = self.client[self.db_name]
            return db[self.collection_name]
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            sys.exit(1)

    def validate_user(self):
        """Check if the MongoDB user/hash matches the expected values."""
        if not self.check_internet():
            print("No internet connection. Exiting...")
            sys.exit(1)

        collection = self.connect_db()
        user_doc = collection.find_one({"username": self.expected_username})

        if not user_doc:
            print("User not found in database. Exiting...")
            sys.exit(1)

        db_hash = user_doc.get("hash_code")
        if db_hash != self.expected_hash:
            print("Hash mismatch. Exiting...")
            sys.exit(1)

        print("Validation successful. Program will run.")

    def run(self):
        """Run Flask app if validation passes."""
        self.validate_user()

        @self.app.route("/")
        def index():
            return "Program is running. Kill switch validation passed!"

        print(f"Running Flask app on port {self.port}")
        self.app.run(host="0.0.0.0", port=self.port)


if __name__ == "__main__":
    killswitch = KillSwitch()
    killswitch.run()
