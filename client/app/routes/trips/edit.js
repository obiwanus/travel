import TripRoute from './index';

export default TripRoute.extend({

  model(trip) {
    return this.get('store').findRecord('trip', trip.id);
  },

  setupController(controller, model) {
    this._super(...arguments);
    controller.set('trip', model);
  },

});
