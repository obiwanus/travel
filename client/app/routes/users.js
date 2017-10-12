import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin, {
  messages: Ember.inject.service(),

  model() {
    return this.get('store').findAll('user');
  },

  actions: {
    delete(user) {
      if (!user) return;
      const messages = this.get('messages');
      const user_name = user.get('first_name') + ' ' + user.get('last_name');
      if (window.confirm(`Delete user ${user_name}?`)) {
        user.destroyRecord().then(() => {
          messages.success(this, `User ${user_name} has been deleted`);
        }).catch((response) => {
          if (!response.errors) {
            messages.error(this, "Couldn't delete user due to internal error");
          } else {
            response.errors.forEach((error) => {
              messages.error(this, error);
            });
          }
        });
      }
    },
  },

});
