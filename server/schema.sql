CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS friend_relationships (
    id INTEGER PRIMARY KEY,
    pair_low INTEGER NOT NULL,
    pair_high INTEGER NOT NULL,
    sender_id INTEGER NOT NULL,
    relationship_status TEXT NOT NULL DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    responded_at DATETIME,
    -- FK integrity
    FOREIGN KEY (pair_low) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (pair_high) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    -- no duplicates for the same pair
    UNIQUE (pair_low, pair_high),
    -- canonical ordering / no self-requests
    CHECK (pair_low < pair_high),
    -- sender must be one of the pair members
    CHECK (sender_id = pair_low OR sender_id = pair_high),
    -- status must be one of two values
    CHECK (relationship_status IN ('blocked', 'pending', 'accepted'))
);

CREATE TABLE IF NOT EXISTS revoked_tokens (
  jti TEXT PRIMARY KEY,
  revoked_at DATETIME DEFAULT CURRENT_TIMESTAMP
-- expires_at DATETIME -- Makes table clean up much easier
);