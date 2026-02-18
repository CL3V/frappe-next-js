/**
 * Authentication utilities for Frappe
 */

import { getFrappeApp } from "./call";

/**
 * Login to Frappe
 * @param {string} username - Username or email
 * @param {string} password - Password
 * @returns {Promise} - Login result
 */
export const login = async (username, password) => {
  const app = getFrappeApp();
  return app.auth.loginWithUsernamePassword({ username, password });
};

/**
 * Logout from Frappe
 * @returns {Promise} - Logout result
 */
export const logout = async () => {
  const app = getFrappeApp();
  return app.auth.logout();
};

/**
 * Get the currently logged in user
 * @returns {Promise} - Current user info
 */
export const getCurrentUser = async () => {
  const app = getFrappeApp();
  return app.auth.getLoggedInUser();
};

/**
 * Check if user is logged in
 * @returns {Promise<boolean>} - True if logged in
 */
export const isLoggedIn = async () => {
  try {
    const user = await getCurrentUser();
    return user && user !== "Guest";
  } catch {
    return false;
  }
};
