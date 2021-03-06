from logflow.logsparser.Dataset import Dataset
from logflow.logsparser.Parser import Parser
from logflow.logsparser.Embedding import Embedding
from logflow.logsparser.Journal import Journal

from logflow.relationsdiscover.Dataset import Dataset as Dataset_learning
from logflow.relationsdiscover.Worker import Worker
from logflow.relationsdiscover.Result import Results

from logflow.logsparser import Pattern
from logflow.relationsdiscover import Model
from logflow.treebuilding.Dataset import Dataset as Dataset_building
from logflow.treebuilding.Workflow import Workflow

from os import listdir
from os.path import isfile

def parser_function(line):
    return line.strip().split()[4:]

def split_function(line):
    try:
        return line.strip().split()[3]
    except:
        return "1"

def sort_function(list_lines):
    return sorted(list_lines, key=lambda line: split_function(line))

if __name__== "__main__":
    path_logs = "data/Windows/"
    list_files = []
    for file in listdir(path_logs):
        if "x" in file:
            list_files.append(path_logs + "/" + file)

    # Find the patterns
    dataset = Dataset(list_files=list_files, parser_function=parser_function)
    patterns = Parser(dataset).detect_pattern()
    Dataset(list_files=list_files, dict_patterns=patterns, saving=True, path_data="data/", name_dataset="Test", path_model="model/", parser_function=parser_function, sort_function=sort_function)
    Embedding(loading=True, name_dataset="Test", path_data="data/", path_model="model/").start()

    # Learn the correlations
    size =  100000000 
    list_cardinalities = Dataset_learning(path_model="model/", path_data="data/", name_dataset="Test", size=size).run()
    worker = Worker(cardinalities_choosen=[4,5,6,7], list_cardinalities=list_cardinalities, path_model="model/", name_dataset="Test")
    worker.train()

    # Show the results
    results = Results(path_model="model/", name_model="Test")
    results.load_files()
    results.compute_results(condition="Test")
    results.print_results()
    
    # Get the tree
    dataset = Dataset_building(path_model="model/", name_model="Test", path_data="data/Windows/Windows.log", index_line_max=30000, parser_function=parser_function)
    dataset.load_files()
    dataset.load_logs()
    workflow = Workflow(dataset)
    workflow.get_tree(index_line=24712)



