import sys
import json
import os
import geojson
from pygeotools.utils.polygon import Polygon


PRECISION = 5
PROGRESSBAR_LEN = 50


def main(args=None):
    # jsondir = args.jsondir if args and args.jsondir else "."

    errors = list()
    step = 1

    file = args[1] if len(args) > 1 else "data.geojson"
    output_dir = args[2] if len(args) > 2 else "json"
    with open(file) as data_file:
        data = data_file.read()

    print("Step {0:d} : IMPORT {1:s}".format(step, os.path.abspath(file)), flush=True)
    features = geojson.loads(data).features
    offset, length = args.offset if args.offset else 0, args.length if args.length else 0

    total, errs, count = min(offset + length, len(features)) - offset, 0, 0
    for feature in features[offset:min(offset + length, len(features))]:
        outfile_name = os.path.join(output_dir, '{0:s}.json'.format(feature.properties['NAME']))

        count += 1
        progress = int(float(count) / total * PROGRESSBAR_LEN)
        print("Importing [{0:s}>{1:s}] {2:d}/{3:d} - {4:s} {5:s}".format(
            "=" * progress,
            " " * (PROGRESSBAR_LEN - progress),
            count,
            total,
            feature.properties['NAME'],
            "({0:d} error{1:s} found)".format(errs, "s" if errs > 1 else "") if errs else ""
        ), end="\r", flush=True)

        try:
            if feature.geometry.type == "Polygon":
                p = Polygon(feature.geometry.coordinates[0])
                hashcodes = p.fcover(precision=PRECISION)
                with open(outfile_name, 'w') as outfile:
                    json.dump(hashcodes, outfile)

            elif feature.geometry.type == "MultiPolygon":
                hashcodes = list()
                for polygon in feature.geometry.coordinates:
                     p = Polygon(polygon[0])
                     hashcodes.extend(p.fcover(precision=PRECISION))
                with open(outfile_name, 'w') as outfile:
                    json.dump(hashcodes, outfile)

        except Exception as e:
            errs += 1
            errors.append(feature.properties["NAME"])

    total += count
    step += 1
    print(flush=True)

    return total, len(errors), errors


if __name__ == "__main__":
    main(sys.argv)
