function filterSuggestions(elem) {
    
}

var filters = document.getElementsByClass('filter');

for (var index = 0; index < filters.length; ++index) {
    var filter = filters[index];

    filter.addEventListener('click', function (event) {
        filterSuggestions(event.target);
    });
}
