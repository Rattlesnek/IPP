
import argparse









if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', help='file with XML representation of source code')
    parser.add_argument('--input', help='file with inputs for interpretation')
    args = parser.parse_args()
    
    if not (args.source or args.input):
        parser.error('Need to specify at least one of the arguments: --source / --input')

    
    
