// Penyimpanan sesi sederhana menggunakan Map
// Pada implementasi produksi, gunakan database atau Redis untuk menyimpan sesi

// Singleton session store
let sessions: Map<string, SessionData> = new Map();

export interface SessionData {
  id: string;
  userId: string;
  expiresAt: string;
}

export const SessionStore = {
  // Mendapatkan sesi berdasarkan token
  get: (token: string): SessionData | undefined => {
    return sessions.get(token);
  },

  // Menyimpan sesi baru
  set: (token: string, sessionData: SessionData): void => {
    sessions.set(token, sessionData);
  },

  // Menghapus sesi
  delete: (token: string): boolean => {
    return sessions.delete(token);
  },

  // Membersihkan sesi yang sudah kedaluwarsa
  cleanup: (): void => {
    const now = new Date();
    for (const [token, session] of sessions.entries()) {
      if (new Date(session.expiresAt) < now) {
        sessions.delete(token);
      }
    }
  },

  // Mendapatkan semua sesi (untuk debugging)
  getAll: (): Map<string, SessionData> => {
    return new Map(sessions);
  }
};
