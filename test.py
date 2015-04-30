import argparse
 
parser = argparse.ArgumentParser(description='Demo')
parser.add_argument('--verbose',
    action='store_true',
    help='verbose flag')
 
v
 
if args.verbose:
    print("~ Verbose!")
else:
    print("~ Not so verbose")