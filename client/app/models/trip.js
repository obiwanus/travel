import Ember from 'ember';
import DS from 'ember-data';
import moment from 'moment';

let today_start = moment().startOf('day');
let today_end = moment().endOf('day');
let month_end = moment().endOf('day').add(1, 'months');

export default DS.Model.extend({
  destination: DS.attr('string'),
  start_date: DS.attr('naivedate'),
  end_date: DS.attr('naivedate'),
  comment: DS.attr('string'),
  user: DS.belongsTo('user'),

  when: Ember.computed('start_date', function () {
    let start = moment(this.get('start_date'));
    if (!start.isValid() || start < today_start) return null;
    if (start < today_end) return "today";
    return start.fromNow();
  }),

  isPast: Ember.computed('start_date', function () {
    return moment(this.get('start_date')) < today_start;
  }),

  isWithinNextMonth: Ember.computed('start_date', function () {
    let start = moment(this.get('start_date'));
    return today_start <= start && start <= month_end;
  }),

  start: Ember.computed('start_date', function () {
    return moment(this.get('start_date')).format("D MMM gggg");
  }),

  end: Ember.computed('end_date', function () {
    let end = moment(this.get('end_date'));
    if (end.isValid()) {
      return end.format("D MMM gggg");
    } else {
      return '-';
    }
  }),

  _filterText: Ember.computed('destination', 'start_date', 'end_date', 'comment', function () {
    return (
      this.get('destination') +
      moment(this.get('start_date')).format('D MMMM gggg') +
      moment(this.get('end_date')).format('D MMMM gggg') +
      this.get('comment')
    ).toLowerCase();
  }),
});
