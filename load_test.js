export let options = {
  stages: [
    { duration: "10s", target: 200 },
    { duration: "10s", target: 500 },
    { duration: "10s", target: 1000 },
  ],
};

import http from 'k6/http';
import { check, sleep } from 'k6';

export function setup() {
    let res = http.post('http://localhost:8000/api/login', JSON.stringify({
        username: 'testuser',
        password: 'password123'
    }), {
        headers: { 'Content-Type': 'application/json' }
    });

    console.log("LOGIN STATUS:", res.status);
    console.log("LOGIN BODY:", res.body);

    if (res.status !== 200) {
        throw new Error("Login failed in setup()");
    }

    return { token: res.json('access_token') };
}

export default function (data) {
    let headers = {
        Authorization: `Bearer ${data.token}`,
        'Content-Type': 'application/json'
    };

    let res = http.get('http://localhost:8000/api/accounts', { headers });

    check(res, {
        'status is 200 or 429': (r) => r.status === 200 || r.status === 429,
    });

    sleep(1);
}