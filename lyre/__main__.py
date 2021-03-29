import argparse
from datetime import timedelta
import logging
from pywinauto import Application  # type: ignore
import sys
from typing import List, Optional
from .player import Chord, Player

_moduleLogger = logging.getLogger(__name__)
_moduleLogger.addHandler(logging.NullHandler())


def _get_tempo(tempo_str: str) -> timedelta:
    bpm = int(tempo_str)
    ms = 60_000.0 / (int(bpm))
    _moduleLogger.info(f"Tempo = {ms}ms")
    return timedelta(milliseconds=ms)


def _main(args: argparse.Namespace) -> int:
    with open(args.input, "r") as f:
        header = f.readline().split()
        tempo = _get_tempo(header[0])
        loop = len(header) > 1 and header[1] == "loop"
        chords = [Chord.from_str(tempo, line) for line in f.readlines()]

    app = Application().connect(title="Genshin Impact", visible_only=True)  # type: ignore
    with Player(app.window().wrapper_object(), loop=loop) as player:  # type: ignore
        player.play([chord for chord in chords if chord is not None])

    return 0


def _parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("input", help="The file(s) to process")

    debug_group = parser.add_argument_group("Debug")
    debug_group.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Print debug information.  Can be repeated for more detailed output.",
    )
    debug_group.add_argument(
        "-q",
        "--quiet",
        action="count",
        default=0,
        help="Print only essential information.  Can be repeated for quieter output.",
    )
    debug_group.add_argument(
        "--doctest", action="store_true", default=False, help="Run doctests then quit."
    )

    args = parser.parse_args(argv)

    # We want to default to WARNING
    # Verbosity gives us granularity to control past that
    if args.verbose > 0 and args.quiet > 0:
        parser.error("Mixing --verbose and --quiet is contradictory")
    verbosity = 2 + args.quiet - args.verbose
    verbosity = min(max(verbosity, 0), 4)
    args.logging_level = [
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL,
    ][verbosity]

    if args.doctest:
        return args

    return args


def main(argv: Optional[List[str]] = None):
    if argv is None:
        argv = sys.argv[1:]
    args = _parse_args(argv)

    if args.doctest:
        import doctest

        result = doctest.testmod()
        print(result)
        sys.exit(0 - result.failed)

    log_format = "(%(asctime)s) %(levelname)-5s %(name)s.%(funcName)s: %(message)s"
    logging.basicConfig(level=args.logging_level, format=log_format)

    sys.exit(_main(args))


if __name__ == "__main__":
    main()
