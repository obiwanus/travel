import Ember from 'ember';

export default Ember.Component.extend({

  filter: '',

  filterFunction: Ember.computed('trips', 'dateFilter', 'filter', function () {
    let dateFilter = (trip) => !trip.get('isPast');
    if (this.get('dateFilter') === 'past') {
      dateFilter = (trip) => trip.get('isPast');
    }
    let filterFunc = dateFilter;
    let filterString = this.get('filter').toLowerCase();
    if (filterString) {
      filterFunc = (trip) => {
        return dateFilter(trip) && (trip.get('_filterText').indexOf(filterString) !== -1);
      };
    }
    return filterFunc;
  }),

  filteredTrips: Ember.computed('filterFunction', function () {
    return this.get('trips').filter(this.get('filterFunction'))
  }),

});
