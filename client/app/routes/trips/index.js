import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin, {

  user: Ember.inject.service(),

  redirect(model, transition) {
    if (transition.targetName === 'trips.index') {
      this.replaceWith('trips.upcoming');
    }
  },

  model() {
    // Get trips filtered by user
    let user_id = this.get('user.id');
    return this.get('store').query('trip', {}).then(function (trips) {
      return trips.filter(function (trip) {
        return trip.get('user_id') == user_id;
      });
    });
  },

  actions: {
    back() {
      history.back();
    },
  },

});
