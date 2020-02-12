from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# pip install watchdog for these packages to work

import os
import time
import re

class EventHandler(FileSystemEventHandler):

    SEARCH_PATTERN = "^#\S+"

    def __init__(self, source_dir, destination_dir):
        self.source_dir = source_dir
        self.destination_dir = destination_dir
        self.dest_tags = {}

    def on_created(self, event):
        # Retrieve dictionary each time in case @source_dir has been modified
        self.get_dest_dir_heirarchy()

        for filename in os.listdir(self.source_dir):

            tag = re.search(EventHandler.SEARCH_PATTERN, filename)
            new_destination = ""
            # Checks if @filename contains a prefixed tag
            if not tag == None:
                tag = tag.group()
                if tag in self.dest_tags:
                    new_name = filename.split(tag)[1].strip()
                    new_destination = self.dest_tags[tag] + "/" + new_name

                    #src = self.source_dir + "/" + filename
                    #self.move_file(src, new_destination)

                    file_exits = os.path.isfile(new_destination)
                    i = 0
                    # Renames the file with an incremental value if @filename already exists
                    while (file_exits):
                        i += 1
                        new_name = filename.split(tag)[1].strip() + " " + str(i)
                        new_destination = self.dest_tags[tag] + "/" + new_name
                        file_exits = os.path.isfile(new_destination)
                else:
                    new_dir = self.destination_dir + "/" + tag
                    os.mkdir(new_dir)
                    self.dest_tags[tag] = new_dir

                    new_destination = new_dir + "/" + filename.split(tag)[1].strip()
            else:
                if filename.endswith(".exe") or filename.endswith(".msi"):
                    pass
                continue
                # TODO: check for file type and place into appropriate folder in downloads

            src = self.source_dir + "/" + filename
            os.rename(src, new_destination)
            print("File: '"+filename+"' moved to: '" + new_destination + "'")

    #def move_file(self, src, dest):
    #    new_destination = dest

        # Renames the file with an incremental value if @dest already exists
    #    file_exists = os.path.isfile(new_destination)
    #    i = 0
    #    while (file_exits):
    #        i += 1
    #        new_destination= dest + " " + str(i)
    #        file_exits = os.path.isfile(new_destination)

    #    os.rename(src, new_destination)
    #    filename = src.split("/")[-1]
    #    print("File: '"+filename+"' moved to: '" + new_destination + "'")



    def get_dest_dir_heirarchy(self):
        for dir in os.listdir(self.destination_dir):
            dir_path = self.destination_dir + "/" + dir
            if os.path.isdir(dir_path):
                tag = re.search(EventHandler.SEARCH_PATTERN, dir)
                if not tag == None:
                    self.dest_tags[tag.group()] = dir_path


if __name__ == "__main__":

    event_handler = EventHandler("C:/Users/salas/Downloads", "C:/Users/salas/Desktop/Imperial")
    event_handler.get_dest_dir_heirarchy()

    for tag in event_handler.dest_tags.items():
        print(tag)

    observer = Observer()
    observer.schedule(event_handler, event_handler.source_dir, recursive = True)
    observer.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
