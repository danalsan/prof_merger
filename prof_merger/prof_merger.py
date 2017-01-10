# Copyright 2017 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import argparse
import os
import pstats


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--in', '-i', default='./', dest='input_path',
                        help='Path to the prof files')
    parser.add_argument('--out', '-o', dest='output_file', required=True,
                        help='Output file')
    parser.add_argument('-f', dest='filter_string', default = '',
                        help='Filter string for input files (eg. 01012017)')
    args = parser.parse_args()

    stats = None
    # Process all files in input dir
    for filename in os.listdir(args.input_path):
        try:
            if args.filter_string not in filename:
                continue
            if not stats:
                stats = pstats.Stats(filename)
                print("Adding file %s" % filename)
            else:
                stats.add(filename)
                print("Adding file %s" % filename)
        except Exception:
            pass

   # Write combined file
    if stats:
        print("Writing results to %s" % args.output_file)
        stats.dump_stats(args.output_file)

if __name__ == "__main__":
    main()
