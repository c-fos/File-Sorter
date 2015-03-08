#!/usr/bin/python
"""
Program to sort heap of different files to distinct folders by file extensions
"""

import argparse
import shutil
import os
import sys
import logging


logging.basicConfig(filename=os.path.join(os.getcwd(), 'file_sorter.log'),
                    filemode='w',
                    level=logging.DEBUG,
                    format='%(levelname)s - %(message)s')
logger = logging.getLogger()
types = {'directory': 'Directory',
         'other': 'Unrecognized',
         '': 'Text',
         '.apk': 'Android',
         '.iso': 'Software',
         '.sql': 'Databases',
         '.odb': 'Databases',
         '.mwb': 'Databases',
         '.svg': 'Graphics',
         '.jnlp': 'Java',
         '.aspx': 'Scripts',
         '.pl': 'Scripts',
         '.pm': 'Scripts',
         '.dia': 'Graphics',
         '.js': 'Scripts',
         '.application': 'Software',
         '.xlsx': 'Documents',
         '.JPG': 'Graphics',
         '.csv': 'Databases',
         '.swf': 'Flash',
         '.bib': 'Latex',
         '.c': 'Scripts',
         '.sh': 'Scripts',
         '.py': 'Scripts',
         '.conf': 'Scripts',
         '.phtml': 'Scripts',
         '.xls': 'Documents',
         '.rtf': 'Documents',
         '.dotx': 'Documents',
         '.sql.gz': 'Databases',
         '.tgz': 'Zipped',
         '.tar.gz': 'Databases',
         '.pdf': 'PDFs',
         '.doc': 'Documents',
         '.docx': 'Documents',
         '.bin': 'Software',
         '.exe': 'Software',
         '.air': 'Software',
         '.msi': 'Software',
         '.jar': 'Libraries',
         '.zip': 'Zipped',
         '.rar': 'Zipped',
         '.tar': 'Zipped',
         '.gz': 'Zipped',
         '.7z': 'Zipped',
         '.bz2': 'Zipped',
         '.htm': 'Documents',
         '.html': 'Documents',
         '.php': 'Scripts',
         '.odt': 'Documents',
         '.ods': 'Documents',
         '.ppt': 'Documents',
         '.xcf': 'Photoshop',
         '.psd': 'Photoshop',
         '.log': 'Logs',
         '.aux': 'Latex',
         '.dvi': 'Latex',
         '.bibtex': 'Latex',
         '.tex': 'Latex',
         '.mp3': 'Music',
         '.ogg': 'Music',
         '.wav': 'Music',
         '.mp4': 'Movies',
         '.mkv': 'Movies',
         '.flv': 'Movies',
         '.avi': 'Movies',
         '.png': 'Graphics',
         '.jpg': 'Graphics',
         '.jpeg': 'Graphics',
         '.gif': 'Graphics',
         '.tiff': 'Graphics',
         '.raw': 'Graphics',
         '.bak': 'Bk',
         '.bk': 'Bk',
         '.eps': 'Graphics',
         '.bmp': 'Graphics',
         '.epub': 'Books',
         '.fb2': 'Books',
         '.mobi': 'Books',
         '.djvu': 'Books',
         '.deb': 'Software',
         '.rpm': 'Software',
         '.patch': 'Software',
         '.dmg': 'Software',
         '.txt': 'Text',
         '.mht': 'Text',
         '.xml': 'Documents',
         '.dll': 'Windows DLLs',
         '.pptx': 'Documents',
         '.odp': 'Documents',
         '.wbk': 'Documents',
         '.torrent': 'Torrents'}


def ensure_dir(destination):
    """
    Check the existence of destination path

    :param destination: - path
    :return: None. Create directories
    """

    if not os.path.exists(destination):
        logger.info("Directory has been created: {}".format(destination))
        os.makedirs(destination)

    for _, _dir in types.items():
        path = os.path.join(destination, _dir)
        if not os.path.exists(path):
            logger.info("Directory has been created: {}".format(path))
            os.makedirs(path)


def dir_clean(destination):
    """
    Remove empty dirs from destination directory. We want to keep our data clean and simple, don`t we? =)

    :param destination: path to destination directory
    :return: None. remove empty dirs from destination directory
    """

    files = os.listdir(destination)
    for file in files:
        p = os.path.join(destination, file)
        if os.path.isdir(p) is True:
            include_files = os.listdir(p)
            if not include_files:
                logger.info("Directory has been removed: {}".format(p))
                os.rmdir(p)


def sort_files(folder_name, destination, recur, other):
    """
    Main sorting algorithm

    :param folder_name: path to input folder
    :param destination: path to output folder
    :param recur: make sorting recursively
    :param other: move unrecognized files to "other" directory
    :return: None/ Move files to right places
    """

    files = os.listdir(folder_name)  # one level file sorting
    for file in files:
        p = os.path.join(folder_name, file)
        if os.path.isdir(p):
            if recur:
                sort_files(p, destination, recur, other)
            else:
                if file not in list(types.values()):
                    d = os.path.join(destination, types['directory'])
                    try:
                        shutil.move(p, d)
                        logger.info("Moving directory '{0}' to '{1}'".format(p, d))
                    except shutil.Error:
                        logger.warning("Can`t move directory '{0}' to '{1}'. {2}".format(p, d, sys.exc_info()[1]))
                    except PermissionError:
                        logger.warning("Can`t move directory '{0}' to '{1}', Permission denied".format(p, d))
        else:
            ext = os.path.splitext(p)[1].lower()
            if ext in list(types.keys()):
                d = os.path.join(destination, types[ext])
                try:
                    shutil.move(p, d)
                    logger.info("Moving file '{0}' to '{1}'".format(p, d))
                except shutil.Error:
                    logger.warning("Can`t move file '{0}' to '{1}'. {2}".format(p, d, sys.exc_info()[1]))
            elif other:
                d = os.path.join(destination, types['other'])
                try:
                    shutil.move(p, d)
                    logger.info("Moving file '{0}' to '{1}'".format(p, d))
                except shutil.Error:
                    logger.warning("Can`t move '{0}' to '{1}', {2}".format(p, d, sys.exc_info()[1]))
            else:
                logger.info("Leaving '{0}'".format(p))


def cli():
    """
    Get parameters from user and execute sorting
    """

    parser = argparse.ArgumentParser(description="Program for file sorting by file extension")
    parser.add_argument("source", help="folder to sort")
    parser.add_argument("destination", help="Directory you want to move files or directories to")
    parser.add_argument("-r", "--recursive", action='store_true', default=False,
                        help="Scan folders recursively. Dangerous due to the loss of information"
                             " about folders hierarchy.")
    parser.add_argument("-o", "--other", action='store_true', default=False,
                        help="Move unrecognized files to special directory. That files keeps unmoved by default")
    options = parser.parse_args()

    if options.source:
        directory = options.source
        logger.info("Source directory: '{}'".format(directory))
    else:
        directory = os.getcwd()
        logger.info("Source directory: '{}'".format(directory))
    destination = options.destination
    logger.info("Destination directory: '{}'".format(destination))
    if not os.path.exists(directory):
        logger.error("Invalid directory: {0}".format(directory))
        sys.exit(1)
    if not destination:
        logger.error("Invalid destination")
        sys.exit(1)

    ensure_dir(destination)
    sort_files(directory, destination, options.recursive, options.other)
    dir_clean(destination)

    logger.info("Sorting complete!")


if __name__ == "__main__":
    cli()