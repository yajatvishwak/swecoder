import { json } from "@sveltejs/kit";

/** @type {import('./$types').RequestHandler} */
export async function GET({ cookies, fetch }) {
  try {
    const jwt = cookies.get("jwt");
    if (!jwt) {
      return json({ error: "Unauthorized" }, { status: 401 });
    }

    const backendResponse = await fetch(
      "http://localhost:8000/api/v1/get-activity",
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${jwt}`,
          "Content-Type": "application/json",
        },
      }
    );

    if (!backendResponse.ok) {
      const errorData = await backendResponse.json().catch(() => ({}));
      return json(
        { error: errorData.detail || "Failed to fetch activity data" },
        { status: backendResponse.status }
      );
    }

    const data = await backendResponse.json();
    return json(data);
  } catch (error) {
    return json({ error: "Failed to fetch activity data" }, { status: 500 });
  }
}
