import Ember from 'ember';

export default Ember.Component.extend({

  filteredErrors: Ember.computed('errors', function () {
    const errors = this.get('errors');
    if (!errors) return [];
    return errors[this.get('for')] || [];
  }),

});
