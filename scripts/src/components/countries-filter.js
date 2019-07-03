import $ from 'jquery'
import { chain, pick, omit, filter, defaults } from 'lodash'

import TmplListGroupItem from '../templates/list-group-item'
import { setContent, slugify, createDatasetFilters, collapseListGroup } from '../util'

export default class {
    constructor(opts) {
        const countries = this._countriesWithCount(opts.datasets, opts.params)
        const countriesMarkup = countries.map(TmplListGroupItem)
        setContent(opts.el, countriesMarkup)
        collapseListGroup(opts.el)
    }

    _countriesWithCount(datasets, params) {
        return chain(datasets)
            .groupBy('country')
            .map(function(datasetsInCountry, country) {
                const filters = createDatasetFilters(pick(params, ['country']))
                const filteredDatasets = filter(datasetsInCountry, filters)
                const countrySlug = slugify(country)
                const selected = params.country && params.country === countrySlug
                const itemParams = selected ? omit(params, 'country') : defaults({ country: countrySlug }, params)
                return {
                    title: country,
                    url: '?' + $.param(itemParams),
                    count: filteredDatasets.length,
                    unfilteredCount: datasetsInCountry.length,
                    selected: selected
                }
            })
            .orderBy('unfilteredCount', 'desc')
            .value()
    }
}