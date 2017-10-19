import Ember from 'ember';

export default Ember.Component.extend({

  filter: '',

  filterFunction: Ember.computed('trips', 'dateFilter', 'filter', function () {
    let dateFilter = (trip) => true;  // no filter
    if (this.get('dateFilter') === 'past') {
      dateFilter = (trip) => trip.get('isPast');
    } else if (this.get('dateFilter') === 'next_month') {
      dateFilter = (trip) => trip.get('isWithinNextMonth');
    } else if (this.get('dateFilter') === 'upcoming') {
      dateFilter = (trip) => !trip.get('isPast');
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
    return this.get('trips').filter(this.get('filterFunction')).sort((trip1, trip2) => {
      return trip1.get('start_date') > trip2.get('start_date');
    })
  }),

});
