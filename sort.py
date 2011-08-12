from optparse import OptionParser
import glob
import shutil
import os
import sys
import time

types = {'directory': 'Directory',
         '.sql': 'Databases',
         '.sql.gz': 'Databases',
         '.tgz': 'Databases',
         '.tar.gz': 'Databases',
         '.pdf': 'PDFs',
         '.doc': 'Documents',
         '.docx': 'Documents',
         '.exe': 'Software',
         '.air': 'Software',         
         '.zip': 'Zipped',
         '.rar': 'Zipped',
         '.tar': 'Zipped',
         '.gz': 'Zipped',
         '.7z': 'Zipped',
         '.bz2': 'Zipped',
         '.htm': 'Documents',
         '.html': 'Documents',
         '.xls': 'Documents',
         '.php': 'Scripts',
         '.ppt': 'Documents',
         '.psd': 'Photoshop',
         '.mp3': 'Music',
         '.mp4': 'Movies',
         '.avi': 'Movies',
         '.png': 'Graphics',
         '.jpg': 'Graphics',
         '.jpeg': 'Graphics',
         '.gif': 'Graphics',
         '.tiff': 'Graphics',
         '.epub': 'Books',
         '.mobi': 'Books',
         '.rpm': 'Software',
         '.dmg': 'Software',
         '.txt': 'Text',
         '.xml': 'Documents',
         '.dll': 'Windows DLLs',
         '.torrent': 'Torrents'}         
         
def ensure_dir(destination):   
    if not os.path.exists(destination):
        os.makedirs(destination)

    for type, dir in types.iteritems():
        path = os.path.join(destination, dir)
        if not os.path.exists(path):
            os.makedirs(path)
        
def sort_files(folder_name, dest):
    files = os.listdir(folder_name)

    for file in files:
        p = os.path.join(folder_name, file)
        if os.path.isdir(p) == True:
            d = os.path.join(dest, types['directory'])
            shutil.move(p, d)
            print "Moving " + p + " to " + d
        else:
            ext = os.path.splitext(p)[1]
            if types.has_key(ext):
                d = os.path.join(dest, types[ext]);
                shutil.move(p, d)
                print "Moving " + p + " to " + d
            else:
                print "Leaving " + p
                

def main():
    parser = OptionParser(usage="Usage: %prog [options] filename")
    parser.add_option("-d", "--destination", dest="destination", help="Directory you want to move files or directories to")
    (options, args) = parser.parse_args()

    directory = args[0]
    destination = options.destination
    
    if not args:
        parser.print_help()
        sys.exit(1)

    if not os.path.exists(directory):
        print "Invalid directory", directory
        sys.exit(1)

    if not destination:
        print "Invalid destination"
        sys.exit(1)

    ensure_dir(destination)
    sort_files(directory, destination)

    print time.time()

if __name__ == "__main__":
    main()
    
    