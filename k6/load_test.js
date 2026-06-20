export let options = {
  stages: [
    { duration: "20s", target: 100 },
    { duration: "30s", target: 200 },
    { duration: "40s", target: 300 },
  ],
};

import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = 'http://localhost:8000';

const headers = {
  'Content-Type': 'application/json',
};

export default function () {
    const username = `user_${__VU}_${__ITER}`;

    // signup
    http.post(`${BASE_URL}/api/signup`, JSON.stringify({
        username,
        name: "Test",
        password: "password123"
    }), { headers });

    // login
    let loginRes = http.post(`${BASE_URL}/api/login`, JSON.stringify({
        username,
        password: "password123"
    }), { headers });

    let token = loginRes.json('access_token');

    // request with token
    let res = http.get(`${BASE_URL}/api/accounts`, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    check(res, {
        'status ok': (r) => r.status === 200 || r.status === 429,
    });

    sleep(1);
}