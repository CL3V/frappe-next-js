/**
 * Socket.io client for Frappe realtime updates
 */

import { io } from "socket.io-client";

let socket = null;

/**
 * Get the socket instance
 * @returns {Socket} - The socket.io client instance
 */
export const getSocket = () => {
  if (!socket) {
    const socketUrl =
      process.env.NEXT_PUBLIC_FRAPPE_URL || "http://localhost:8000";
    socket = io(socketUrl, {
      withCredentials: true,
      transports: ["websocket", "polling"],
    });
  }
  return socket;
};

/**
 * Subscribe to document updates
 * @param {string} doctype - The doctype to subscribe to
 * @param {string} name - The document name (optional, for specific doc)
 * @param {function} callback - Callback function when update received
 */
export const subscribeDoc = (doctype, name, callback) => {
  const sock = getSocket();
  const event = name ? `doc:${doctype}:${name}` : `doctype:${doctype}`;
  sock.emit("subscribe", event);
  sock.on(event, callback);

  return () => {
    sock.off(event, callback);
    sock.emit("unsubscribe", event);
  };
};

/**
 * Subscribe to a room
 * @param {string} room - The room name
 * @param {function} callback - Callback function
 */
export const subscribeRoom = (room, callback) => {
  const sock = getSocket();
  sock.emit("subscribe", room);
  sock.on(room, callback);

  return () => {
    sock.off(room, callback);
    sock.emit("unsubscribe", room);
  };
};

/**
 * Disconnect the socket
 */
export const disconnect = () => {
  if (socket) {
    socket.disconnect();
    socket = null;
  }
};
