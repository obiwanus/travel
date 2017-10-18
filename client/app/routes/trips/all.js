import TripRoute from './index';

export default TripRoute.extend({

  model() {
    // Fetch all trips for all users
    return this.get('store').query('trip', {all: true});
  },

});
