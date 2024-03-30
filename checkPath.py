import os, sys, subprocess, stat
from os import path

def checkPath():
    if (not path.exists(sys.argv[1])):
        print('Directory {0} non existing'.format(sys.argv[1]))
        sys.exit(1)
    
    id = os.popen('id -u')
    uid = id.read()
    uid = uid.rstrip('\n')
    inode = os.stat(sys.argv[1])
    if (stat.S_IWUSR & inode.st_mode) == 0:
        print('file {0} must have -w privilege'.format(sys.argv[1]))
        sys.exit(1)

    if (uid != inode.st_uid):
        print('user {0} is not proprietary of {1}'.format(uid,sys.argv[1]))
        sys.exit(1)