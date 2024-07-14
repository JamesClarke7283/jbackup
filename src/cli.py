import argparse
import sys
from core.config import Config
from core.backup import Backup

def parse_arguments():
    parser = argparse.ArgumentParser(description="jbackup - James's Backup Utility")
    parser.add_argument("-s", "--source", help="Source directory to backup", required=True)
    parser.add_argument("-d", "--destination", help="Destination directory for the backup", required=True)
    parser.add_argument("--schedule", help="Schedule backup (e.g., daily, weekly, monthly)")
    parser.add_argument("--remote", help="Remote destination for rsync backup (user@host:/path)")
    parser.add_argument("--delete-older-than", type=int, help="Delete remote backups older than specified days")
    return parser.parse_args()

def print_progress(progress, status):
    sys.stdout.write(f"\rProgress: [{progress:50.0%}] {status}")
    sys.stdout.flush()

def main():
    args = parse_arguments()
    config = Config()
    backup = Backup(config)

    backup.set_source(args.source)
    backup.set_destination(args.destination)

    if args.schedule:
        config.set_schedule(args.schedule)
        print(f"Backup scheduled: {args.schedule}")
    
    if args.remote:
        backup.set_remote(args.remote)
        print(f"Remote backup destination set: {args.remote}")
    
    if args.delete_older_than:
        backup.set_delete_older_than(args.delete_older_than)
        print(f"Will delete remote backups older than {args.delete_older_than} days")

    try:
        print("Starting backup...")
        backup.start(progress_callback=print_progress)
        print("\nBackup completed successfully!")
    except Exception as e:
        print(f"\nAn error occurred during backup: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()