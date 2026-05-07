import API from "./api";


export const signupUser = (data) =>
  API.post("/signup", data);


export const loginUser = (data) =>
  API.post("/login", data);


export const updateProfile = (data) =>
  API.put("/profile", data);