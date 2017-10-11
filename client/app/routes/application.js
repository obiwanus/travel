import Ember from 'ember';
import ApplicationRouteMixin from 'ember-simple-auth/mixins/application-route-mixin';

export default Ember.Route.extend(ApplicationRouteMixin, {

  title: 'Travel Planner',
  csrf: Ember.inject.service(),

  beforeModel() {
    this.get('csrf').refreshToken();
  },

  sessionAuthenticated() {
    this._super(...arguments);

    // Reload user after login. This will refresh the csrf token
    this.get('csrf').refreshToken();
  },

});
