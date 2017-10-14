import Ember from 'ember';
import FormMixin from 'client/mixins/form';

export default Ember.Controller.extend(FormMixin, {

  user: Ember.inject.service(),

  formFields: ['password', 'password_confirm'],

  minPasswordLength: 8,

  passwordTooShort: Ember.computed('password', function () {
    if (!this.password) return false;
    return this.password.length < this.minPasswordLength;
  }),

  passwordsDontMatch: Ember.computed('password', 'password_confirm', function () {
    if (!this.password_confirm) return false;
    return this.password !== this.password_confirm;
  }),

  disableSubmit: Ember.computed('password', 'password_confirm', function () {
    if (this.get('inProgress')) return true;
    if (!this.password || !this.password_confirm) return true;
    return this.password.length < this.minPasswordLength ||
           this.password !== this.password_confirm;
  }),

  actions: {
    setPassword() {
      const password = this.get('password'),
            b64Uid = this.get('model.b64Uid'),
            urlToken = this.get('model.token');

      this.submitForm(`/password/set/${b64Uid}/${urlToken}/`, {
        password: password,
      }).then(() => {
        this.get('user').logout(true).then(() => {
          this.transitionToRoute('login');
        });
      }).catch(() => {
        this.clearForm();
      });
    }
  }

});
