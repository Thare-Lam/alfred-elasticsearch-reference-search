import sys
from workflow import Workflow3, web, ICON_SYNC

url = 'https://search.elastic.co/suggest'
tags = 'Elasticsearch'
home = 'https://www.elastic.co'


def main(wf):
    if len(wf.args) == 0:
        return
    params = dict(tags=tags, q=' '.join(wf.args))
    r = web.get(url, params)
    r.raise_for_status()
    result = r.json()
    for hit in result['hits']:
        wf.add_item(title=format_title(hit['title']), subtitle=format_subtitle(hit['breadcrumbs']),
                    arg=format_url(hit['url']), valid=True)
    wf.send_feedback()


def format_title(title):
    return title.replace('<em>', '').replace('</em>', '')


def format_subtitle(breadcrumbs):
    return breadcrumbs.replace('&raquo;', '>>')


def format_url(url):
    return home + url


if __name__ == '__main__':
    wf = Workflow3(help_url='https://github.com/Thare-Lam/alfred-elasticsearch-reference-search',
                   update_settings={
                       'github_slug': 'Thare-Lam/alfred-elasticsearch-reference-search',
                       'frequency': 1
                   })

    if wf.update_available:
        wf.add_item('New version available', 'Action this item to install the update',
                    autocomplete='workflow:update', icon=ICON_SYNC)

    sys.exit(wf.run(main))
