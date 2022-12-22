import os
import shutil
import logging
import sys
 

class FolderSynchronizer():
    """
    Synchronizes two folders: source and replica. After the synchronization content of the replica 
    folder matches content of the source folder. Synchronization operations are logged to a log file 
    and to the console output.
    """
    
    def __init__(self, source_folder, replica_folder, log_file_folder):
        self.source_folder = source_folder
        self.replica_folder = replica_folder
        self.log_file_folder = log_file_folder
        # Logging settings (handles both log file and console output)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', 
                            handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(f'{self.log_file_folder}/app.log', mode='a')])

    def copy(self):
        """
        Checks which files or folders from the source folder are missing in the replica 
        folder and then creates their copies in the replica folder.
        """
        for (root, dirs, files) in os.walk(self.source_folder):
            for unit in dirs + files:
                rel_path = os.path.relpath(os.path.join(root, unit), self.source_folder)
                if not os.path.exists(f"{self.replica_folder}/{rel_path}"):
                    # Check if unit is folder -> create folder in replica
                    if os.path.isdir(f"{self.source_folder}/{rel_path}"):
                        os.mkdir(f"{self.replica_folder}/{rel_path}")
                        logging.info(f"CREATED Folder: {rel_path}") 
                    # Check if unit is file -> create file in replica
                    elif os.path.isfile(f"{self.source_folder}/{rel_path}"):
                        shutil.copy2(f"{self.source_folder}/{rel_path}", f"{self.replica_folder}/{rel_path}")
                        logging.info(f"CREATED File: {rel_path}")  
    
    def update(self):
        """
        Compares the modification time of files in the source folder and the replica folder
        and updates files in the replica folder that have different modification time.
        """
        for (root, dirs, files) in os.walk(self.source_folder):
            for unit in dirs + files:
                rel_path = os.path.relpath(os.path.join(root, unit), self.source_folder)  
                if os.path.isfile(f"{self.source_folder}/{rel_path}"):
                    source_file_modif_time = os.path.getmtime(f"{self.source_folder}/{rel_path}")
                    replica_file_modif_time = os.path.getmtime(f"{self.replica_folder}/{rel_path}")
                    if source_file_modif_time != replica_file_modif_time:
                        shutil.copy2(f"{self.source_folder}/{rel_path}", f"{self.replica_folder}/{rel_path}")
                        logging.info(f"UPDATED File: {rel_path}")  
                    
    def remove(self):
        """
        Checks which files or folders from the replica folder are missing in the source 
        folder and then removes them from the replica folder.
        """
        for (root, dirs, files) in os.walk(self.replica_folder):
            for unit in dirs + files:
                rel_path = os.path.relpath(os.path.join(root, unit), self.replica_folder)
                if not os.path.exists(f"{self.source_folder}/{rel_path}"):
                    # Check if unit is folder -> create folder in replica
                    if os.path.isdir(f"{self.replica_folder}/{rel_path}"):
                        os.rmdir(f"{self.replica_folder}/{rel_path}")
                        logging.info(f"REMOVED Folder: {rel_path}")  
                    # Check if unit is file -> create file in replica
                    elif os.path.isfile(f"{self.replica_folder}/{rel_path}"):
                        os.remove(f"{self.replica_folder}/{rel_path}")
                        logging.info(f"REMOVED File: {rel_path}")     
          
    def run_synchronization(self):
        """
        Starts synchronization process.
        """
        logging.info(f"Synchronization started")
        logging.info(f"Source folder: {self.source_folder}")
        logging.info(f"Replica folder: {self.replica_folder}") 
        self.copy()
        self.update()
        self.remove()
        logging.info(f"Synchronization finished")
                