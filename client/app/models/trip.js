import DS from 'ember-data';

export default DS.Model.extend({
  destination: DS.attr('string'),
  start_date: DS.attr('date'),
  end_date: DS.attr('date'),
  comment: DS.attr('string'),
  user: DS.attr('user'),
});
