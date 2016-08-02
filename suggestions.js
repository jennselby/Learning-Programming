        function getCategory(filterItem) {
            var parentElem = filterItem;
            do {
                parentElem = parentElem.parentElement;
            }
            while (parentElem.nodeName !== 'UL');

            return parentElem.id;
        }

        function checkSuggestionVisibility(suggestion) {
            var visible = false;
            filterCategories = Object.keys(filters);
            for (var catIndex = 0;
                 catIndex < filterCategories.length;
                 ++catIndex) {
                visible = false;

                var filterNames = filters[filterCategories[catIndex]];
                for (var nameIndex = 0;
                     nameIndex < filterNames.length;
                     ++nameIndex) {
                    var filterName = filterNames[nameIndex];
                    if (suggestion.classList.contains(filterName)) {
                        visible = true;
                    }
                }

                // If any one category has no items that are in the
                // class list, the item should not be visible. Stop
                // checking.
                if (visible === false) {
                    suggestion.style.display = 'none';
                    break;
                }
            }

            if (visible === true) {
                suggestion.style.display = 'block';
            }
        }

        function refilter() {
            var suggestions = document.getElementsByClassName(
                'suggestion-item');

            for (var suggIndex = 0;
                 suggIndex < suggestions.length;
                 ++suggIndex) {
                var suggestion = suggestions[suggIndex];
                checkSuggestionVisibility(suggestion);
            }
        }

        function toggleFilter(filterItem) {
            if (filterItem.classList.contains('filtering')) {
                // switch to showing

                filterItem.classList.add('showing');
                filterItem.classList.remove('filtering');

                // add this to the list of things that should be displayed
                var category = getCategory(filterItem);
                var filterName = filterItem.id;
                filters[category].push(filterName);

                // change what items are displayed
                refilter();

            } else {
                // switch to filtering
                // showing is the default; if there was a mistake and
                // it has neither class, we can ignore that error

                filterItem.classList.add('filtering');
                filterItem.classList.remove('showing');

                // remove this from the list of things that should
                // be displayed
                var category = getCategory(filterItem);
                var categoryFilters = filters[category];
                var filterName = filterItem.id;
                var filterIndex = categoryFilters.indexOf(filterName);
                while (filterIndex !== -1) {
                    categoryFilters.splice(filterIndex, 1);
                    filterIndex = categoryFilters.indexOf(filterName);
                }

                // change what items are displayed
                refilter();
            }
        }

        var filterItems = document.getElementsByClassName('filter-item');
        for (var index = 0; index < filterItems.length; ++index) {
            filterItems[index].addEventListener('click', function(event) {
                toggleFilter(event.target);
            });
        }
