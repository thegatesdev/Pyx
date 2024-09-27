import itertools
import base64
import argparse
import sys

def xor_bytes(key: bytes, input: bytes, fill: int = 0, cycle_key: bool = False) -> bytes:
    zipped = zip(itertools.cycle(key), input) if cycle_key else itertools.zip_longest(key, input, fillvalue=fill)
    return bytes(a ^ b for a,b in zipped)

def pyx(key: str,
           input: str,
           input_base64: bool = False,
           output_base64: bool = False,
           codec: str = 'UTF-8',
           fill: int = 0,
           cycle_key: bool = False
           ) -> str:
    input = input.encode(codec)
    input = base64.b64decode(input) if input_base64 else input
    key = key.encode(codec)
    result = xor_bytes(key, input, fill, cycle_key)
    result = base64.b64encode(result) if output_base64 else result
    return result.decode(codec)

def pyx_cmdl_parse():
    parser = argparse.ArgumentParser(description='Overengineered XOR cyphering')
    parser.add_argument('-k', '--key', required=False)
    parser.add_argument('-i', '--input', required=False)
    parser.add_argument('--input-base64', action='store_true')
    parser.add_argument('--output-base64', action='store_true')
    parser.add_argument('-c', '--codec', default="UTF-8")
    parser.add_argument('-f', '--fill', type=int, default=0)
    parser.add_argument('-l', '--cycle-key', action='store_true')
    return parser.parse_args()

def pyx_cmdl():
    args = pyx_cmdl_parse()
    input = args.input or sys.stdin.read()
    print(pyx(args.key or "", input, args.input_base64, args.output_base64, args.codec, args.fill, args.cycle_key))
    
pyx_cmdl()