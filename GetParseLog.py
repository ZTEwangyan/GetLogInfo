# parse the Git log in python
import sys
import re
import subprocess
# create a dict to store the log information
commits = []
def ParseLog(commitLines):
    # each log information
    commit = {}
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
def GetLogInfo():
    #print('GetLogInfo()')
    command = ['git','log','-2']
    #p       = subprocess.Popen(command,stdout = subprocess.PIPE)  #Is pipe need close??
    #stdout,stderr = p.communicate()
    stdout  = subprocess.check_output(command)
    return stdout
if __name__ == '__main__':
    info = GetLogInfo()
    print(info)
    f = open('commit.txt','w+')
    f.write(info)
    f.close()
    f = open('commit.txt','r')
    ParseLog(f)
    f.close()
    #ParseLog(sys.stdin.readlines())
    print 'Author'.ljust(15) + '  ' + 'Email'.ljust(20) + '  ' + 'num'.ljust(8) + '  ' + 'message'.ljust(20)
    print('=========================================================================')
    for commit in commits:
        print(commit['author'].ljust(15) + ' ' + commit['email'][:20].ljust(20) + ' ' +commit['num'][:7].ljust(8) + '  ' + commit['message'])
