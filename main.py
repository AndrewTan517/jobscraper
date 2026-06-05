import argparse

SCRAPERS = {}


def create_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="site")

    for site, (add_arguments, scrape) in SCRAPERS.items():
        subparser = subparsers.add_parser(site)
        add_arguments(subparser)
        subparser.set_defaults(scrape=scrape)

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    args.scrape(args)


if __name__ == "__main__":
    main()
