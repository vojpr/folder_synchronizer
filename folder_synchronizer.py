import os
import shutil
import logging
import sys
import threading
 

class FolderSynchronizer():
    """
    Synchronizes two folders: source and replica. After the synchronization content of the replica 
    folder matches content of the source folder. Synchronization runs periodically. Synchronization 
    operations are logged to a log file and to the console output.
    
    Positional arguments:
        source_folder (str): Source folder path
        replica_folder (str): Replica folder path
        sync_interval (int): Synchronization interval in whole minutes
        log_folder (str): Path to the folder, where log file is/will be created
    """
    
    def __init__(self, source_folder: str, replica_folder: str, sync_interval: int, log_folder: str):
        self.source_folder = source_folder
        if not type(self.source_folder) is str:
            raise TypeError("Folder path must be a string")
        if not os.path.isdir(self.source_folder):
            raise NotADirectoryError("No such folder")
            
        self.replica_folder = replica_folder
        if not type(self.replica_folder) is str:
            raise TypeError("Folder path must be a string")
        if not os.path.isdir(self.replica_folder):
            raise NotADirectoryError("No such folder")
        
        self.sync_interval = sync_interval
        if not type(self.sync_interval) is int:
            raise TypeError("Synchronization interval must be an integer")
        if self.sync_interval < 1:
            raise Exception("Synchronization interval must be higher than zero")
        
        self.log_folder = log_folder
        if not type(self.log_folder) is str:
            raise TypeError("Folder path must be a string")
        if not os.path.isdir(self.log_folder):
            raise NotADirectoryError("No such folder")
        
        # Logging settings (handles both log file and console output)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', 
                            handlers=[
                                logging.StreamHandler(sys.stdout), 
                                logging.FileHandler(os.path.join(self.log_folder, "sync.log"), mode='a')
                                ])

    def operation_method(self, operation: str, folder: str, topdown: bool):
        """
        Method runs one of two operations ("copy_and_update" or "remove") based on operation specified in a positional argument.
        """
        for (root, dirs, files) in os.walk(folder, topdown=topdown):
            for unit in dirs + files:
                rel_path = os.path.relpath(os.path.join(root, unit), folder)
                if operation == "copy_and_update":
                    if not os.path.exists(os.path.join(self.replica_folder, rel_path)):
                        if os.path.isdir(os.path.join(self.source_folder, rel_path)):
                            os.mkdir(os.path.join(self.replica_folder, rel_path))
                            logging.info(f"CREATED Folder: {rel_path}") 
                        elif os.path.isfile(os.path.join(self.source_folder, rel_path)):
                            shutil.copy2(os.path.join(self.source_folder, rel_path), os.path.join(self.replica_folder, rel_path))
                            logging.info(f"CREATED File: {rel_path}")  
                    elif os.path.isfile(os.path.join(self.source_folder, rel_path)):
                        source_file_modif_time = os.path.getmtime(os.path.join(self.source_folder, rel_path))
                        replica_file_modif_time = os.path.getmtime(os.path.join(self.replica_folder, rel_path))
                        if source_file_modif_time != replica_file_modif_time:
                            shutil.copy2(os.path.join(self.source_folder, rel_path), os.path.join(self.replica_folder, rel_path))
                            logging.info(f"UPDATED File: {rel_path}") 
                if operation == "remove" and not os.path.exists(os.path.join(self.source_folder, rel_path)):
                    if os.path.isdir(os.path.join(self.replica_folder, rel_path)):
                        os.rmdir(os.path.join(self.replica_folder, rel_path))
                        logging.info(f"REMOVED Folder: {rel_path}")  
                    elif os.path.isfile(os.path.join(self.replica_folder, rel_path)):
                        os.remove(os.path.join(self.replica_folder, rel_path))
                        logging.info(f"REMOVED File: {rel_path}")
          
    def run_synchronization(self):
        """
        Starts synchronization process.
        """
        logging.info("Synchronization started")
        logging.info(f"Source folder: {self.source_folder}")
        logging.info(f"Replica folder: {self.replica_folder}") 
        self.operation_method("copy_and_update", self.source_folder, True)
        self.operation_method("remove", self.replica_folder, False)
        logging.info("Synchronization finished\n")
        
        # Run synchronization periodically
        threading.Timer(self.sync_interval*60, self.run_synchronization).start()
                