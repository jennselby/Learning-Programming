import sys
import json
import os.path

CATEGORY_HTML = \
'''
            <div class="panel panel-primary">
                <div class="category-item panel-heading">
                    <div class="panel-heading">
                        <div class="category-name panel-title">{cat_name}</div>
                        <div class="category-desc">{cat_desc}</div>
                    </div>
                </div>
                <div class="panel-body">
                    <ul class="category-suggestions-list list-group">
'''

SUGGESTION_HTML = \
'''
                    <li class="suggestion-item list-group-item {classes}">
                        <div class="suggestion-name"><a href="{url}">{name}</a></div>
                        <div class="suggestion-desc">{desc}</div>
                        <div class="suggestion-levels">Levels: {levels}</div>
                        <div class="suggestion-languages">Languages: {languages}</div>
                        <div class="suggestions-subjects">Topics: {subjects}</div>
                    </li>
'''

FILTER_HEADER_HTML = \
'''
            <div class="panel panel-primary">
                <div class="category-item panel-heading">
                    <div class="panel-heading">
                        <div class="filter-name panel-title">Filter by {filter_heading}</div>
                    </div>
                </div>
                <div class="panel-body">
                    <ul class="filter-list list-group" id="{filter_id}">
'''

FILTER_ITEM_HTML = \
'''
                        <li class="filter-item list-group-item showing" id="{filter_name}">{filter_name}</li>
'''

def create_html():
    indir = os.path.dirname(os.path.realpath(__file__))

    suggestions_html = ''
    script = ''
    uniq_languages = set()
    uniq_subjects = set()
    with open(os.path.join(indir, 'suggestions.json'), 'rb') as indata:
        jsondata = json.loads(indata.read())

        suggestions_html = '<div class="row">\n\n'
        suggestions_html = '    <div id="suggestions-list" class="col-md-8 col-md-pull-4">\n'

        for category in jsondata:
            cat_name, cat_desc, cat_suggestions = category

            suggestions_html += CATEGORY_HTML.format(
                                    cat_name=cat_name,
                                    cat_desc=cat_desc)


            for suggestion in cat_suggestions:
                name, desc, url, levels, languages, subjects = suggestion
                uniq_languages.update(languages.split())
                uniq_subjects.update(subjects.split())
                classes = ' '.join([levels, languages, subjects])

                suggestions_html += SUGGESTION_HTML.format(
                                        classes=classes,
                                        name=name,
                                        url=url,
                                        desc=desc,
                                        levels=levels,
                                        languages=languages,
                                        subjects=subjects)

            suggestions_html += '                    </ul>\n'
            suggestions_html += '                </div>\n'
            suggestions_html += '            </div>\n\n'

        suggestions_html += '        </div>\n'

    filters_html = '    <div id="filters-list" class="col-md-4 col-md-push-8">\n'
    script += '        var filters = {\n'
    for filter_heading, filter_list in [
            ('Difficulty Level', ['Beginner', 'Intermediate', 'Advanced']),
            ('Subject', sorted(list(uniq_subjects))),
            ('Programming Language', sorted(list(uniq_languages)))]:
        filter_id = filter_heading.replace(' ', '')
        filters_html += FILTER_HEADER_HTML.format(
                            filter_heading=filter_heading,
                            filter_id=filter_id)

        script += '            "{filter_id}": {filter_list},\n'.format(
                    filter_id=filter_id,
                    filter_list=[str(x) for x in filter_list])

        for filter_name in filter_list:
            filters_html += FILTER_ITEM_HTML.format(filter_name=filter_name)

        filters_html += '                </ul>\n'
        filters_html += '            </div>\n\n'
        filters_html += '        </div>\n\n'

    filters_html += '        </div>\n\n'
    filters_html += '    </div>\n\n'

    script += '        };\n\n'

    style = ''
    with open(os.path.join(indir, 'suggestions.css'), 'rb') as instyle:
        style = instyle.read()

    with open(os.path.join(indir, 'suggestions.js'), 'rb') as inscript:
        script += inscript.read()

    html = ''
    with open(os.path.join(indir, 'template.html'), 'rb') as inhtml:
        html = inhtml.read().format(suggestions=suggestions_html,
                                    filters=filters_html,
                                    style=style,
                                    script=script)

    return html

def create_page(output_dir):

    html = create_html()

    with open(os.path.join(output_dir, 'index.html'), 'wb') as outfile:
        outfile.write(html)

if __name__ == '__main__':
    output_dir = sys.argv[1]

    create_page(output_dir)
