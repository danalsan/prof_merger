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
import sys


def process_dir(input_path, filter_string, out_stream):
    stats = None
    # Process all files in input dir
    for filename in os.listdir(input_path):
        try:
            if filter_string not in filename:
                continue
            if not stats:
                stats = pstats.Stats(filename, stream=out_stream)
                print("Adding file %s" % filename)
            else:
                stats.add(filename)
                print("Adding file %s" % filename)
        except Exception:
            pass
    return stats


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--in', '-i', default='./', dest='input_path',
                        help='Directory where prof files are located or path '
                             'of the input file to be formatted')
    parser.add_argument('--out', '-o', dest='output_file', required=False,
                        help='Output file')
    parser.add_argument('--txt', '-t', dest='txt_file', required=False,
                        help='Output file containing stats in text format')
    parser.add_argument('-f', dest='filter_string', default='',
                        help='Filter string for input files (eg. 01012017)')
    parser.add_argument('-p', dest='stats_filter', default='', required=False,
                        nargs='*', help='Sequence of filters to be applied'
                                        'for text formatting')
    parser.add_argument('--sort', '-s', dest='stats_sort',
                        default='cumulative', help='Field to sort by when '
                                                   'text formatting')
    args = parser.parse_args()

    out_stream = None

    if args.txt_file:
        try:
            out_stream = open(args.txt_file, "w+")
        except Exception:
            print("Cannot create output file %s" % args.txt_file)
            sys.exit(1)

    if os.path.isdir(args.input_path) and (args.output_file or args.txt_file):
        stats = process_dir(args.input_path, args.filter_string, out_stream)
        if stats and args.output_file:
            # Write combined file
            print("Writing results to %s" % args.output_file)
            stats.dump_stats(args.output_file)
    elif os.path.isfile(args.input_path) and not args.output_file:
        if not args.txt_file:
            print("--txt parameter is required when input is a file")
            sys.exit(1)
        try:
            stats = pstats.Stats(args.input_path, stream=out_stream)
        except Exception:
            print("Invalid input file")
            out_stream.close()
            sys.exit(1)
    else:
        print("Wrong parameters")
        parser.print_help()
        if out_stream:
            out_stream.close()
        sys.exit(1)

    if not stats and out_stream:
            os.unlink(out_stream.name)
	    print("No stats produced")
    else:
        try:
            stats.sort_stats(args.stats_sort)
        except KeyError:
            print("Wrong sort value '%s'" % args.stats_sort)
        else:
            print("Writing text results to %s" % args.txt_file)
            statsfilter = [int(s) if s.isdigit() else s for s in args.stats_filter]
            stats.print_stats(*statsfilter)
    out_stream.close()

if __name__ == "__main__":
    main()
