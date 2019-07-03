# Adding extra search filters to the Datasets page

## What is this

This is hasty doc on how to add more search filters to the datasets page.  By default, JKAN exposes single value `Organizations` and a multi-value `Categories` search filters.  Since PacELF originally had a bunch of search filters, we need to replicate them as possible in this Jekyll static site.

## IF TL;DR

Feel free to see commit # and figure it out.

Otherwise...

## Read background on architecture

JKAN is an existing open source product with some documentation.

You should read the existing project's [wiki](https://github.com/timwis/jkan/wiki) in order to gain familiarity.

## Expose value you wish to filter on in `datasets.json`

For example if you wish to be able to filter on `access` key:

Append

```json
{% if dataset.access != "" %},
    "access": {{ dataset.access | jsonify }}
{% endif %}
```

to the end of `datasets.json` so Jekyll extracts it from each markdown file in `_datasets`
and puts it into a `datasets.json` which contains an object of key-value pairs for each file.

## Duplicate an existing filter and replace with new filter value

For example, duplicate `decades-filter.js` from `scripts/src/`

Then replace `decade` (the singular form) with `access` and `decades` (the plural form) with `accesses`

Resulting in:

```javascript
import $ from 'jquery'
import { chain, pick, omit, filter, defaults } from 'lodash'

import TmplListGroupItem from '../templates/list-group-item'
import { setContent, slugify, createDatasetFilters, collapseListGroup } from '../util'

export default class {
    constructor(opts) {
        const accesses = this._accessesWithCount(opts.datasets, opts.params)
        const accessesMarkup = accesses.map(TmplListGroupItem)
        setContent(opts.el, accessesMarkup)
        collapseListGroup(opts.el)
    }

    _accessesWithCount(datasets, params) {
        return chain(datasets)
            .groupBy('access')
            .map(function(datasetsInAccess, access) {
                const filters = createDatasetFilters(pick(params, ['access']))
                const filteredDatasets = filter(datasetsInAccess, filters)
                const accessSlug = slugify(access)
                const selected = params.access && params.access === accessSlug
                const itemParams = selected ? omit(params, 'access') : defaults({ access: accessSlug }, params)
                return {
                    title: access,
                    url: '?' + $.param(itemParams),
                    count: filteredDatasets.length,
                    unfilteredCount: datasetsInAccess.length,
                    selected: selected
                }
            })
            .orderBy('unfilteredCount', 'desc')
            .value()
    }
}
```

## Register the new filter component with the rest of the Javascript

* Add `<filter-name>` to `datasets-list.js`

```javascript
    const paramFilters = pick(opts.params, ['organization', 'category'])
    const attributeFilters = pick(opts.el.data(), ['organization', 'category'])
```

becomes:

```javascript
    const paramFilters = pick(opts.params, ['organization', 'category', 'access'])
    const attributeFilters = pick(opts.el.data(), ['organization', 'category', 'access'])
```

* Add new component `access-filter` to `index.js`

```javascript
...
import AccessesFilter from './components/accesses-filter'
...
```

```javascript
...
{tag: 'accesses-filter', class: AccessesFilter, usesDatasets: true}
...
```

* Update `util.js` to include new filter condition

```javascript
...
    if (filters.access) {
      conditions.push(dataset.access && slugify(dataset.access).indexOf(filters.access) !== -1)
    }
...
```

## Recompile the Javascript

Install dependencies and build tools as per JKAN [docs](https://github.com/timwis/jkan/wiki/Architecture#development-1)

Then rebuild `bundle.js`

```shell
npm run build
```

## Add the new element to the `datasets.html` page

```html
...
<h3>Decades</h3>
      <div class="list-group" data-component="accesses-filter" data-show="5">
      </div>
...
```

## Debugging

If your element doesn't appear or isn't populate, double check your singular and plural element names.

More than once this was the missing error while developing this.

## Questions

You can check for existing questions on JKAN's issue tracker

e.g. my [issue](https://github.com/timwis/jkan/issues/155)
