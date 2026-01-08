import { NextRequest, NextResponse } from 'next/server';

export default async function proxy(request: NextRequest) {
  const token = request.cookies.get('auth_token')?.value;
  const { pathname } = request.nextUrl;

  // Allow public routes
  const publicPaths = ['/', '/signin', '/signup'];
  const isPublicPath = publicPaths.some(path => pathname.startsWith(path));

  if (isPublicPath) {
    return NextResponse.next();
  }

  // Check for auth token on protected routes
  if (!token && !isPublicPath) {
    // Redirect to signin if no token
    const url = new URL('/signin', request.url);
    return NextResponse.redirect(url);
  }

  // Check token expiration
  if (token) {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const now = Math.floor(Date.now() / 1000);

      if (payload.exp < now) {
        // Token expired - redirect to signin
        const url = new URL('/signin', request.url);
        const response = NextResponse.redirect(url);
        response.cookies.delete('auth_token');
        return response;
      }
    } catch (error) {
      // Invalid token - redirect to signin
      const url = new URL('/signin', request.url);
      return NextResponse.redirect(url);
    }
  } else {
    // No token - redirect to signin
    const url = new URL('/signin', request.url);
    return NextResponse.redirect(url);
  }

  return NextResponse.next();
}
