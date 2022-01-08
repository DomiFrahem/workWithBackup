# -*- coding: utf-8 -*-
import gzip
import json
import re
from os import walk, path
import time
from multiprocessing import Process




class pathDB:
    def __init__(self, path):
        self.path = path

    def getFileInDirectory(self):
        f = []
        for (dirpath, dirname, filename) in walk(self.path):
            f.append({"dirpath": dirpath, "dirname": dirname, "filename": filename})
        return f

    def checkFileExists(self, file):
        if path.isfile(file):
            return 1
        else:
            return 0

    def get_json_by_date(self):
        f = {}
        date = []
        for (dirpath, dirname, filename) in walk(self.path):
            for file in filename:
                if str(file[0:8]) not in date:
                    date.append(file[0:8])
                    f[file[0:8]] = {
                        'year': int(file[0:4]),
                        'month': int(file[4:6]),
                        'day': int(file[6:8]),
                        'files': list(filter(lambda x: file[0:8] in x, filename))
                    }
        return f


class Settings:
    def __init__(self, path):
        self.path = path

    def getFullSetting(self):
        with open(self.path, 'r') as setting:
            sett = json.load(setting)
        return sett

    def getPathBackup(self):
        return self.getFullSetting()['pathDir']


def get_fun(data, pattern):
    p = re.compile(pattern)
    result = re.findall(p, data)
    return result


def readInChunk(fileObj, chunkSize=2018):
    while True:
        data = fileObj.read(chunkSize)
        if not data:
            break
        yield data


class work_with_backup:
    def __init__(self, data, pattern, path_file):
        self.data = data
        self.pattern = pattern
        self.path_file = path_file

    def open_file(path_file):
        pattern_extensions = ".*\.gz"
        name_file = re.split('/', path_file)[len(re.split('/', path_file)) - 1]
        data = ""
        if re.match(pattern_extensions, name_file):
            ff = gzip.open(path_file, 'rt', encoding='utf-8', errors='ignore')
            start_time = time.time()
            for x in readInChunk(ff):
                data = data + Process(x)

            print("--- %s seconds ---" % (time.time() - start_time))
        else:
            ff = open(path_file, 'rb')
            data = readInChunk(ff)
        ff.close()
        return data

    def get_name_database(self, data):
        # print(json.dump(self.get_fun(data, '-- MySQL dump')))
        p = "hdfhdfghdfghdfghdfgh"
        print(len(json.dumps(get_fun(data, p))))
        return 0
        # if int(len(json.dump(self.get_fun(data, '-- MySQL dump')))) < 0:
        #     return 'mysql'
        # elif int(len(json.dump(self.get_fun(data, '-- PostgreSQL database dump')))) < 0:
        #     return 'pg'
