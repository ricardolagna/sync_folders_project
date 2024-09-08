import os
import shutil
import time
import argparse

def sync_folders(source, replica, log_file):
    # Function to log operations to the log file
    def log(message):
        with open(log_file, 'a') as log_f:
            log_f.write(message + '\n')
        print(message)

    while True:
        # List files and directories in the source folder
        source_files = set()
        for root, _, files in os.walk(source):
            for file in files:
                source_files.add(os.path.relpath(os.path.join(root, file), source))

        # List files and directories in the replica folder
        replica_files = set()
        for root, _, files in os.walk(replica):
            for file in files:
                replica_files.add(os.path.relpath(os.path.join(root, file), replica))

        # Synchronize files from the source folder to the replica folder
        for file in source_files:
            source_path = os.path.join(source, file)
            replica_path = os.path.join(replica, file)
            if not os.path.exists(os.path.dirname(replica_path)):
                os.makedirs(os.path.dirname(replica_path))
            if not os.path.exists(replica_path) or os.path.getmtime(source_path) > os.path.getmtime(replica_path):
                shutil.copy2(source_path, replica_path)
                log(f'Copied: {source_path} -> {replica_path}')

        # Remove files from the replica folder that do not exist in the source folder
        for file in replica_files:
            replica_path = os.path.join(replica, file)
            if not os.path.exists(os.path.join(source, file)):
                os.remove(replica_path)
                log(f'Removed: {replica_path}')

        # Wait for the interval before the next synchronization
        time.sleep(10)  # Interval of 10 seconds

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Synchronize folders.')
    parser.add_argument('source', type=str, help='Path to the source folder')
    parser.add_argument('replica', type=str, help='Path to the replica folder')
    parser.add_argument('interval', type=int, help='Synchronization interval in seconds')
    parser.add_argument('log_file', type=str, help='Path to the log file')

    args = parser.parse_args()

    # Call the synchronization function with the provided arguments
    sync_folders(args.source, args.replica, args.log_file)


