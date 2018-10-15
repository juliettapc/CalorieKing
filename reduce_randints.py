#! /usr/bin/env python
import sys
def read_ints(file_handle):
   for line in file_handle:
       if len(line.strip()) > 0:
           yield int(line.strip())

def main():
    data = read_ints(sys.stdin)
    total = 0
    for d in data:
        total += d
    print total
if __name__ == "__main__":
    main()
