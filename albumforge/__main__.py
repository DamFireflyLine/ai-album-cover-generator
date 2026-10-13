"""Entry point: `python -m albumforge`."""

from __future__ import annotations

import sys

from albumforge.host.bootstrap import bootstrap


def main() -> int:
    return bootstrap(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())