#!/usr/bin/env python

from __future__ import print_function

import os
import sys

import dummy_thirdparty1


def main():
    print("args: {}".format(sys.argv))
    print("current dir: {}".format(os.getcwd()))
    sys.exit(0)


if __name__ == "__main__":
    main()
