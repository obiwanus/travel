import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin, {

    redirect(model, transition) {
      if (transition.targetName === 'trips.index') {
        this.replaceWith('trips.upcoming');
      }
    },

    model() {
      return this.get('store').findAll('trip');
    },

});
