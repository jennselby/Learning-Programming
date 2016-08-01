import sys
import json
import os.path

CATEGORY_HTML = \
'''
        <li class="category-item">
            <div class="category-name">{cat_name}</div>
            <div class="category-desc">{cat_desc}</div>
'''

SUGGESTION_HTML = \
'''
                <li class="suggestion-item {classes}">
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

        suggestions_html = '<ul id="suggestions-list">\n'

        for category in jsondata:
            cat_name, cat_desc, cat_suggestions = category

            suggestions_html += CATEGORY_HTML.format(
                                    cat_name=cat_name,
                                    cat_desc=cat_desc)

            suggestions_html += \
                '            <ul class="category-suggestions-list">\n'

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

            suggestions_html += '            </ul>\n'
            suggestions_html += '        </li>\n\n'

        suggestions_html += '    </ul>\n'

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
