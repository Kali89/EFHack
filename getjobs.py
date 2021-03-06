import sys
import pickle

def getJobs(filePath):
    
    inp = open(filePath, 'r')  # input
    inpf = open(filePath, 'r') # input, one line forward

    bizExp = []                # list of business experiences, bizexp[k] corresponds to k-th CV
    edu = []                   # list of educations, edu[k] corresponds to k-th CV
    job = {}                   # eg job['Financial Analyst'] = [23, 45, 52]
    company = {}               # eg company['Bain & Company'] = [2, 15]
    name = {}
    email = {}
    phoneNumber = {}
    cvCount = -1
    
    prevline = inpf.readline()
    line = inpf.readline()
    # print line, prevline
    while line != '':

        # print 'start again at line:', line
        cvCount += 1
        
        while not isEmail(line):
            prevline = line
            line = inpf.readline()
            # if 'FAISAL AZIZ' in line:
            #     print 'found Baran, exit0'
                # return
            if line == '': return bizExp, edu, job, company, name, email, phoneNumber, cvCount
            
        # print 'found beginning of a new CV! starts with:', prevline
        
        # found name: remove whitespace, add it to relevant dict
        print 'ADDING NAME', prevline.strip()
        name[prevline.strip()] = []
        name[prevline.strip()].append(cvCount)

        # found email: remove whitespace, add it to relevant dict
        email[line.strip()] = []
        email[line.strip()].append(cvCount)
        
        # prevline = line dont need this
        line = inpf.readline()
        # if 'FAISAL AZIZ' in line:
        #     print 'found Ravi, exit2'
        #     return
        # print line, prevline
        if line == '': return bizExp, edu, job, company, name, email, phoneNumber, cvCount
        
        # found phone number: remove whitespace, add it to relevant dict
        try :
            phoneNumber[line.strip()].append(cvCount)
        except:
            phoneNumber[line.strip()] = []
            phoneNumber[line.strip()].append(cvCount)
        
        # prevline = line dont need this
        line = inpf.readline()
        # if 'FAISAL AZIZ' in line:
        #     print 'found Ravi, exit3'
        #     return
        # print line, prevline
        if line == '': return bizExp, edu, job, company, name, email, phoneNumber, cvCount

        while 'EDUCATION' not in line:
            # prevline = line dont needd this
            line = inpf.readline()
            # if 'FAISAL AZIZ' in line:
            #     print 'found Ravi, exit4'
            #     return
            # print line, prevline
            if line == '': return bizExp, edu, job, company, name, email, phoneNumber, cvCount

        # found education: add it to relevant list
        while 'BUSINESS EXPERIENCE' not in line:
            try:
                edu[cvCount] += line
            except:
                edu.append(line)
            line = inpf.readline()
            # if 'FAISAL AZIZ' in line:
            #     print 'found Ravi, exit5'
            #     return
            # print line, prevline
            if line == '': return bizExp, edu, job, company, name, email, phoneNumber, cvCount

        # found business experience: add it to relevant list
        try:
            bizExp[cvCount] += line
        except:
            bizExp.append(line)
            
        # find next company
        while 'ADDITIONAL INFORMATION' not in line:
            #print line, '-> evaluating for bizExp'
            #return inpf, line
            while 'ADDITIONAL INFORMATION' not in line and threeConsecCaps(line) < 0:
                print line, '-> added to bizExp'
                line = inpf.readline()
                # if 'FAISAL AZIZ' in line:
                #     print 'found Ravi, exit6'
                #     return bizExp, edu, job, company, name, email, phoneNumber, cvCount
                # print line, prevline
                bizExp[cvCount] += line
                if line == '': return bizExp, edu, job, company, name, email, phoneNumber, cvCount

            i = threeConsecCaps(line)
            if i >= 0: # found company name: extract and add to relevant dict
                # print 'found company name:', line[i:].partition(',')[0]
                try:
                    company[line[i:].partition(',')[0]].append(cvCount)
                except:
                    company[line[i:].partition(',')[0]] = []
                    company[line[i:].partition(',')[0]].append(cvCount)

            # to find job, look for first line containing bullet point; job is in previous line
            while '\xe2\x80\xa2' not in line:
                prevline = line
                line = inpf.readline()
                # if 'FAISAL AZIZ' in line:
                #     print 'found Ravi, exit7'
                #     return
                # print line, prevline
                bizExp[cvCount] += line
                if line == '': return bizExp, edu, job, company, name, email, phoneNumber, cvCount
            
            # found job: remove whitespace, add it to relevant list
            # print 'found job:', prevline.strip()
            try:
                job[prevline.strip()].append(cvCount)
            except:
                job[prevline.strip()] = []
                job[prevline.strip()].append(cvCount)

            # move to end of job description, ie either next job or additional information
            while line[0]==' ':
                line = inpf.readline()
                # if 'FAISAL AZIZ' in line:
                #     print 'found Ravi, exit8'
                #     return
                # print line, prevline
                bizExp[cvCount] += line
                if line == '': return bizExp, edu, job, company, name, email, phoneNumber, cvCount

            # print 'should be ADDITIONAL INFORMATION or end of file:', line

        while 'NATIONALITY' not in line:
            line = inpf.readline()
            # if 'FAISAL AZIZ' in line:
            #     print 'found Ravi, exit9'
            #     return
            # print line, prevline

        # print line, 'met so exiting'
        #return bizExp, edu, job, company, name, email, phoneNumber, cvCount

    return bizExp, edu, job, company, name, email, phoneNumber, cvCount
                

def threeConsecCaps(line):
    for i in range(len(line)-3):
        if isDate(line[0:14]) and (line[14:15]).isupper() and (line[14:15]).isalpha(): return 14
        # if (line[i]+line[i+1]+line[i+2]).isupper() and (line[i]+line[i+1]+line[i+2]).isalpha() and line[i+3]==',': return i
    return -1

def isDate(line):
    if (line[0:3]).isdigit() and (line[4:7]) == ' - ' and (line[7:10]).isdigit() and (line[11:14]) == '   ': return True
    if (line[0:2]).isalpha() and (line[4:7]).isdigit() and (line[9:11]) == 'to' and (line[11:14]) == '   ': return True
    return False

def isEmail(line):
    if '@london.edu' in line: return True
    if '@gmail.com' in line: return True
    
def missingCVs(max, name):
    for num in range(max):
        found = False
        for key in name.keys():
            # print 'do', key, 'and', num, 'go together?'
            if name[key] == [num]: found = True
        if found == False: print 'CV number', num, 'missing!'



if __name__ == "__main__" :
    outfilename = sys.argv[1].partition('.')[0] + '_data.pickle'
    with open(outfilename, 'w') as f:
        bizExp, edu, job, company, name, email, phoneNumber, cvCount = getJobs(sys.argv[1])
        data = pickle.dump((bizExp, edu, job, company, name, email, phoneNumber, cvCount), f)
    # data = pickle(getjobs(sys.argv[1]))

# import getjobs
# bizExp, edu, job, company, name, email, phoneNumber, cvCount = getJobs('CVs/All.txt')
# getjobs.missingCVs(64, name)
