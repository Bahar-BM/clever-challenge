import json
import argparse
import time


class ASTParser:
    def __init__(self):
        self.variablesInfo = []

    def parse(self, file):
        variable_nodes = []
        input_ast = json.load(file)
        root_node = input_ast['Root']
        # Returns variable nodes
        recursive_visit(root_node, 'VariableDeclaration', variable_nodes)
        # For each variable node extract the declaration info
        self.variablesInfo = extract_variables_info(variable_nodes)


def extract_variables_info(variable_nodes):
    declaration_info = []
    for node in variable_nodes:
        variable_type = extract_node_value(node, 'PredefinedType')
        variable_name = extract_node_value(node, 'VariableDeclarator')
        declaration_info.append((variable_type, variable_name))
    return declaration_info


def recursive_visit(root, annotation, results):
    for child in root['Children']:
        if child['Type'] == annotation:
            results.append(child)
        else:
            recursive_visit(child, annotation, results)


def extract_node_value(node, annotation):
    node_value = []
    recursive_visit(node, annotation, node_value)
    if node_value:
        return node_value[0]['Children'][0]['ValueText']


def create_parser():
    parser = argparse.ArgumentParser(description='Parsing diff files')
    parser.add_argument('--input_json', type=str, default='ast/astChallenge.json',
                        help='The json file related to the input AST')

    return parser


def main(args):
    start = float(time.time() * 1000)
    input_json = args.input_json

    parser = ASTParser()
    with open(input_json) as file:
        print("Parsing the AST ...")
        parser.parse(file)

    stop = float(time.time() * 1000)
    print("Done!")
    print("Processing time: %s milliseconds" % (stop - start))

    for variable in parser.variablesInfo:
        print("{{{}}}{{{}}}".format(variable[0], variable[1]))


if __name__ == '__main__':
    main(create_parser().parse_args())
