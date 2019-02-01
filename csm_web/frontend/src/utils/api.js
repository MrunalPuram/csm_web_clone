import Cookies from "js-cookie";

export function post(endpoint, data) {
  const relative_endpoint_pattern = RegExp("^([A-z0-9]+/)+$");
  if (!relative_endpoint_pattern.test(endpoint)) {
    throw new Error("post should only be used with relative endpoints");
  }

  return fetch(endpoint, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "X-CSRFToken": Cookies.get("csrftoken"),
      Accept: "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });
}
