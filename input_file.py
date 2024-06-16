from dataclasses import dataclass
from typing import List


@dataclass
class Input:
    name: str
    signature: str
    description: str
    examples: List[str]
    temperatures: List[float]
    k: int
    unit_tests: List[str]
    ground_truth: List[str]

    def __init__(self, file_name: str):
        try:
            with open(file_name, 'r', encoding="utf-8") as f:
                input_file = f.readlines()
                # Drop additional whitespace which are not significant
                input_file = [line.strip() for line in input_file]
                # Drop resulting and additional newlines which are not significant
                input_file = [line for line in input_file if line]
                input_iterator = iter(input_file)

                # Function name
                self.name = next(input_iterator)

                # Signature
                assert next(input_iterator) == '"""', "Expected start of docstring"
                self.signature = next(input_iterator)
                assert self.signature.startswith('signature:'), "Signature line should start with 'signature:'"
                self.signature = self.signature.replace('signature:', '').strip(';').strip()

                # Description
                self.description = ''
                while (line := next(input_iterator)) != '"""':
                    self.description += line + ' '
                self.description = self.description.strip()

                # Examples
                self.examples = []
                while (line := next(input_iterator)).startswith('example:'):
                    line = line.replace('example:', '').strip(';').strip()
                    self.examples.append(line)

                # Temperatures
                assert line.startswith('temperatures:'), "Expected 'temperatures:'"
                line = line.replace('temperatures:', '').strip(';').strip()
                self.temperatures = [float(t) for t in line.split(',')]

                # Number of samples (k)
                line = next(input_iterator)
                assert line.startswith('num'), "Expected 'num'"
                line = line.replace('num', '').strip('=; ').strip()
                self.k = int(line)
                assert 0 < self.k < 10

                # Unit tests and ground truth
                assert next(input_iterator) == 'unit_tests:', "Expected 'unit_tests:'"
                self.unit_tests = []
                self.ground_truth = []
                while line := next(input_iterator, None):
                    try:
                        unit_test, ground_truth = line.strip(';').split('->')
                        self.unit_tests.append(unit_test.strip())
                        self.ground_truth.append(ground_truth.strip())
                    except ValueError as e:
                        print(f"Error parsing unit test line: {line} - {e}")

        except FileNotFoundError:
            print(f"File {file_name} not found.")
        except StopIteration:
            print("Unexpected end of input file.")
        except Exception as e:
            print(f"An error occurred: {e}")
