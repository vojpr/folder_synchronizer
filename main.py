from folder_synchronizer import FolderSynchronizer
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(dest="source", type=str, help="This is the source folder path")
arg_parser.add_argument(dest="replica", type=str, help="This is the replica folder path")
arg_parser.add_argument(dest="interval", type=int, help="This is the sync interval in whole minutes")
arg_parser.add_argument(dest="logfile", type=str, help="This is the log file path")
args = arg_parser.parse_args()

synchronizer = FolderSynchronizer(args.source, args.replica, args.interval, args.logfile)
synchronizer.run_synchronization()