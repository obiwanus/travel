import Ember from 'ember';

export default Ember.Mixin.create({
  messages: Ember.inject.service(),
  ajax: Ember.inject.service(),

  formErrors: {},
  formFields: [],
  inProgress: false,

  displayMessages(messages, type) {
    const flash = this.get('messages');
    if (Array.isArray(messages)) {
      messages.forEach((message) => {
        flash.send(this, type, message);
      });
    } else if (messages) {
      // A single message
      flash.send(this, type, messages);
    }
  },

  submitForm(url, data, type) {
    if (type === undefined) {
      type = 'POST';
    }

    return new Ember.RSVP.Promise((resolve, reject) => {
      this.set('inProgress', true);
      this.get('ajax').sendData(url, data, type).then((response) => {
        this.displayMessages(response.success, 'success');
        resolve(response);
      }).catch((xhr) => {
        const response = xhr.responseJSON;
        if (!response || !response.errors) {
          // TODO: if CSRF is missing, need to refresh the page
          if (xhr.status && xhr.status > 299) {
            this.displayMessages("An error has occurred while contacting the server", 'error');
          }
        } else {
          this.set('formErrors', response.errors);
          this.displayMessages(response.errors['__all__'] || [], 'error');
        }
        reject(xhr.status);
      }).finally(() => {
        this.set('inProgress', false);
      });
    });
  },

  clearForm() {
    const formFields = this.get('formFields');
    if (Array.isArray(formFields)) {
      formFields.forEach((field) => {
        this.set(field, '');
      });
    }
    this.set('formErrors', {});
  },

});
