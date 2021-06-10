import sys
import re
import shutil
from os import path, walk, remove
from mdpdf.converter import Converter
from mdpdf.headfoot import Header


class MdToPdf:
    def __init__(self, folder):
        self.folder = folder
        self.output = path.normpath('./mdpdfbook-output.pdf')
        self.tmp = path.normpath('./tmp')
        self.files = []
        self.run()

    def run(self):
        self.remove_tmp()
        self.create_tmp()
        self.get_files()
        self.edit_files()
        self.convert()
        self.remove_tmp()

    def create_tmp(self):
        shutil.copytree(self.folder, self.tmp)
        self.folder = self.tmp

    def remove_tmp(self):
        if path.exists(self.tmp):
            shutil.rmtree(self.tmp)

    def get_files(self):
        smfile = path.join(self.folder, 'SUMMARY.md')
        if path.exists(smfile):
            with open(smfile, 'r', encoding='utf_8') as f:
                ctx = f.read()
                li = re.findall(r'\[(.+)\]\s*\((.+\.md)\)', ctx)
                for l in li:
                    p = path.join(self.folder, l[1])
                    p = path.normpath(p)
                    self.files.append(p)
        else:
            for pth, dirs, files in walk(self.folder):
                for f in files:
                    if f.endswith('.md'):
                        p = path.join(pth, f)
                        p = path.normpath(p)
                        self.files.append(p)

    def edit_files(self):
        for file in self.files:
            with open(file, 'r+', encoding='utf_8') as f:
                ctx = f.read()
                f.seek(0)
                ctx = re.sub(r'\[(.+)\]\s*\((.+\.md)\)',
                             r'\g<1>', ctx)
                f.write(ctx)
                f.truncate()

    def convert(self):
        if path.exists(self.output):
            remove(self.output)
        Header.setFmt("{heading}, ,{page}")
        converter = Converter(self.output)
        converter.convert(self.files)


if __name__ == '__main__':
    folder_path = sys.argv[1]
    MdToPdf(folder_path)
