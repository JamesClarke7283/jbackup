import os
import tarfile
import zstandard
import time
import subprocess
from datetime import datetime, timedelta

class Backup:
    def __init__(self, config):
        self.config = config
        self.source = None
        self.destination = None
        self.remote = None
        self.delete_older_than = None

    def set_source(self, source):
        self.source = source

    def set_destination(self, destination):
        self.destination = destination

    def set_remote(self, remote):
        self.remote = remote

    def set_delete_older_than(self, days):
        self.delete_older_than = days

    def start(self, progress_callback=None):
        if not self.source or not self.destination:
            raise ValueError("Source and destination must be set before starting backup")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tar_filename = f"backup_{timestamp}.tar"
        compressed_filename = f"{tar_filename}.zst"

        # Stage 1: Create tar archive
        with tarfile.open(tar_filename, "w") as tar:
            total_files = sum([len(files) for _, _, files in os.walk(self.source)])
            processed_files = 0

            for root, _, files in os.walk(self.source):
                for file in files:
                    file_path = os.path.join(root, file)
                    tar.add(file_path, arcname=os.path.relpath(file_path, self.source))
                    processed_files += 1
                    if progress_callback:
                        progress = processed_files / total_files / 2  # First half of progress
                        progress_callback(progress, f"Archiving: {file_path}")

        # Stage 2: Compress tar archive
        compressor = zstandard.ZstdCompressor()
        with open(tar_filename, "rb") as tar_file, open(compressed_filename, "wb") as compressed_file:
            total_size = os.path.getsize(tar_filename)
            compressed_size = 0

            for chunk in compressor.stream_reader(tar_file):
                compressed_file.write(chunk)
                compressed_size += len(chunk)
                if progress_callback:
                    progress = 0.5 + (compressed_size / total_size / 2)  # Second half of progress
                    progress_callback(progress, "Compressing backup")

        # Clean up temporary tar file
        os.remove(tar_filename)

        # Move compressed file to destination
        final_path = os.path.join(self.destination, compressed_filename)
        os.rename(compressed_filename, final_path)

        if self.remote:
            self._rsync_to_remote(final_path)

        if self.delete_older_than:
            self._delete_old_remote_backups()

    def _rsync_to_remote(self, local_file):
        rsync_command = ["rsync", "-avz", "--progress", local_file, self.remote]
        subprocess.run(rsync_command, check=True)

    def _delete_old_remote_backups(self):
        if not self.remote:
            return

        remote_path = self.remote.split(':')[1]
        cutoff_date = datetime.now() - timedelta(days=self.delete_older_than)
        
        ssh_command = f"ssh {self.remote.split(':')[0]} 'find {remote_path} -name \"backup_*.tar.zst\" -type f -mtime +{self.delete_older_than} -delete'"
        subprocess.run(ssh_command, shell=True, check=True)