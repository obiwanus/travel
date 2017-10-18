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
      let user_id = this.get('user.user.id');  // show only our trips, even if we have other loaded
      return this.get('store').findAll('trip').filter((trip) => true);
    },

});
