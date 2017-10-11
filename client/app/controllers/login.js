import Ember from 'ember';


export default Ember.Controller.extend({
  session: Ember.inject.service(),
  messages: Ember.inject.service(),

  actions: {
    login() {
      let { email, password } = this.getProperties('email', 'password');
      this.set('inProgress', true);
      this.get('session').authenticate('authenticator:django-session', email, password).then(() => {
        this.set('formErrors');
        this.transitionToRoute('index');
      }).catch((xhr) => {
        const errors = (xhr.responseJSON && xhr.responseJSON.errors) || ["Unable to contact the server"];
        if (Array.isArray(errors)) {
          errors.forEach((error) => {
            this.get('messages').error(this, error);
          });
        } else {
          this.set('formErrors', errors);
        }
      }).finally(() => {
        this.set('inProgress', false);
      });
    },
  },
});
