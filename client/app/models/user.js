import Ember from 'ember';
import DS from 'ember-data';

export default DS.Model.extend({
  email: DS.attr('string'),
  first_name: DS.attr('string'),
  last_name: DS.attr('string'),
  password: DS.attr('string'),
  role: DS.attr('string'),
  is_active: DS.attr('boolean'),

  full_name: Ember.computed('first_name', 'last_name', function () {
    return this.get('first_name') + ' ' + this.get('last_name');
  }),
});
