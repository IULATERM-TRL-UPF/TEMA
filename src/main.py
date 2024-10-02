

import train
import tema
import argparse
import os


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="TEMA")
    parser.add_argument("--act", required=True, help="pretraining (1) or TEMA (2)")
    parser.add_argument("--lang", required=True, help="source language")
    parser.add_argument("--l1", required=True, help="rich model")
    parser.add_argument("--l2", required=True, help="poor model")
    args = parser.parse_args()
    return args 


def main():
    """Main function."""
    args = parse_args()
    
    if args.act == 1:
        train.train(args.lang)
    else:
        tema.tema(args.l1,args.l2)
    
    
if __name__ == "__main__":
    main()




