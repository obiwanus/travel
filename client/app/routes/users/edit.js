import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin, {

  user: Ember.inject.service(),
  messages: Ember.inject.service(),

  availableRoles: Ember.computed('user.isAdmin', function () {
    let roles = ['Normal user', 'User manager'];
    if (this.get('user.isAdmin')) {
      roles.push('Administrator');
    }
    return roles;
  }),

  model(user) {
    return this.get('store').findRecord('user', user.id);
  },

  afterModel(user) {
    const availableRoles = this.get('availableRoles');
    if (availableRoles.indexOf(user.get('role')) === -1) {
      this.get('messages').error(this, 'Insufficient permissions to edit user');
      this.transitionTo('users');
    }
  },

  setupController(controller, user) {
    controller.set('user', user);
    controller.set('availableRoles', this.get('availableRoles'));
  },

});
