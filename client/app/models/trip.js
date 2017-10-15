import DS from 'ember-data';

export default DS.Model.extend({
  destination: DS.attr('string'),
  start_date: DS.attr('naivedate'),
  end_date: DS.attr('naivedate'),
  comment: DS.attr('string'),
  user: DS.belongsTo('user'),
});
