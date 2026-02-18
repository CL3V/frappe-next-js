/**
 * Frappe API call utility for Next.js
 * Uses frappe-js-sdk under the hood
 */

import { FrappeApp } from "frappe-js-sdk";

const getSiteUrl = () => {
  if (typeof window !== "undefined") {
    return window.location.origin;
  }
  return process.env.NEXT_PUBLIC_FRAPPE_URL || "http://localhost:8000";
};

let frappeApp = null;

export const getFrappeApp = () => {
  if (!frappeApp) {
    frappeApp = new FrappeApp(getSiteUrl());
  }
  return frappeApp;
};

/**
 * Make a Frappe API call
 * @param {string} method - The whitelisted method to call
 * @param {object} params - Parameters to pass to the method
 * @returns {Promise} - The API response
 */
export const call = async (method, params = {}) => {
  const app = getFrappeApp();
  return app.call.post(method, params);
};

/**
 * Get a document from Frappe
 * @param {string} doctype - The doctype
 * @param {string} name - The document name
 * @returns {Promise} - The document
 */
export const getDoc = async (doctype, name) => {
  const app = getFrappeApp();
  return app.db.getDoc(doctype, name);
};

/**
 * Get a list of documents
 * @param {string} doctype - The doctype
 * @param {object} options - Query options (fields, filters, limit, etc.)
 * @returns {Promise} - List of documents
 */
export const getList = async (doctype, options = {}) => {
  const app = getFrappeApp();
  return app.db.getDocList(doctype, options);
};

/**
 * Create a new document
 * @param {string} doctype - The doctype
 * @param {object} doc - The document data
 * @returns {Promise} - The created document
 */
export const createDoc = async (doctype, doc) => {
  const app = getFrappeApp();
  return app.db.createDoc(doctype, doc);
};

/**
 * Update a document
 * @param {string} doctype - The doctype
 * @param {string} name - The document name
 * @param {object} doc - The fields to update
 * @returns {Promise} - The updated document
 */
export const updateDoc = async (doctype, name, doc) => {
  const app = getFrappeApp();
  return app.db.updateDoc(doctype, name, doc);
};

/**
 * Delete a document
 * @param {string} doctype - The doctype
 * @param {string} name - The document name
 * @returns {Promise} - Deletion result
 */
export const deleteDoc = async (doctype, name) => {
  const app = getFrappeApp();
  return app.db.deleteDoc(doctype, name);
};
