export let options = {
  stages: [
    { duration: "10s", target: 200 },
    { duration: "10s", target: 500 },
    { duration: "10s", target: 1000 },
  ],
};

import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = 'http://localhost:8000';

export function setup() {
    // 🔥 ensure user exists
    http.post(`${BASE_URL}/api/signup`, JSON.stringify({
        username: 'testuser',
        name: 'Test User',
        password: 'password123'
    }), {
        headers: { 'Content-Type': 'application/json' }
    });

    // 🔐 login
    let res = http.post(`${BASE_URL}/api/login`, JSON.stringify({
        username: 'testuser',
        password: 'password123'
    }), {
        headers: { 'Content-Type': 'application/json' }
    });

    console.log("LOGIN STATUS:", res.status);

    if (res.status !== 200) {
        console.log("LOGIN BODY:", res.body);
        throw new Error("Login failed in setup()");
    }

    return { token: res.json('access_token') };
}

export default function (data) {
    let headers = {
        Authorization: `Bearer ${data.token}`,
        'Content-Type': 'application/json'
    };

    let res = http.get(`${BASE_URL}/api/accounts`, { headers });

    check(res, {
        'status is 200 or 429': (r) => r.status === 200 || r.status === 429,
    });

    sleep(1);
}