"""Module to test for scrape.py module."""
import pytest


def test_indeed_search():
    """Verify indeed_search returns list object."""
    from scrape import indeed_search
    assert type(indeed_search('python', {'chicago'}, {'engineer'})) is list


def test_builtin_search():
    """Verify builtin_searchis returns list object."""
    from scrape import builtin_search
    assert type(builtin_search({'developer'})) is list


def test_craigslist_search():
    """Verify craigslist_search returns list object."""
    from scrape import craigslist_search
    assert type(craigslist_search({'developer'})) is list


def test_matter_search():
    """Verify matter_search returns list object."""
    from scrape import matter_search
    assert type(matter_search({'developer'})) is list


# def test_dict_to_csv_ioerror():
#     """Raise IOError to test error handling of dict_to_csv."""
#     from scrape import dict_to_csv
#     columns = ['title', 'link', 'company', 'location', 'date']
#     final_list = [{'company': 'coffee store', 'title': 'barista'}]
#     csv_file = 'some/bad/path'
#     with pytest.raises(Exception):
#         dict_to_csv(csv_file, columns, final_list)
