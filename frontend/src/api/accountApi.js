import API from "./api";


export const createAccount = (data) =>
  API.post("accounts", data);


export const getAccounts = () =>
  API.get("/accounts");


export const depositMoney = (id, data) =>
  API.post(`/accounts/${id}/deposit`, data);


export const withdrawMoney = (id, data) =>
  API.post(`/accounts/${id}/withdraw`, data);


export const transferMoney = (data) =>
  API.post("/transfer", data);


export const getTransactions = (id, skip = 0, limit = 20) =>
  API.get(`/accounts/${id}/transactions?skip=${skip}&limit=${limit}`);


export const deleteAccount = (id) =>
  API.delete(`/accounts/${id}`);