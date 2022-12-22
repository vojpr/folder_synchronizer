import os
import shutil
import logging
import sys
 
SOURCE_FOLDER = "source"
REPLICA_FOLDER = "replica"

# Logging settings (handles both log file and console output)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', 
                    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler('app.log', mode='a')])


# Start syncing info
logging.info(f"Syncing started")
logging.info(f"Source folder: {SOURCE_FOLDER}")
logging.info(f"Replica folder: {REPLICA_FOLDER}") 

# COPY units from source to replica
for (root, dirs, files) in os.walk(SOURCE_FOLDER):
    for unit in dirs + files:
        rel_path = os.path.relpath(os.path.join(root, unit), SOURCE_FOLDER)
        
        # Check if unit already exists in replica folder, in not copy it
        if not os.path.exists(f"{REPLICA_FOLDER}/{rel_path}"):
            # Check if unit is folder -> create folder in replica
            if os.path.isdir(f"{SOURCE_FOLDER}/{rel_path}"):
                os.mkdir(f"{REPLICA_FOLDER}/{rel_path}")
                                
                logging.info(f"CREATED Folder: {rel_path}") 
                
            # Check if unit is file -> create file in replica
            elif os.path.isfile(f"{SOURCE_FOLDER}/{rel_path}"):
                shutil.copy2(f"{SOURCE_FOLDER}/{rel_path}", f"{REPLICA_FOLDER}/{rel_path}")
                
                logging.info(f"CREATED File: {rel_path}")  
         
        # UPDATE existing unit in replica
        else:       
            # Check if unit is file
            if os.path.isfile(f"{SOURCE_FOLDER}/{rel_path}"):
                source_file_modif_time = os.path.getmtime(f"{SOURCE_FOLDER}/{rel_path}")
                replica_file_modif_time = os.path.getmtime(f"{REPLICA_FOLDER}/{rel_path}")
                # Check if source and replica units modification time is equal, if not update replica file
                if source_file_modif_time != replica_file_modif_time:
                    shutil.copy2(f"{SOURCE_FOLDER}/{rel_path}", f"{REPLICA_FOLDER}/{rel_path}")
                    
                    logging.info(f"UPDATED Folder: {rel_path}")  
                    
# REMOVE units that are only in replica folder
for (root, dirs, files) in os.walk(REPLICA_FOLDER):
    for unit in dirs + files:
        rel_path = os.path.relpath(os.path.join(root, unit), REPLICA_FOLDER)
        
        # Check if unit exists in source folder, in not copy remove it
        if not os.path.exists(f"{SOURCE_FOLDER}/{rel_path}"):
            
            # Check if unit is folder -> create folder in replica
            if os.path.isdir(f"{REPLICA_FOLDER}/{rel_path}"):
                os.rmdir(f"{REPLICA_FOLDER}/{rel_path}")
                
                logging.info(f"REMOVED Folder: {rel_path}")  
                
            # Check if unit is file -> create file in replica
            elif os.path.isfile(f"{REPLICA_FOLDER}/{rel_path}"):
                os.remove(f"{REPLICA_FOLDER}/{rel_path}")
                
                logging.info(f"REMOVED File: {rel_path}")     
                
                
logging.info(f"Syncing finished")
                