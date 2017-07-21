# parse the Git log in python
import sys
import re
import subprocess
#import pdb    #used for debug
# create a dict to store the log information
branchs = []
commits = []
FILE    = ''
def ParseLog(files):
    # each log information
    global commits
    commit = {}
    commits = []
    #commitLines = open(files,'r')
    with open(files) as commitLines:
        for each_line in commitLines:
            # use regular express to match
            if each_line =='' or each_line == '\n':
                pass
            elif re.match('commit',each_line,re.IGNORECASE):
                # 'commit flag'
                if len(commit) != 0:        # new commit arrive
                    commits.append(commit)
                    commit = {}
                commit = {'num': re.match('commit (.*)',each_line,re.IGNORECASE).group(1)}
            elif re.match('Author:',each_line,re.IGNORECASE):
                # Author:
                p = re.compile('Author: (.*) <(.*)>').match(each_line)
                commit['author'] = p.group(1)
                commit['email']  = p.group(2)
            elif re.match('date:',each_line,re.IGNORECASE):
                # Date:xx
                pass
            elif re.match('    ',each_line,re.IGNORECASE):
                if commit.get('message') is None:
                    commit['message'] = each_line.strip()
            else:
                print('ERROR: Unexpected Line:'+ each_line)
    #add the last commit
    commits.append(commit)
    commitLines.close()
    
def GetLogInfo(info):
    global FILE
    FILE = info[0]+'.txt'
    comm     = ['git','checkout',info[0]]
    command  = ['git','log','-'+str(info[1])]
    subprocess.check_output(comm)
    stdout  = subprocess.check_output(command)
    return stdout
#get branch infomation

def get_branch():
    global branchs
    branchs = []
    command = ['git','branch','--all']
    stdout  = subprocess.check_output(command)
    for each in stdout.splitlines():
        if re.match('  remotes/',each,re.IGNORECASE):
            pass
        else:
            branchs.append(each[2:])
    print('total '+str(len(branchs))+' branches:')
    for branch in branchs:
        print(branch)    
# used for record infomation.

def record_info(info):
    with open(FILE,'w') as f:
        f.write(info)
        
def get_input():
    input_info = []
    print('please select one branch:')
    msg = raw_input()
    if msg in branchs:
        input_info.append(msg)
    else:
        print('Not a good branch name! please type again!')
    print('how many do you want? the range is from 1 to 10 ')
    num = int(raw_input())
    if num > 10 or num < 1:
        print('bad number!!! please input again!')
    input_info.append(num)
    return input_info

def output():
    print 'Author'.ljust(15) + '  ' + 'Email'.ljust(20) + '  ' + 'num'.ljust(8) + '  ' + 'message'.ljust(20)
    print('=========================================================================')
    for commit in commits:
        print(commit['author'].ljust(15) + ' ' + commit['email'][:20].ljust(20) + ' ' +commit['num'][:7].ljust(8) + '  ' + commit['message'])

if __name__ == '__main__':
    while(1):
        get_branch()
        input_list = get_input()
        info = GetLogInfo(input_list)
        record_info(info)
        ParseLog(FILE)
        output()
        
