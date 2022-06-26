import argparse

from secconfig.config import (
    generate_env_params,
    store_env,
    load_env,
    create_secconfig,
    load_secconfig,
)


def prog_generate_env(args):
    params = generate_env_params()
    if args.verbose:
        for (key, param) in params.items():
            print(f"{key}={param}")
    if args.file:
        store_env(params, path=args.file)
    else:
        store_env(params)


def prog_create_secconfig(args):
    load_env(path=args.envfile)
    with open(args.infile, "r") as infp:
        config_data = infp.read()
        secconfig = create_secconfig(config_data)
    if args.verbose:
        print(secconfig)
    with open(args.outfile, "w") as outfp:
        outfp.write(secconfig)


def prog_show_secconfig(args):
    load_env(path=args.envfile)
    with open(args.infile, "r") as infp:
        secconfig = infp.read()
        config_data = load_secconfig(secconfig)
    with open(args.outfile, "w") as outfp:
        outfp.write(config_data)


def run():
    parser = argparse.ArgumentParser(description="Create secure configurations")
    subparser = parser.add_subparsers()
    genenv = subparser.add_parser("env-file")
    genenv.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose output, be careful, because it prints secret information!",
    )
    genenv.add_argument(
        "-f",
        "--file",
        type=str,
        default=None,
        help="Filename to store the generated values",
    )
    genenv.set_defaults(func=prog_generate_env)
    create = subparser.add_parser("create")
    create.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose output, be careful, because it prints secret information!",
    )
    create.add_argument(
        "-i",
        "--infile",
        type=str,
        help="Configuration filename to be secured",
    )
    create.add_argument(
        "-o",
        "--outfile",
        type=str,
        default=None,
        help="output filename for the secure configuration",
    )
    create.add_argument(
        "-e",
        "--envfile",
        type=str,
        default=None,
        help="environment filename for the protection parameter (default: .env)",
    )
    create.set_defaults(func=prog_create_secconfig)
    show = subparser.add_parser("show")
    show.add_argument(
        "-i",
        "--infile",
        type=str,
        help="Configuration filename to be secured",
    )
    show.add_argument(
        "-o",
        "--outfile",
        type=str,
        default=None,
        help="output filename for the secure configuration",
    )
    show.add_argument(
        "-e",
        "--envfile",
        type=str,
        default=None,
        help="environment filename for the protection parameter (default: .env)",
    )
    show.set_defaults(func=prog_show_secconfig)
    args = parser.parse_args()
    exit(args.func(args))


if __name__ == "__main__":
    run()
