#!/usr/bin/python
"""
Program to sort heap of different files to distinct folders by file extensions
"""

import argparse
import shutil
import os
import sys
import logging
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

logging.basicConfig(
    filename=SCRIPT_DIR / 'file_sorter.log', filemode='w', level=logging.DEBUG, format='%(levelname)s - %(message)s')

logger = logging.getLogger()


class Classifier:
    def __init__(self, other=False):
        self.other = other
        self._groups = {
            'Directory': ['directory'],
            'Unrecognized': ['other'],
            'Empty': ['""'],
            'Android': ['.apk'],
            'Software': ['.iso', '.application', '.bin', '.exe', '.air', '.msi', '.deb', '.rpm', '.patch', '.dmg'],
            'Firmware': ['.img', '.rom'],
            'Databases': ['.sql', '.odb', '.mwb', '.csv', '.sql.gz'],
            'Graphics':
            ['.xcf', '.psd', '.svg', '.dia', '.png', '.jpg', '.jpeg', '.gif', '.tiff', '.raw', '.eps', '.bmp'],
            'Java': ['.jnlp', '.jar'],
            'Scripts': ['.aspx', '.pl', '.pm', '.js', '.c', '.sh', '.py', '.conf', '.phtml', '.php'],
            'Documents': {
                "Doc-like": ['.doc', '.docx', '.rtf', '.odt'],
                "Xls-like": ['.xlsx', '.xls', '.ods'],
                "PDF": ['.pdf', '.chm'],
                "Ppt-like": ['.pptx', '.odp', '.ppt'],
                "Text": ['.txt', '.mht', '.htm', '.html'],
                "Other": ['.dotx', '.xml'],
                "Mindmaps": ['.xmind']
            },
            'Flash': ['.swf'],
            'Latex': ['.bib', '.aux', '.dvi', '.bibtex', '.tex'],
            'Zipped': ['.tgz', '.zip', '.rar', '.tar', '.gz', '.7z', '.bz2', '.tar.gz', '.ova'],
            'Logs': ['.log'],
            'Music': ['.mp3', '.ogg', '.wav', '.wv'],
            'Movies': ['.mp4', '.mkv', '.flv', '.avi', '.mpg'],
            'Bk': ['.bak', '.bk'],
            'Books': ['.epub', '.fb2', '.mobi', '.djvu'],
            'DLLs': ['.dll'],
            'Torrents': ['.torrent']
        }

    @property
    def groups(self):
        return list(self._groups.keys())

    @property
    def types(self):
        try:
            return self._types
        except AttributeError:
            self._types = {}
            for key, value in self._groups.items():
                if isinstance(value, list):
                    self.types.update({ext.lower(): key for ext in value})
                elif isinstance(value, dict):
                    for subdir_key, subdir_value in value.items():
                        self.types.update({ext.lower(): f"{key}/{subdir_key}" for ext in subdir_value})
            return self._types

    def choose_group(self, file_path: Path):
        group = self.types.get(file_path.suffix.lower())
        if not group and self.other:
            group = self.types.get('other')
        return group


class Sorter:
    def __init__(self, options):
        self.src_dir = Path(options.source) if options.source else Path.cwd()
        self.tgt_dir = Path(options.destination)
        self.in_place = self.src_dir == self.tgt_dir
        self.recursive = options.recursive
        self.other = options.other
        self.cl = Classifier(self.other)

        self._validate()

    def prepare(self):
        """ Check the existence of destination path and create dirs """

        if not self.tgt_dir.exists():
            self.tgt_dir.mkdir()
            logger.info("Directory has been created: %s", self.tgt_dir)

    def sort(self):
        to_exclude = {*self.cl.groups, "sort.py", 'file_sorter.log'} if self.in_place else set()
        self._recursive_sort(self.src_dir, to_exclude)

    def clean(self):
        """ Remove empty dirs from destination directory """
        files = os.listdir(self.tgt_dir)
        for file in files:
            p = self.tgt_dir / file
            if p.is_dir():
                include_files = os.listdir(p)
                if not include_files:
                    p.rmdir()
                    logger.info("Directory has been removed: %s", p)

    def _recursive_sort(self, start_dir: Path, exclude: set):
        """ Main sorting algorithm """
        files = os.listdir(start_dir)
        for file in [i for i in files if i not in exclude]:
            p = start_dir / file
            if p.is_dir():
                if self.recursive:
                    self._recursive_sort(p, set())
                else:
                    if file not in self.cl.groups:
                        d = self.tgt_dir / self.cl.types['directory']
                        self._move(p, d)
            else:
                group = self.cl.choose_group(p)
                if not group:
                    logger.info("Leaving '%s'", p)
                    continue
                self._move(p, self.tgt_dir / group)

    def _move(self, src: Path, tgt: Path):
        try:
            if not tgt.exists():
                tgt.mkdir()
                logger.info("Directory has been created: %s", tgt)
            shutil.move(str(src), str(tgt))
            logger.info("Moving '%s' to '%s'", src, tgt)
        except shutil.Error as err:
            logger.warning("Can`t move '%s' to '%s': %s", src, tgt, str(err))
        except PermissionError:
            logger.warning("Can`t move '%s' to '%s': Permission denied", src, tgt)

    def _validate(self):
        if not self.src_dir.exists():
            raise ValueError('Source dir does not exists')
        if not self.tgt_dir:
            raise ValueError("Invalid destination")


def cli():
    """
    Get parameters from user and execute sorting
    :return:
    """

    parser = argparse.ArgumentParser(description="Program for file sorting by file extension")
    parser.add_argument("source", help="folder to sort")
    parser.add_argument("destination", help="Directory you want to move files or directories to")
    parser.add_argument(
        "-r",
        "--recursive",
        action='store_true',
        default=False,
        help="Scan folders recursively. Dangerous due to the loss of information"
        " about folders hierarchy.")
    parser.add_argument(
        "-o",
        "--other",
        action='store_true',
        default=False,
        help="Move unrecognized files to special directory. That files keeps unmoved by default")

    options = parser.parse_args()
    try:
        sorter = Sorter(options)
        sorter.prepare()
        sorter.sort()
        sorter.clean()
        logger.info("Sorting complete!")
    except Exception as err:
        logger.exception(err)
        sys.exit(1)


if __name__ == "__main__":
    cli()
