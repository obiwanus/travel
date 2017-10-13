import Ember from 'ember';

const ERROR_MESSAGES = {
    403: 'Forbidden',
    404: 'Page not found',
    502: 'Unable to contact the server',
    503: 'Unable to contact the server',
};

export default Ember.Route.extend({

  user: Ember.inject.service(),

  setupController(controller, error) {
    // for a data adapter error, assuming there is only a single error
    if (error) {
      const rawError = error.errors && error.errors[0] || error;
      const code = rawError.status || rawError.code;

      if (code == 401) {
        // Session seems to have expired. Logging out
        this.get('user').logout();
        return;
      }
      controller.set('message', ERROR_MESSAGES[parseInt(code)]);

    } else {
      controller.set('message', ERROR_MESSAGES[404]);
    }
    this._super(controller, error);
  }
});
