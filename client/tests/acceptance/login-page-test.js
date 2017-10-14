import { test } from 'qunit';
import moduleForAcceptance from 'client/tests/helpers/module-for-acceptance';

moduleForAcceptance('Acceptance | login page');

test('if not authenticated then redirects to login', function(assert) {
  visit('/');

  andThen(function() {
    assert.equal(currentURL(), '/login');
  });
});

test('Can login as normal user', function(assert) {
  loginAs('normal user');

  andThen(function() {
    assert.equal(currentURL(), '/trips');
  });
});

test('Can login as user manager', function(assert) {
  loginAs('user manager');

  andThen(function() {
    assert.equal(currentURL(), '/trips');
  });
});

test('Can login as admin user', function(assert) {
  loginAs('admin');

  andThen(function() {
    assert.equal(currentURL(), '/trips');
  });
});

test('Cannot login with wrong password', function(assert) {
  loginAs('normal user', 'wrong_password');

  andThen(function() {
    assert.equal(currentURL(), '/login');
    let error = find('p.is-danger:contains("Wrong")');
    assert.ok(error.length >= 1, 'No error displayed');
  });
});
