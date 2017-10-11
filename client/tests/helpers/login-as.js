import Ember from 'ember';

export default Ember.Test.registerAsyncHelper(
  'loginAs', function(app, role, password) {
    const emails = {
      'normal user': 'normal@test.com',
      'user manager': 'user-manager@test.com',
      'admin': 'admin@test.com',
    };
    if (password === undefined) {
      password = 'pqlapqlapqla';
    }
    visit('/login');
    fillIn('input[type=email]', emails[role]);
    fillIn('input[type=password]', password);
    click('button[type=submit]');
  }
);
