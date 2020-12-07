from module2.src.dataset_reader import read_dataset as reader
from module2.src.preprocessor import Preprocessor


if __name__ == '__main__':
    data = reader()
    preprocess = Preprocessor()
    for msg in data:
        clean = preprocess.process(msg[1])
        pass
