import type { RequestEvent } from '@sveltejs/kit';

// Session cookie name for authentication
export const sessionCookieName = 'auth-session';

// Generate a random session token
export function generateSessionToken(): string {
	const bytes = crypto.getRandomValues(new Uint8Array(18));
	const token = Array.from(bytes, byte => byte.toString(16).padStart(2, '0')).join('');
	return token;
}

// Authentication interface types
export interface User {
	id: string;
	username: string;
	isAdmin: boolean;
}

export interface Session {
	id: string;
	userId: string;
	expiresAt: Date;
}

export interface SessionValidationResult {
	session: Session | null;
	user: User | null;
}

// Simple in-memory session storage for development
type SessionStore = Record<string, Session>;
const sessions: SessionStore = {};

// Create a new session for a user - no API calls needed anymore
export async function createSession(token: string, user: User): Promise<Session> {
	const expiresAt = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000); // 30 days
	
	try {
		// Create session in memory - no need for API calls
		const session: Session = {
			id: token,
			userId: user.id,
			expiresAt
		};
		
		// Store in memory
		sessions[token] = session;
		console.log(`Created in-memory session for ${user.username}`);
		
		return session;
	} catch (error) {
		console.error('Error creating session:', error);
		throw error;
	}
}

// Mock user database for in-memory sessions
const users: Record<string, User> = {};

// Validate a session token
export async function validateSessionToken(token: string): Promise<SessionValidationResult> {
	if (!token) {
		return { session: null, user: null };
	}
	
	try {
		// Check if token exists in our in-memory sessions
		const session = sessions[token];
		if (!session) {
			return { session: null, user: null };
		}
		
		// Check if session is expired
		if (session.expiresAt < new Date()) {
			delete sessions[token];
			return { session: null, user: null };
		}
		
		// Get user from our internal database or create a mock one
		let user = users[session.userId];
		if (!user) {
			// Create a mock user for testing
			user = {
				id: session.userId,
				username: 'admin-user',
				isAdmin: true
			};
			
			// Store for future use
			users[session.userId] = user;
		}
		
		// Check if session needs renewal
		const renewSession = Date.now() >= session.expiresAt.getTime() - (15 * 24 * 60 * 60 * 1000); // 15 days before expiry
		if (renewSession) {
			const newExpiresAt = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000); // 30 days
			session.expiresAt = newExpiresAt;
			console.log(`Renewed session for ${user.username}`); 
		}
		
		return { session, user };
	} catch (error) {
		console.error('Error validating session:', error);
		return { session: null, user: null };
	}
}

// Invalidate a session (logout)
export async function invalidateSession(token: string): Promise<void> {
	try {
		// Simply remove from our in-memory sessions
		if (sessions[token]) {
			const userId = sessions[token].userId;
			const username = users[userId]?.username || 'unknown';
			
			delete sessions[token];
			console.log(`Invalidated session for ${username}`);
		}
	} catch (error) {
		console.error('Error invalidating session:', error);
	}
}

// Set session cookie
export function setSessionTokenCookie(event: RequestEvent, token: string, expiresAt: Date): void {
	event.cookies.set(sessionCookieName, token, {
		expires: expiresAt,
		path: '/',
		httpOnly: true,
		secure: process.env.NODE_ENV === 'production',
		sameSite: 'strict'
	});
}

// Delete session cookie
export function deleteSessionTokenCookie(event: RequestEvent): void {
	event.cookies.delete(sessionCookieName, {
		path: '/'
	});
}
