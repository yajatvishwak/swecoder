import { json } from "@sveltejs/kit";

/** @type {import('./$types').RequestHandler} */
export async function POST({ request, cookies, url, fetch }) {
  try {
    const { username, password } = await request.json();
    if (!username || !password) {
      return json({ ok: false, error: "Missing credentials" }, { status: 400 });
    }

    const backendResponse = await fetch(
      "http://localhost:8000/api/v1/auth/login",
      {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ username, password }),
      }
    );

    if (!backendResponse.ok) {
      return json({ ok: false, error: "Invalid credentials" }, { status: 401 });
    }

    const data = await backendResponse.json();
    const token = data?.access_token;
    if (!token) {
      return json(
        { ok: false, error: "Malformed backend response" },
        { status: 502 }
      );
    }

    const secure = url.protocol === "https:";
    cookies.set("jwt", token, {
      path: "/",
      httpOnly: true,
      sameSite: "lax",
      secure,
      // Set a reasonable session length; adjust as needed
      maxAge: 60 * 60 * 24 * 7,
    });

    return json({ ok: true });
  } catch (_e) {
    return json({ ok: false, error: "Login failed" }, { status: 500 });
  }
}
