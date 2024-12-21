# testing webscraping functions

import src.data.webscraping_functions as wf

def test_def():

    df = wf.scrape_def(2020)

    assert len(df) == 32

def test_qb():

    df = wf.scrape_pass(2024)

    assert len(df) != 0

df = wf.scrape_pass(2024)
print(df[:5])