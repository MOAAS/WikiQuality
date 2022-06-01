import matplotlib.pyplot as plot
import os
import pandas as pd


dataset_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'datasets')


def load_dataset(dataset_name):
    train = pd.read_csv(os.path.join(dataset_folder, dataset_name + "_train.csv"))
    test = pd.read_csv(os.path.join(dataset_folder, dataset_name + "_test.csv"))

    # join the two datasets
    return pd.concat([train, test])

dataset = load_dataset('6000x6-csrhn')

def show_boxplot(column, ylim=None, disable_outliers=False):
    plot.figure(figsize=(7,5))
    plot.boxplot([
        dataset[dataset['Quality'] == 'FA'][column],
        dataset[dataset['Quality'] == 'GA'][column],
        dataset[dataset['Quality'] == 'B'][column],
        dataset[dataset['Quality'] == 'C'][column],
        dataset[dataset['Quality'] == 'Start'][column],
        dataset[dataset['Quality'] == 'Stub'][column],
    ], showfliers=not disable_outliers)
    
    plot.ylabel(column)
    plot.xlabel('Quality')
    plot.xticks([1,2,3,4,5,6], ['FA', 'GA', 'B', 'C', 'Start', 'Stub'])
    if ylim:
        plot.ylim(ylim[0], ylim[1])

    plot.draw()
    plot.pause(1) # https://stackoverflow.com/a/22899859
    plot.waitforbuttonpress(0)

def list_average_columns(columns, num_decimals=2, col_width=7):
    to_format = f'{{:<{col_width}}}' * 8

    print(to_format.format('Column', 'Avg', 'FA', 'GA', 'B', 'C', 'Start', 'Stub'))
    for column in columns:
        # compute the average readability for each quality
        means = "".join([str(round(dataset[dataset['Quality'] == quality][column].mean(), num_decimals)).ljust(col_width) for quality in ['FA', 'GA', 'B', 'C', 'Start', 'Stub']])
        avg = round(dataset[column].mean(), num_decimals)
        print(column.ljust(col_width) + str(avg).ljust(col_width) + means)



def get_fa_ranges():
    columns = [ 
        "CC", "CW", "CSN", "CS", "CMSL", "CP", "CMPL", "CLSL", "CSSL", "CSTDSL", "CLSSR", "CB", "CBPS", "CNL", "CNLTLR", "CR", 
        "CCC", "CCCPC", "CCCPS", "CEL", "CELPS", "CIL", "CI", "CIPS", "CIB", "CCT", "CNCT", "CTB", "CUCT", "SSLS", "SSSS", "SMSS", 
        "SLSR", "SSSR", "SS", "SMSPW", "SMCPW", "SWL6", "HA", "HAPR", "HRPD", "HRPC", "HRPCSD", "HR", "HC", "HRC", "HAC", "HRCPC", 
        "HACPC", "HRCPAC", "HREV", "HREVPR", "HRML", "HREC", "HRECPR", "HACT", "HACTPR", "HOCCPR", "HSSLE", "HMCL"
    ]

    fa = dataset[dataset['Quality'] == 'FA']
    fa = fa.drop(['Title', 'Quality'], axis=1)
    
    ranges = {}
    for column in columns:
        ranges[column] = {"name": "???", "range": [fa[column].quantile(0.33), fa[column].quantile(0.99)]}

    print("{")
    for k, v in ranges.items():
        k = '"' + k + '":'
        print(f'{k:13} {v},')
    print("}")

    return ranges





# show box plot with 'CC'
#show_boxplot('NIN', disable_outliers=True)

#list_average_columns(['RARI', 'RCL', 'RFK', 'RGFI', 'RSG', 'RLWF'])
#list_average_columns(['CC', 'CW', 'CSN', 'CCC', 'CNL', 'SV', 'HA', 'HR', 'NIN'], col_width=10)

get_fa_ranges()

