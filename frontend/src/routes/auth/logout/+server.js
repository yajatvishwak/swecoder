import { json } from "@sveltejs/kit";

/** @type {import('./$types').RequestHandler} */
export async function POST({ cookies, url }) {
  const secure = url.protocol === "https:";
  cookies.set("jwt", "", {
    path: "/",
    httpOnly: true,
    sameSite: "lax",
    secure,
    maxAge: 0,
  });
  return json({ ok: true });
}
