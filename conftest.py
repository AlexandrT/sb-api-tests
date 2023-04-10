import pytest
import sys
import os

from py.xml import html
from tests.conftest import ValueStorage


pytest_plugins = ['fixtures.common_fixtures', 'fixtures.json_fixtures']

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj

    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
         description = ' '.join((pref, suf))
         #item._nodeid = description.encode('utf-8', errors='replace').decode('cp1251', 'replace')
         item._nodeid = description

@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    del cells[3]
    del cells[2]

    cells.insert(2, html.th(u'Запрос'))
    cells.insert(3, html.th(u'Ответ'))
    cells.insert(4, html.th(u'Статус-код'))
    cells[0] = html.th(u'Статус')
    cells[1] = html.th(u'Описание')

@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    name = report.nodeid#.encode('cp1251', errors='replace').decode('utf-8', 'replace')
    cells[1] = html.td(name, class_="col-name")

    del cells[3]
    del cells[2]

    try:
        cells.insert(2, html.td(report.curl))
        cells.insert(3, html.td(report.response))
        cells.insert(4, html.td(report.status_code))
    except AttributeError:
        pass

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    report.curl = ValueStorage.request
    report.status_code = ValueStorage.status_code
    report.response = ValueStorage.response
