import Ember from 'ember';
import TripRoute from './index';

export default TripRoute.extend({

  messages: Ember.inject.service(),

  model(trip) {
    return this.get('store').findRecord('trip', trip.id);
  },

  setupController(controller, model) {
    this._super(...arguments);
    controller.set('trip', model);
  },

  actions: {
    delete(trip) {
      if (!trip) return;
      const messages = this.get('messages');
      if (window.confirm(`Delete trip?`)) {
        trip.destroyRecord().then(() => {
          messages.success(this, `Trip has been deleted`);
          history.back();
        }).catch((response) => {
          if (!response.errors) {
            messages.error(this, "Couldn't delete trip due to internal error");
          } else {
            response.errors.forEach((error) => {
              let error_msg = error.title || error;
              messages.error(this, error_msg);
            });
          }
        });
      }
    },
  },

});
