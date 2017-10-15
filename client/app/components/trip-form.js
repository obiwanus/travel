import Ember from 'ember';

export default Ember.Component.extend({

  trip: {},

  minStartDate: Ember.computed(function() {
    return new Date();
  }),

  minEndDate: Ember.computed(function () {
    this.get('minStartDate');
  }),

  actions: {

    setStartDate(date) {
      this.set('minEndDate', date);
      this.set('trip.start_date', date);
    },

    setEndDate(date) {
      this.set('trip.end_date', date);
    },

  },

});
