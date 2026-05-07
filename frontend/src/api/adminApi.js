import API from "./api";


export const getUsers = () =>
  API.get("/admin/users");


export const getAllAccounts = () =>
  API.get("/admin/accounts");