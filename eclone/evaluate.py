import sys
import os
import copy
import traceback
import random
import logging
import eclone

evm_dir = "/home/aliu/Research/Projects/eclone-eval/evm-bytecode-clone/bin-runtime/result"
#evm_dir = "/home/aliu/Research/Projects/eclone-eval/evm-bytecode-clone/bin-runtime"
evm_opt_dir = "/home/aliu/Research/Projects/eclone-eval/evm-bytecode-clone/bin-runtime-optimize/result"
#evm_opt_dir = "/home/aliu/Research/Projects/eclone-eval/evm-bytecode-clone/bin-runtime-optimize"
dataset_file = "/home/aliu/Research/Projects/eclone-eval/datafile/dataset"

N_contracts = 1
THRESHOLD = 0.5


def prepare_contracts():
	noopt = []
	contract_dirs = os.listdir(evm_dir)
	random.shuffle(contract_dirs)
	for i in range(10):
		d = os.path.join(evm_dir, contract_dirs[i])
		print d
		fs = os.listdir(d)
		if len(fs) == 0:
			continue
		else:
			seed = random.randint(0, len(fs) - 1)
			if fs[seed].endswith("bin-runtime"):
				f = os.path.join(d, fs[seed])
				noopt.append(f)
 
	print noopt, len(noopt)
	return noopt

def prepare_dataset(contracts, data_file, n_false):
	with open(data_file, 'a+') as f:
		for i in range(0, len(contracts)):
			f_noopt = contracts[i]
			f_opt = f_noopt.replace(evm_dir, evm_opt_dir)
			data_true = f_noopt + ',' + f_opt + ',1\n'
			f.write(data_true)
		for i in range(0, n_false):
			f_1 = contracts[i]
			f_1_base = os.path.basename(f_1)
			s = random.randint(0, len(contracts))
			f_2 = contracts[s]
			f_2_base = os.path.basename(f_2)
			while f_1_base == f_2_base:
				s = random.randint(0, len(contracts))
				f_2 = contracts[s]
				f_2_base = os.path.basename(f_2)
			f_2 = f_2.replace(evm_dir, evm_opt_dir)
			data_false = f_1 + ',' + f_2 + ',0\n'
			f.write(data_false)
	f.close()
	print "Evaluation dataset finished: " + data_file

def run_evaluation():
	with open(dataset_file, 'r') as f:
		count = 0
		# TODO: tp,tn,fp,fn

		
		argv_bak = sys.argv
		for line in f:
			sys.argv = argv_bak

			query = line.split(',')[0]
			target = line.split(',')[1]
			label = int(line.split(',')[2]) # 0 for not clone or 1 for clone

			try:
				argv_qt = copy.copy(argv_bak)
                argv_qt.extend(['--clone', query, target])
                sys.argv = copy.copy(argv_qt)
                qt_json = eclone.main()

                argv_qq = copy.copy(argv_bak)
                argv_qq.extend(['--clone', query, query])
                sys.argv = copy.copy(argv_qq)
                qq_json = eclone.main()
            except Exception as e:
            	traceback.print_exc()
            	continue

            if qq_json["score"] == 0:
            	continue
            
            # aliu: query-target / query-query
            relative_similarity = qt_json["score"] / qq_json["score"]
            if relative_similarity >= THRESHOLD:
                result = 1 # identified as clones
            else:
                result = 0 # identified as not clones




def fse_eval():
    count = 0
    correct = 0
    argv_bak = sys.argv
    for root, dirs, files in os.walk(evm_dir):
        path = root.split(os.sep)
        print((len(path) - 1) * '---', os.path.basename(root))
        for file in files:
            sys.argv = argv_bak
            if count >= N_contracts:
                return {"correct": correct, "total": count}
            print(len(path) * '---', file)
            #print(os.path.abspath(root + '/' + file))
            query = os.path.abspath(root + '/' + file)
            print(query)
            target = query.replace(evm_dir, evm_opt_dir)
            print(target)

            try:
                argv_qt = copy.copy(argv_bak)
                argv_qt.extend(['--clone', query, target])
                sys.argv = copy.copy(argv_qt)
                qt_json = eclone.main()

                argv_qq = copy.copy(argv_bak)
                argv_qq.extend(['--clone', query, query])
                sys.argv = copy.copy(argv_qq)
                qq_json = eclone.main()
            except Exception as e:
            	traceback.print_exc()
            	continue

            if qq_json["score"] == 0:
            	continue
            
            # aliu: query-target / query-query
            relative_similarity = qt_json["score"] / qq_json["score"]

            if relative_similarity >= THRESHOLD:
            	print("Relative Similarity: " + str(relative_similarity))
                print("Clone Found: " + query + ", " + target)
                correct += 1
            else:
                print("Clone Not Found: " + query + ", " + target)

            #sys.argv.extend(['--clone', query, target])
            #print sys.argv
            
            #eclone_json = eclone.main()
            #print eclone_json
            #print("## EClone Clone Detection: " + str(eclone_json["score"]))
            #print("## Number of basic block in query: " + str(eclone_json["nquery"]))
            #print("## Number of basic block in target: " + str(eclone_json["ntarget"]))
            count += 1

    #eclone.main()
    print("EClone Accuracy: " + str( correct / float(count) ))


if __name__ == '__main__':
	picked = prepare_contracts()
	prepare_dataset(picked, dataset_file, 4)
    #out = fse_eval()
    #print("EClone Accuracy: " + str( out["correct"] / float(out["total"]) ))