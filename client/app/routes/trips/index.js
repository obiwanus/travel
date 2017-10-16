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
      this._super(...arguments);
      const parent = this.controllerFor('trips');
      parent.set('title', this.get('title'));
      parent.set('noAddButton', this.get('noAddButton'));
    },

});
