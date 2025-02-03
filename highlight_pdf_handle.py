import tempfile
import time
import threading
import os
from datetime import datetime, timedelta
import uuid

class TempFileManager:
    def __init__(self, cleanup_interval=3600, file_lifetime=1800):  # 1 hour cleanup, 30 min lifetime
        self.temp_dir = tempfile.mkdtemp(prefix="highlighted_pdfs_")
        self.cleanup_interval = cleanup_interval
        self.file_lifetime = file_lifetime
        self.file_timestamps = {}
        self._start_cleanup_thread()

    def _start_cleanup_thread(self):
        thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        thread.start()

    def _cleanup_loop(self):
        while True:
            self.cleanup_old_files()
            time.sleep(self.cleanup_interval)

    def cleanup_old_files(self):
        current_time = datetime.now()
        files_to_remove = []
        
        for filepath, timestamp in self.file_timestamps.items():
            if current_time - timestamp > timedelta(seconds=self.file_lifetime):
                try:
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    files_to_remove.append(filepath)
                except Exception as e:
                    print(f"Error removing file {filepath}: {e}")

        for filepath in files_to_remove:
            self.file_timestamps.pop(filepath, None)

    def add_file(self, filepath):
        self.file_timestamps[filepath] = datetime.now()

    def get_temp_filepath(self, prefix="highlighted_", suffix=".pdf"):
        return os.path.join(self.temp_dir, f"{prefix}{uuid.uuid4()}{suffix}")
