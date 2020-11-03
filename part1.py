from abc import ABC, abstractmethod
import os
import argparse
import re
import time


class Strategy(ABC):
    """
    We're using the Strategy design pattern to dynamically change
    the strategy of computing number of function calls
    """
    def __init__(self):
        self.function_calls = {}

    def check_regex(self, line):
        func_calls = re.findall(r'(?!.*\{)\b\w+(?=\()', line)
        for func_call in func_calls:
            if func_call not in self.function_calls:
                self.function_calls[func_call] = 0
            self.function_calls[func_call] += 1

    @abstractmethod
    def compute_function_calls(self, line):
        pass


class ConcreteStrategyA(Strategy):
    """
    In this strategy, we are interested in the function calls that are added but not deleted.
    Also, we do not consider function calls in the context.
    """
    def compute_function_calls(self, line):
        if line[:1] == '+' and not line[:3] == '+++':
            self.check_regex(line)


class ConcreteStrategyB(Strategy):
    """
    In this strategy, we are interested in the function calls that are added OR deleted.
    Also, we do not consider function calls in the context.
    """

    def compute_function_calls(self, line):
        if (line[:1] == '+' and not line[:3] == '+++') \
                or (line[:1] == '-' and not line[:3] == '---'):
            self.check_regex(line)


class ConcreteStrategyC(Strategy):
    """
    In this strategy, we are interested in any kind of function calls (even in the context).
    """

    def compute_function_calls(self, line):
        self.check_regex(line)


class DiffEvaluator:
    def __init__(self, strategy):
        self.function_calls = {}
        self.files = {}
        self.regions = 0
        self.deleted_lines = 0
        self.added_lines = 0
        self._strategy = strategy

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        """
        Usually, the Context allows replacing a Strategy object at runtime.
        """

        self._strategy = strategy

    def evaluate(self, file_path):
        if file_path is not None and os.path.isfile(file_path):
            print('Evaluating %s ...' % file_path)
            file = open(file_path, 'r')

            while True:
                line = file.readline()
                if not line:
                    break

                line = line.strip('\n')

                # Skip empty lines
                if not line.replace(' ', ''):
                    continue

                if line[:10] == 'diff --git':
                    file_name = line[11:]
                    if file_name not in self.files:
                        self.files[file_name] = 0
                    self.files[file_name] += 1

                elif line[:2] == '@@':
                    self.regions += 1

                elif line[:1] == '+' and not line[:3] == '+++':
                    # don't consider the added lines that are just a space
                    if len(line.replace(' ', '')) > 1:
                        self.added_lines += 1

                elif line[:1] == '-' and not line[:3] == '---':
                    # don't consider the deleted lines that are just a space
                    if len(line.replace(' ', '')) > 1:
                        self.deleted_lines += 1

                self._strategy.compute_function_calls(line)

            self.function_calls = self._strategy.function_calls
            file.close()


def create_parser():
    parser = argparse.ArgumentParser(description='Parsing diff files')
    parser.add_argument('--input_path', type=str, default='diffs',
                        help='Path to the directory containing the diff files')
    parser.add_argument('--strategy', type=int, default=1,
                        help='What is you desired strategy to compute the number of function calls? '
                             '[default=1]')

    return parser


def main(args):
    start = int(round(time.time() * 1000))

    diffs_dir = args.input_path

    if args.strategy == 1:
        evaluator = DiffEvaluator(ConcreteStrategyA())
    elif args.strategy == 2:
        evaluator = DiffEvaluator(ConcreteStrategyB())
    else:
        evaluator = DiffEvaluator(ConcreteStrategyC())

    for file in os.listdir(diffs_dir):
        evaluator.evaluate(os.path.join(diffs_dir, file))

    stop = int(round(time.time() * 1000))

    print('Done!')
    print('Processing time: %s milliseconds' % (stop - start))

    # Write list of files in file_list.txt
    print('Writing file names in file_list.txt ...')
    with open('file_list.txt', 'w') as f:
        for file in evaluator.files.keys():
            f.write('%s\n' % file)
    f.close()

    # Write list of calls in calls_num.txt
    print('Writing file calls in calls_num.txt ...')
    with open('calls_num.txt', 'w') as f:
        for key, value in evaluator.function_calls.items():
            f.write('%s:%s\n' % (key, value))
    f.close()

    print('Number of files: %s' % len(evaluator.files))
    print('Number of regions: %s' % evaluator.regions)
    print('Number of lines added: %s' % evaluator.added_lines)
    print('Number of lines deleted: %s' % evaluator.deleted_lines)


if __name__ == "__main__":
    main(create_parser().parse_args())
