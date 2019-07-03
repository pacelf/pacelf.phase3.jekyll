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