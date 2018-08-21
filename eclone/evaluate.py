import sys
import os
import copy
import traceback
import random
import logging
import eclone
import datetime
import faulthandler
faulthandler.enable()

evm_dir = "/home/aliu/Research/Projects/eclone-eval/evm-bytecode-clone/bin-runtime/result"
#evm_dir = "/home/aliu/Research/Projects/eclone-eval/evm-bytecode-clone/bin-runtime"
evm_opt_dir = "/home/aliu/Research/Projects/eclone-eval/evm-bytecode-clone/bin-runtime-optimize/result"
#evm_opt_dir = "/home/aliu/Research/Projects/eclone-eval/evm-bytecode-clone/bin-runtime-optimize"
dataset_file = "/home/aliu/Research/Projects/eclone-eval/datafile/dataset_3000"
log_dir = "/home/aliu/Research/Projects/eclone-eval/datafile/"

# evaluation configuration
N_contracts = 1
N_CLONE = 3000
N_NON_CLONE = 3000
THRESHOLD = 0.5


def prepare_contracts():
    noopt = []
    contract_dirs = os.listdir(evm_dir)
    random.shuffle(contract_dirs)
    for i in range(N_CLONE):
        d = os.path.join(evm_dir, contract_dirs[i])
        print d
        fs = os.listdir(d)
        if len(fs) == 0:
            continue
        else:
            seed = random.randint(0, len(fs)-1)
            if fs[seed].endswith("bin-runtime"):
                f = os.path.join(d, fs[seed])
                noopt.append(f)
 
    #print noopt, len(noopt)
    print "## Total number of CLONES: " + str(len(noopt))
    return noopt

def prepare_dataset(contracts, data_file, n_false):
    with open(data_file, 'a+') as f:
        for i in range(0, len(contracts)):
            f_noopt = contracts[i]
            f_opt = f_noopt.replace(evm_dir, evm_opt_dir)
            data_true = f_noopt + ',' + f_opt + ',1\n'
            f.write(data_true)
        for i in range(0, n_false):
            if i >= len(contracts):
                break
            f_1 = contracts[i]
            f_1_base = os.path.basename(f_1)
            s = random.randint(0, len(contracts)-1)
            f_2 = contracts[s]
            f_2_base = os.path.basename(f_2)
            while f_1_base == f_2_base:
                s = random.randint(0, len(contracts)-1)
                f_2 = contracts[s]
                f_2_base = os.path.basename(f_2)
            f_2 = f_2.replace(evm_dir, evm_opt_dir)
            data_false = f_1 + ',' + f_2 + ',0\n'
            f.write(data_false)
    f.close()
    print "Evaluation dataset finished: " + data_file
    print "# of CLONES: " + str(len(contracts))
    print "# of NON-CLONES: " + str(i)

def run_evaluation():
    LOG_FILE = log_dir + 'LOG_' + datetime.datetime.today().strftime('%Y-%m-%d')
    with open(dataset_file, 'r') as f, open(LOG_FILE, 'a+') as lf:
        count = 0
        # TP, TN, FP (not clone, but identified as clone), FN (is clone, but identified as not clone)
        tp, tn, fp, fn = 0, 0, 0, 0

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
                result_label = 1 # identified as clones
            else:
                result_label = 0 # identified as not clones

            # aliu: compute TP, TN, FP, FN
            result_type = "NA"
            if result_label == label:
                if label == 1:
                    tp += 1
                    result_type = "TP"
                else:
                    tn += 1
                    result_type = "TN"
            else:
                if label == 1:
                    fn += 1
                    result_type = "FN"
                else:
                    fp += 1
                    result_type = "FP"


            count += 1
            print "\n++++ iteration " + str(count) + " ++++\n"
            # LOG_FILE: query, target, relative_similarity, result_label, result_type
            lf.write(query + ',' + target + ',' + str(relative_similarity) + ',' + str(result_label) + ',' + result_type + '\n')

        f.close()
        lf.close()

        print "++++ Evaluation Finished ++++"
        print "number of tests: " + str(count) + ", threshold: " + str(THRESHOLD)
        print "TP: " + str(tp) + ", " + "TN: " + str(tn) + ", " + "FP: " + str(fp) + ", " + "FN: " + str(fn)




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
    #picked = prepare_contracts()
    #prepare_dataset(picked, dataset_file, N_NON_CLONE)
    run_evaluation()
    #out = fse_eval()
    #print("EClone Accuracy: " + str( out["correct"] / float(out["total"]) ))