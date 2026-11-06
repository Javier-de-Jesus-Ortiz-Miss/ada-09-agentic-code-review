"""I exercise the production field selector for AC-11 through AC-13 and AC-15."""

import pytest

from customer_search import Customer, search_customers


CUSTOMERS = [
    Customer("email", "Bruno", "ana@example.com"),
    Customer("both", "Ana López", "ana.lopez@example.com"),
    Customer("neither", "Carla", "carla@example.com"),
    Customer("name", "Mariana", "mar@example.com"),
]


def test_default_and_explicit_all_preserve_two_argument_results():
    expected = [CUSTOMERS[0], CUSTOMERS[1], CUSTOMERS[3]]
    default = search_customers("ana", CUSTOMERS)
    explicit = search_customers("ana", CUSTOMERS, field="all")
    assert default == explicit == expected
    assert default is not CUSTOMERS
    assert explicit is not default
    assert explicit.count(CUSTOMERS[1]) == 1
    assert all(actual is original for actual, original in zip(explicit, expected))


@pytest.mark.parametrize(
    ("field", "expected_indices"),
    [("all", [0, 1, 3]), ("name", [1, 3]), ("email", [0, 1])],
)
def test_selected_field_matches_partial_trimmed_query_in_single_pass(field, expected_indices):
    customers = (customer for customer in CUSTOMERS)
    assert search_customers("  ANA  ", customers, field=field) == [
        CUSTOMERS[index] for index in expected_indices
    ]
    assert list(customers) == []


@pytest.mark.parametrize("field", ["name", "email"])
def test_selected_field_retains_unicode_casefold(field):
    selected = Customer(
        "selected",
        "Straße" if field == "name" else "Other",
        "straße@example.com" if field == "email" else "other@example.com",
    )
    excluded = Customer(
        "excluded",
        "Straße" if field == "email" else "Other",
        "straße@example.com" if field == "name" else "other@example.com",
    )
    assert search_customers("  STRASSE  ", [excluded, selected], field=field) == [selected]


@pytest.mark.parametrize("field", ["name", "email"])
@pytest.mark.parametrize("spaces", [" ", "  "])
def test_selected_field_preserves_interior_spaces(field, spaces):
    customers = [
        Customer("single", "Ana López", "ana lopez@example.com"),
        Customer("double", "Ana  López", "ana  lopez@example.com"),
    ]
    term = f"ANA{spaces}{'LÓPEZ' if field == 'name' else 'LOPEZ'}"
    expected = customers[0] if spaces == " " else customers[1]
    assert search_customers(f"  {term}  ", customers, field=field) == [expected]


@pytest.mark.parametrize("field", ["all", "name", "email"])
def test_selected_field_returns_empty_list_for_no_match(field):
    assert search_customers("absent", CUSTOMERS, field=field) == []
    assert search_customers("ana", iter(()), field=field) == []


@pytest.mark.parametrize(
    "field",
    ["", " ", "Name", "ALL", "EMAIL", " name", "email ", "id", None, 1, True,
     b"name", [], {}, {"name"}],
)
def test_invalid_selectors_raise_value_error_even_without_records(field):
    with pytest.raises(ValueError):
        search_customers("ana", iter(()), field=field)


@pytest.mark.parametrize("field", ["all", "name", "email"])
@pytest.mark.parametrize(
    ("term", "message"),
    [("", "no vacío"), (" \t\n", "no vacío"), (None, "debe ser texto"),
     (17, "debe ser texto"), (b"ana", "debe ser texto")],
)
def test_valid_selectors_retain_query_validation(field, term, message):
    with pytest.raises(ValueError, match=message):
        search_customers(term, CUSTOMERS, field=field)


def test_field_selector_is_keyword_only():
    with pytest.raises(TypeError):
        search_customers("ana", CUSTOMERS, "name")
