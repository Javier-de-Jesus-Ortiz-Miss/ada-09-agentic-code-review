"""Search and validate customer queries."""

from collections.abc import Iterable

from .models import Customer


def search_customers(
    term: str, customers: Iterable[Customer], *, field: str = "all"
) -> list[Customer]:
    """I return customers matching the selected field(s) in input order."""
    if not isinstance(field, str) or field not in ("all", "name", "email"):
        raise ValueError("El campo de búsqueda debe ser all, name o email.")

    if not isinstance(term, str):
        raise ValueError("El término de búsqueda debe ser texto.")

    query = term.strip().casefold()
    if not query:
        raise ValueError("Escribe un término de búsqueda no vacío.")

    return [
        customer
        for customer in customers
        if (field in ("all", "name") and query in customer.name.casefold())
        or (field in ("all", "email") and query in customer.email.casefold())
    ]
