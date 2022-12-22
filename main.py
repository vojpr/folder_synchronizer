from folder_synchronizer import FolderSynchronizer

SOURCE_FOLDER = "source"
REPLICA_FOLDER = "replica"
LOG_FILE_FOLDER = "log"

synchronizer = FolderSynchronizer(SOURCE_FOLDER, REPLICA_FOLDER, LOG_FILE_FOLDER)
synchronizer.run_synchronization()