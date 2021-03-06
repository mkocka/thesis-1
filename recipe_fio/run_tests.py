#/bin/python
#Tests generates workloads using fio(flexible input/output tool).
#script takes recipe in *-* format and desired number of iterations
#keby nieco dal som prec import os, tuto spravu odstranit ak nebude ziadny problem

import subprocess, sys, logging
logging.basicConfig(filename='./out/log.out',level=logging.DEBUG)

recipe = ' --'.join(sys.argv[1].split('-'))
_iter = str(sys.argv[2])
free = sys.argv[3]

subprocess.call('echo -n '+recipe+' --numjobs'+free+' >> ./out/recipe',shell=True)			
test ='fio --' + recipe + ' --write_bw_log=./out/job_'+_iter+' --output=./out/job_'+_iter+'.out'+' --write_iops_log=./out/job_'+_iter+' --numjobs='+free

logging.info('initializing')
logging.info(test)
subprocess.call(test,shell=True)	
logging.info('test over')
	 

