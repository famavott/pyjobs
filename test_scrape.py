"""Module to test for scrape.py module."""
import pytest


def test_indeed_search():
    """Verify indeed_search is returning list object."""
    from scrape import indeed_search
    assert type(indeed_search('python', {'chicago'}, {'engineer'})) is list
