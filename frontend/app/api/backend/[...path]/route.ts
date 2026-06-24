import { NextRequest, NextResponse } from "next/server";

const publicApiBase = process.env.NEXT_PUBLIC_API_BASE_URL || process.env.NEXT_PUBLIC_API_URL || "";
const BACKEND_API_BASE =
  process.env.BACKEND_API_BASE_URL ||
  (publicApiBase.startsWith("http://") || publicApiBase.startsWith("https://") ? publicApiBase : "") ||
  "http://localhost:8000/api/v1";

const HOP_BY_HOP_HEADERS = new Set([
  "connection",
  "content-length",
  "expect",
  "keep-alive",
  "proxy-authenticate",
  "proxy-authorization",
  "te",
  "trailer",
  "transfer-encoding",
  "upgrade"
]);

type RouteContext = {
  params: {
    path?: string[];
  };
};

async function proxyRequest(request: NextRequest, context: RouteContext) {
  const path = context.params.path?.join("/") || "";
  const incomingUrl = new URL(request.url);
  const target = new URL(`${BACKEND_API_BASE.replace(/\/$/, "")}/${path}`);
  target.search = incomingUrl.search;

  const headers = new Headers(request.headers);
  for (const header of HOP_BY_HOP_HEADERS) {
    headers.delete(header);
  }
  headers.delete("host");

  const response = await fetch(target, {
    method: request.method,
    headers,
    body: request.method === "GET" || request.method === "HEAD" ? undefined : await request.text(),
    cache: "no-store"
  });

  const responseHeaders = new Headers(response.headers);
  for (const header of HOP_BY_HOP_HEADERS) {
    responseHeaders.delete(header);
  }

  return new NextResponse(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: responseHeaders
  });
}

export async function GET(request: NextRequest, context: RouteContext) {
  return proxyRequest(request, context);
}

export async function POST(request: NextRequest, context: RouteContext) {
  return proxyRequest(request, context);
}
