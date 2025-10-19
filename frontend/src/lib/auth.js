// Client-side auth helpers call server endpoints which manage an HTTPOnly cookie

/**
 * Get JWT from localStorage
 */
// No token access from client; cookie is HTTPOnly

/**
 * Save JWT to localStorage
 */
// No direct token setting from client

/**
 * Remove JWT from localStorage
 */
// No direct token clearing from client

/**
 * Check if user is authenticated (has token)
 */
// If needed, check via server using /auth/verify or page data

/**
 * Attempt login by calling backend through server route.
 * @param {string} username
 * @param {string} password
 */
export async function login(username, password) {
  const res = await fetch("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  const data = await res.json().catch(() => ({}));
  const ok = res.ok && data?.ok === true;
  return { ok, status: res.status, error: data?.error };
}

export function logout() {
  // fire-and-forget; server clears the cookie
  fetch("/auth/logout", { method: "POST" });
}

/**
 * Attempt signup by calling backend through server route.
 * @param {string} username
 * @param {string} password
 * @param {string | undefined} name
 */
export async function signup(username, password, name) {
  console.log(username, password, name);
  console.log("signup from auth.js");
  const res = await fetch("/auth/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password, name }),
  });
  console.log(await res.json());
  console.log("res from auth.js");
  if (!res.ok) return { ok: false };
  return { ok: true };
}
