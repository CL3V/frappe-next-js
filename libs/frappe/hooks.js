/**
 * React hooks for Frappe integration
 * These hooks provide a more React-idiomatic way to interact with Frappe
 */

import { useState, useEffect, useCallback } from "react";
import { call, getDoc, getList, createDoc, updateDoc, deleteDoc } from "./call";
import { isLoggedIn, getCurrentUser, login, logout } from "./auth";

/**
 * Hook for making Frappe API calls
 * @param {string} method - The method to call
 * @param {object} params - Parameters for the method
 * @param {boolean} immediate - Whether to call immediately on mount
 */
export const useFrappeCall = (method, params = {}, immediate = false) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = useCallback(
    async (overrideParams = {}) => {
      setLoading(true);
      setError(null);
      try {
        const result = await call(method, { ...params, ...overrideParams });
        setData(result);
        return result;
      } catch (err) {
        setError(err);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [method, JSON.stringify(params)],
  );

  useEffect(() => {
    if (immediate) {
      execute();
    }
  }, [immediate, execute]);

  return { data, loading, error, execute };
};

/**
 * Hook for fetching a single document
 * @param {string} doctype - The doctype
 * @param {string} name - The document name
 */
export const useFrappeDoc = (doctype, name) => {
  const [doc, setDoc] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const refetch = useCallback(async () => {
    if (!doctype || !name) return;
    setLoading(true);
    setError(null);
    try {
      const result = await getDoc(doctype, name);
      setDoc(result);
      return result;
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [doctype, name]);

  useEffect(() => {
    refetch();
  }, [refetch]);

  return { doc, loading, error, refetch };
};

/**
 * Hook for fetching a list of documents
 * @param {string} doctype - The doctype
 * @param {object} options - Query options
 */
export const useFrappeList = (doctype, options = {}) => {
  const [list, setList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const refetch = useCallback(
    async (overrideOptions = {}) => {
      if (!doctype) return;
      setLoading(true);
      setError(null);
      try {
        const result = await getList(doctype, {
          ...options,
          ...overrideOptions,
        });
        setList(result);
        return result;
      } catch (err) {
        setError(err);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [doctype, JSON.stringify(options)],
  );

  useEffect(() => {
    refetch();
  }, [refetch]);

  return { list, loading, error, refetch };
};

/**
 * Hook for authentication state
 */
export const useFrappeAuth = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const checkAuth = useCallback(async () => {
    setLoading(true);
    try {
      const loggedIn = await isLoggedIn();
      if (loggedIn) {
        const currentUser = await getCurrentUser();
        setUser(currentUser);
      } else {
        setUser(null);
      }
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  const handleLogin = async (username, password) => {
    const result = await login(username, password);
    await checkAuth();
    return result;
  };

  const handleLogout = async () => {
    const result = await logout();
    setUser(null);
    return result;
  };

  return {
    user,
    loading,
    isLoggedIn: !!user && user !== "Guest",
    login: handleLogin,
    logout: handleLogout,
    refetch: checkAuth,
  };
};

/**
 * Hook for CRUD operations on a doctype
 * @param {string} doctype - The doctype
 */
export const useFrappeCRUD = (doctype) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const create = useCallback(
    async (doc) => {
      setLoading(true);
      setError(null);
      try {
        const result = await createDoc(doctype, doc);
        return result;
      } catch (err) {
        setError(err);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [doctype],
  );

  const update = useCallback(
    async (name, doc) => {
      setLoading(true);
      setError(null);
      try {
        const result = await updateDoc(doctype, name, doc);
        return result;
      } catch (err) {
        setError(err);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [doctype],
  );

  const remove = useCallback(
    async (name) => {
      setLoading(true);
      setError(null);
      try {
        const result = await deleteDoc(doctype, name);
        return result;
      } catch (err) {
        setError(err);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [doctype],
  );

  return { create, update, remove, loading, error };
};
