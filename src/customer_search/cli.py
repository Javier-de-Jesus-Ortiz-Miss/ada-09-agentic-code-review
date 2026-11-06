"""Command-line interface for customer search."""

import argparse
import sys
from collections.abc import Sequence

from .data import CUSTOMERS
from .search import search_customers


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Busca clientes por nombre o correo.")
    parser.add_argument("term", help="Texto parcial del nombre o correo")
    parser.add_argument(
        "--field", choices=("all", "name", "email"), default="all",
        help="Campo de búsqueda (predeterminado: all)",
    )
    args = parser.parse_args(argv)

    try:
        matches = search_customers(args.term, CUSTOMERS, field=args.field)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    if not matches:
        print("No se encontraron clientes.")
        return 0

    for customer in matches:
        print(f"{customer.id} | {customer.name} | {customer.email}")
    return 0
