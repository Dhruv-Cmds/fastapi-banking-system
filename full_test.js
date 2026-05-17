import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 5,
  duration: '30s',
};

const BASE_URL = 'https://vaultx.dhruvsystems.tech';

function randomUser() {

  const id = `${__VU}_${__ITER}_${Math.floor(Math.random() * 100000)}`;

  return {
    username: `user_${id}`,
    password: 'password123',
    name: `Test User ${id}`,
  };
}

function randomAccountNumber() {
  return Math.floor(Math.random() * 1000000000);
}

export default function () {

  // -----------------------------------
  // HEALTH CHECK
  // -----------------------------------
  const healthRes = http.get(`${BASE_URL}/health`);

  check(healthRes, {
    'health works': (r) => r.status === 200,
  });

  sleep(1);

  // -----------------------------------
  // USER SETUP
  // -----------------------------------
  const user = randomUser();

  const jsonHeaders = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  // -----------------------------------
  // SIGNUP
  // -----------------------------------
  const signupPayload = JSON.stringify({
    username: user.username,
    password: user.password,
    name: user.name,
  });

  const signupRes = http.post(
    `${BASE_URL}/api/signup`,
    signupPayload,
    jsonHeaders
  );

  check(signupRes, {
    'signup success': (r) =>
      r.status === 200 || r.status === 201,
  });

  if (signupRes.status !== 200 && signupRes.status !== 201) {
    console.log(`Signup failed: ${signupRes.body}`);
    return;
  }

  sleep(1);

  // -----------------------------------
  // LOGIN
  // -----------------------------------
  const loginPayload = JSON.stringify({
    username: user.username,
    password: user.password,
  });

  const loginRes = http.post(
    `${BASE_URL}/api/login`,
    loginPayload,
    jsonHeaders
  );

  check(loginRes, {
    'login success': (r) => r.status === 200,
  });

  if (loginRes.status !== 200) {
    console.log(`Login failed: ${loginRes.body}`);
    return;
  }

  let token;

  try {
    token = loginRes.json('access_token');
  } catch (err) {
    console.log(`Token parse failed: ${loginRes.body}`);
    return;
  }

  const authHeaders = {
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  };

  sleep(1);

  // -----------------------------------
  // CREATE ACCOUNT
  // -----------------------------------
  const accountPayload = JSON.stringify({
    acc_no: randomAccountNumber(),
  });

  const createAccountRes = http.post(
    `${BASE_URL}/api/accounts`,
    accountPayload,
    authHeaders
  );

  check(createAccountRes, {
    'account created': (r) => r.status === 200,
  });

  if (createAccountRes.status !== 200) {
    console.log(`Create account failed: ${createAccountRes.body}`);
    return;
  }

  let accountData;

  try {
    accountData = createAccountRes.json();
  } catch (err) {
    console.log(`Account JSON parse failed: ${createAccountRes.body}`);
    return;
  }

  const accountId = accountData.id;

  sleep(1);

  // -----------------------------------
  // GET ACCOUNTS
  // -----------------------------------
  const accountsRes = http.get(
    `${BASE_URL}/api/accounts`,
    authHeaders
  );

  check(accountsRes, {
    'accounts fetched': (r) => r.status === 200,
  });

  sleep(1);

  // -----------------------------------
  // DEPOSIT
  // -----------------------------------
  const depositPayload = JSON.stringify({
    amount: 1000,
  });

  const depositRes = http.post(
    `${BASE_URL}/api/accounts/${accountId}/deposit`,
    depositPayload,
    authHeaders
  );

  check(depositRes, {
    'deposit success': (r) => r.status === 200,
  });

  sleep(1);

  // -----------------------------------
  // WITHDRAW
  // -----------------------------------
  const withdrawPayload = JSON.stringify({
    amount: 100,
  });

  const withdrawRes = http.post(
    `${BASE_URL}/api/accounts/${accountId}/withdraw`,
    withdrawPayload,
    authHeaders
  );

  check(withdrawRes, {
    'withdraw success': (r) => r.status === 200,
  });

  sleep(1);

  // -----------------------------------
  // TRANSACTIONS
  // -----------------------------------
  const txRes = http.get(
    `${BASE_URL}/api/transactions/${accountId}`,
    authHeaders
  );

  check(txRes, {
    'transactions fetched': (r) => r.status === 200,
  });

  sleep(1);

  // -----------------------------------
  // UPDATE PROFILE
  // -----------------------------------
  const updatePayload = JSON.stringify({
    name: `Updated_${user.name}`,
  });

  const updateRes = http.put(
    `${BASE_URL}/api/me`,
    updatePayload,
    authHeaders
  );

  check(updateRes, {
    'profile updated': (r) => r.status === 200,
  });

  sleep(1);

  // -----------------------------------
  // WITHDRAW REMAINING BALANCE
  // -----------------------------------
  const withdrawAllPayload = JSON.stringify({
    amount: 900,
  });

  http.post(
    `${BASE_URL}/api/accounts/${accountId}/withdraw`,
    withdrawAllPayload,
    authHeaders
  );

  sleep(1);

  // -----------------------------------
  // DELETE ACCOUNT
  // -----------------------------------
  const deleteRes = http.del(
    `${BASE_URL}/api/accounts/${accountId}`,
    null,
    authHeaders
  );

  check(deleteRes, {
    'account deleted': (r) => r.status === 200,
  });

  sleep(1);
}