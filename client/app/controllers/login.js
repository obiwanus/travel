import Ember from 'ember';
import FormMixin from 'client/mixins/form';

export default Ember.Controller.extend(FormMixin, {
  session: Ember.inject.service(),

  formFields: ['email', 'password'],

  doSubmit() {
    let { email, password } = this.getProperties('email', 'password');
    return this.get('session').authenticate('authenticator:django-session', email, password);
  },

  actions: {
    login() {
      this.submitForm().then(() => {
        this.clearForm();
        this.transitionToRoute('index');
      });
    },
  },
});
