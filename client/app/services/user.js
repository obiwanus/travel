import Ember from 'ember';


export default Ember.Service.extend({
  session: Ember.inject.service(),
  csrf: Ember.inject.service(),

  load() {
    return new Ember.RSVP.Promise((resolve) => {
      let data = this.get('session.data.authenticated');

      if (!Ember.isEmpty(data)) {
        this.set('user', data);

        // Refresh token every time we load user
        this.get('csrf').refreshToken();

        resolve(data);
      } else {
        this.logout();  // don't resolve
      }
    });
  },

  name: Ember.computed('user', function () {
    const fullName = this.get('user.first_name') + ' ' + this.get('user.last_name');
    if (fullName.trim() == '') {
      return this.get('user.email');
    }
    return fullName;
  }),

  id: Ember.computed('user', function () {
    return this.get('user.id');
  }),

  role: Ember.computed('user', function () {
    return this.get('user.role');
  }),

  isAuthenticated: Ember.computed('user', function () {
    return this.get('session.session.isAuthenticated');
  }),

  isAdmin: Ember.computed('user', function () {
    return (this.get('user.role').toLowerCase() == 'administrator');
  }),

  isUserManager: Ember.computed('user', function () {
    const role = this.get('user.role').toLowerCase();
    return (role == 'administrator') || (role == 'user manager');
  }),

  logout(soft) {
    let unload = () => {
      this.set('user', null);
      if (soft !== true) {
        // Hard reload so the user gets the latest backend version
        window.location.reload(true);
      }
    };

    if (this.get('isAuthenticated')) {
      return this.get('session').invalidate().then(unload);
    } else {
      // Returning an empty promise anyway, since the caller may want it
      return new Ember.RSVP.Promise((resolve) => {
        resolve();
      }).then(unload);
    }
  },

});
