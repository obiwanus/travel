import Ember from 'ember';

export default Ember.Route.extend({

  ajax: Ember.inject.service(),
  messages: Ember.inject.service(),

  afterModel(model) {
    const messages = this.get('messages'),
          url = `/password/set/${model.b64Uid}/${model.token}/`;

    return this.get('ajax').GET(url).catch((xhr) => {
      const response = xhr.responseJSON;
      if (response && response.error) {
        messages.error(this, response.error);
      }
      this.transitionTo('password-request');
    });
  },

});
