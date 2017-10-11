import Ember from 'ember';
import DS from 'ember-data';

export default DS.JSONAPIAdapter.extend({
  csrf: Ember.inject.service(),
  namespace: 'api',
  headers: Ember.computed('csrf.token', function () {
    return {
      "X-CSRFToken": this.get('csrf.token')
    };
  }),
});
