import { json } from "@sveltejs/kit";

/** @type {import('./$types').RequestHandler} */
export async function POST({ request, cookies, url, fetch }) {
  try {
    const { username, password, name } = await request.json();
    console.log(username, password, name);
    console.log("signup");
    if (!username || !password) {
      return json({ ok: false, error: "Missing fields" }, { status: 400 });
    }

    const backendResponse = await fetch(
      "http://localhost:8000/api/v1/auth/signup",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password, name }),
      }
    ).catch((err) => {
      console.log(err);
      return json({ ok: false, error: "Signup failed" }, { status: 500 });
    });

    if (!backendResponse.ok) {
      const err = await backendResponse.json().catch(() => ({}));
      return json(
        { ok: false, error: err?.detail || "Signup failed" },
        { status: backendResponse.status }
      );
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
      maxAge: 60 * 60 * 24 * 7,
    });

    return json({ ok: true });
  } catch (_e) {
    return json({ ok: false, error: "Signup failed" }, { status: 500 });
  }
}
