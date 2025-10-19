import { redirect } from "@sveltejs/kit";

// Publicly accessible paths (no auth required)
// Include API route prefix "/auth" so signup/login endpoints are reachable unauthenticated
const publicPaths = ["/login", "/signup", "/auth"];

function isPublicPath(pathname) {
  return publicPaths.some(
    (p) => pathname === p || pathname.startsWith(p + "/")
  );
}

/** @type {import('@sveltejs/kit').Handle} */
export async function handle({ event, resolve }) {
  const url = new URL(event.request.url);
  const pathname = url.pathname;

  const jwt = event.cookies.get("jwt");
  if (jwt) {
    // Always verify token with backend, even on public routes
    try {
      const verify = await event.fetch(
        "http://localhost:8000/api/v1/auth/verify",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ token: jwt }),
        }
      );
      // Backend returns 200 with { valid: boolean }
      const verifyBody = await verify.json().catch(() => ({ valid: false }));
      if (!verify.ok || !verifyBody?.valid) {
        event.cookies.set("jwt", "", {
          path: "/",
          httpOnly: true,
          sameSite: "lax",
          secure: url.protocol === "https:",
          maxAge: 0,
        });
      } else {
        event.locals.jwt = jwt;
      }
    } catch (_e) {
      event.cookies.set("jwt", "", {
        path: "/",
        httpOnly: true,
        sameSite: "lax",
        secure: url.protocol === "https:",
        maxAge: 0,
      });
    }
  }

  // Redirect unauthenticated users away from protected routes
  if (!event.locals.jwt && !isPublicPath(pathname)) {
    throw redirect(302, "/login");
  }

  // Redirect authenticated users away from the login/signup pages (but not API endpoints)
  if (event.locals.jwt && (pathname === "/login" || pathname === "/signup")) {
    throw redirect(302, "/dashboard");
  }

  return resolve(event);
}
