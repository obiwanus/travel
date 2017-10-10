import Ember from 'ember';

export default Ember.Controller.extend({
  session: Ember.inject.service(),

  actions: {
    login() {
      let { email, password } = this.getProperties('email', 'password');
      this.get('session').authenticate('authenticator:django-session', email, password).catch((reason) => {
        debugger;
      });
    },
  },
});
