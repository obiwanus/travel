import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin, {

    title: "Trips",
    noAddButton: false,

    redirect(model, transition) {
      if (transition.targetName === 'trips.index') {
        this.replaceWith('trips.upcoming');
      }
    },

    model() {
        return this.get('store').findAll('trip');
    },

    setupController() {
      const controller = this.controllerFor('trips');
      controller.set('title', this.get('title'));
      controller.set('noAddButton', this.get('noAddButton'));
    },

});
