import os
from datetime import datetime
from operator import itemgetter

file_time_list = []

for (path, dir, files) in os.walk('./DB'):
    for filename in files:
        if 'backup' in filename: continue
        if filename.split('.')[-1] != 'db': continue
        fileMtime = datetime.fromtimestamp(os.path.getmtime(path+'\\'+filename)).strftime("%Y-%m-%d %H:%M:%S")
        file_time_list.append([path, filename, fileMtime])

file_time_list.sort(key = lambda file_time_list: file_time_list[2])
file_time_list.reverse()
print(file_time_list)
