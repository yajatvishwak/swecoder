import { json } from "@sveltejs/kit";

/** @type {import('./$types').RequestHandler} */
export async function POST({ request, cookies, fetch }) {
  try {
    const jwt = cookies.get("jwt");
    if (!jwt) {
      return json({ error: "Unauthorized" }, { status: 401 });
    }

    const body = await request.json();

    const backendResponse = await fetch(
      "http://localhost:8000/api/v1/store-submission",
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${jwt}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      }
    );

    if (!backendResponse.ok) {
      const errorData = await backendResponse.json().catch(() => ({}));
      return json(
        { error: errorData.detail || "Failed to store submission" },
        { status: backendResponse.status }
      );
    }

    const data = await backendResponse.json();
    return json(data);
  } catch (error) {
    return json({ error: "Failed to store submission" }, { status: 500 });
  }
}
