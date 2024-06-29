import sys
import asyncio
import argparse
from stdlib import SuperError
from lexer import Lexer

parser = argparse.ArgumentParser(prog="superscript", description="Program anything, the fun way.")
parser.add_argument("file", type=str, help="What file should we run?", nargs="?", default=None)
parser.add_argument("--debug", help="Get more information", action="store_true")
args = parser.parse_args()


debug = False

if args.debug:
    debug = True
    print("Debug mode on. GLHF!")



if True:
    with open("test.super", "r") as file:
        text = file.read()
    lexer = Lexer(text)
    try:
        tokens = lexer.scanTokens()
    
    except SuperError as e:
        print(e)
        sys.exit(1)
    finally:
        if debug:
            print(tokens)
