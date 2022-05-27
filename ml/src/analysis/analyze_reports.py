import os
import re

reports_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'reports')

algorithms = ['ada_c', 'forest_c', 'gboost_c', 'gnb_c', 'knn_c', 'logreg_c', 'mlp_c', 'svc_c', 'tree_c', 'ada_r', 'forest_r', 'gboost_r', 'linreg_r', 'mlp_r', 'svr_r', 'tree_r']
categories = ['CSRHN6', 'CSRHN5', 'CSRHN3', 'CSRHN2', 'CSRH6', 'CSRN6', 'CSHN6', 'CRHN6', 'SRHN6', 'C6', 'S6', 'R6', 'H6', 'N6', 'CSR6', 'CSH6', 'CRH6', 'CH6']
def analyze_reports(extract_info):
    print("Algorithm".ljust(10), end='')    
    print("".join(["{:7}".format(c) for c in categories])) # print all categories with 7 characters
    for algorithm in algorithms:        
        print(algorithm.ljust(10), end='') # print algorithm with 10 characters
        for category in categories:
            with open(os.path.join(reports_folder, category, algorithm + ".report.txt"), 'r') as f:
                text = f.read()
                info = extract_info(text)
               
                if len(info) > 5: # if string length is more than 5, truncate it
                    info = info[:5]
                if len(info) < 5: # if string length is less than 5, add zeros to end of string
                    info = info + '0' * (5 - len(info))
                print(info.ljust(7), end='')
        print()

#analyze_reports(lambda text : re.search(r'Total Time elapsed: (.*?) \((.*?) seconds\)', text).group(2))
analyze_reports(lambda text : re.search(r'Prediction Time: (.*?) milliseconds', text).group(1))

