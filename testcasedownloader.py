from bs4 import BeautifulSoup
import re
import os
import requests
import os,math
import shutil
import sys

#"C:\Users\Sharma\Desktop\Projects\Python\Contest"

#freopen("", "r", stdin)
#freopen("output.txt", "w", stdout)

#url = "https://codeforces.com/contest/1342"

os.chdir(os.path.dirname(os.path.abspath(__file__)))    #Change Directory to current directory

print('\n\n*************************** Alert ****************************')
print('Remember to Change directory of terminal to current directory')
print('**************************************************************\n\n')
url=input('Enter Contest URL: ')
print('\n')

print('************  Ok!!  ****************')
try:
    data = requests.get(url)
    corweb=re.findall('codeforces.com/contest',url)
    if(len(corweb)==0):
        print("Incorrect Website\n")
        exit(0)

    soup = BeautifulSoup(data.content, 'lxml')
    pTable = soup.find("table", {"class": "problems"})
    s=str(pTable)
    problem=re.findall('<a href="(.*)">\r\n\s*(.*)\r',s)
    n=len(problem)
    ext=".cpp"

    cnt=0
    print('\n********************* Have a cup of tea *************************\n\n')
    for i in problem:
        a, qname = i
        print('Downloading problem '+str(qname)+'.................\n')

        p_url = url+"/problem/"+str(qname)      # Problem URL
        p_data=requests.get(p_url)
        soup=BeautifulSoup(p_data.content,'lxml')               #Parse Url data
        inp=soup.findAll('div',{'class':'input'})               #input data
        out=soup.findAll('div',{'class':'output'})              #output data
        Tcheck=soup.findAll('div',{'class':'input-specification'})      # Check if t or n  

        test_cases = re.search(' t ', str(Tcheck))        #Search if t (testcase) is present
        test_casesx=re.search(' T ',str(Tcheck))

        tflag = 1
        if(test_cases is None):
            if(test_casesx is not None):
                tflag = 1
            else:
                tflag=0

        tes=[]
        for j in inp:
            inputS = re.findall('<pre>(.*)?</pre', str(j), re.DOTALL)
            tes.append(inputS[0])

        tot_test=0
        act_test=""
        resin="" 
        if(tflag):
            for k in range(len(tes)):
                pos = 1
                if((str(tes[k][2])).isnumeric()):
                    pos = 2
                if pos == 2:
                    tot_test += int(tes[k][pos:pos+2])
                    act_test += str(tes[k][pos+2:])

                else:
                    tot_test += int(tes[k][pos])
                    act_test += str(tes[k][pos+1:])

            resin=str(tot_test)+(act_test)
                    
        else:
            tot_test=len(tes)
            for k in range(len(tes)):
                pos = 1
                act_test+=str(tes[k][pos:])

            resin=str(tot_test)+"\n"+(act_test)
            
        ansx=[]
        for k in out:
            outputS=re.findall('<pre>\n(.*)?</pre',str(k),re.DOTALL)
            ansx.append(outputS[0])

        act_ans=""

        for i in ansx:
            act_ans+=str(i)

        
        # resin is the final input string 
        # act_ans  is the final output string

        alert="\n\\\\"+'******************* This problem doesnt have multiple testcases but input.txt has concatenated testcases and has "t" !!!!! **********************\n\\\\************************ So remove t before submitting the solution ************************\n\n'

        filename=open(str(qname)+ext,'w')          # CPP files Create
        shutil.copy('Template.txt',str(qname)+ext)
        filename.close()
        filename=open('output.txt','w')
        filename = open(str(qname)+ext, 'r')
        filenameAr=filename.readlines()
        filenameAr[24] = '\tfio;\n\tfreopen(\"'+str(qname)+"in.txt\",\"r\",stdin);" +'\n\tfreopen("output.txt", \"w\", stdout);'
        if(not tflag):
            filenameAr[25]= alert

        filename.close()

        filename = open(str(qname)+ext, 'w')
        filename.writelines(filenameAr)
        filename.close()
        
        filename=open(str(qname)+"in.txt",'w')      # Input file create
        filename.write(resin)
        filename.close()
        filename=open(str(qname)+"out.txt",'w')     # Output file create
        filename.write(act_ans)
        filename.close()
        print('*********************** Done!!! *************************\n\n')


except Exception as ex:
    print("Network Error or No server Response or "+str(ex))
    exception_type, exception_object, exception_traceback = sys.exc_info()
    line_number=exception_traceback.tb_lineno
    print('Error at line '+str(line_number))

