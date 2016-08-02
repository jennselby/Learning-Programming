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

def create_html():
    indir = os.path.dirname(os.path.realpath(__file__))

    suggestions_html = ''
    with open(os.path.join(indir, 'suggestions.json'), 'rb') as indata:
        jsondata = json.loads(indata.read())

        suggestions_html = '<div id="suggestions-list">\n'

        for category in jsondata:
            cat_name, cat_desc, cat_suggestions = category

            suggestions_html += CATEGORY_HTML.format(
                                    cat_name=cat_name,
                                    cat_desc=cat_desc)

            suggestions_html += \
                '                <ul class="category-suggestions-list list-group">\n'

            for suggestion in cat_suggestions:
                name, desc, url, levels, languages, subjects = suggestion
                classes = ' '.join([levels, languages, subjects])

                suggestions_html += SUGGESTION_HTML.format(
                                        classes=classes,
                                        name=name,
                                        url=url,
                                        desc=desc,
                                        levels=levels,
                                        languages=languages,
                                        subjects=subjects)

            suggestions_html += '                </ul>\n'
            suggestions_html += '            </div>\n'
            suggestions_html += '        </div>\n\n'

        suggestions_html += '    </div>\n'

    html = ''
    with open(os.path.join(indir, 'template.html'), 'rb') as inhtml:
        html = inhtml.read().format(suggestions=suggestions_html)

    return html

def create_page(output_dir):

    html = create_html()

    with open(os.path.join(output_dir, 'index.html'), 'wb') as outfile:
        outfile.write(html)

if __name__ == '__main__':
    output_dir = sys.argv[1]

    create_page(output_dir)
