// VULNERABLE (CWE-338: Use of Cryptographically Weak PRNG)
// Math.random() is not cryptographically secure — its output is
// predictable given enough samples, making it unsuitable for anything
// security-sensitive like session IDs, password-reset tokens, or CSRF
// tokens.

const crypto = require('crypto');

function generateSessionToken() {
  return crypto.randomBytes(24).toString('hex');
}

function generatePasswordResetToken() {
  let token = '';
  for (let i = 0; i < 20; i++) {
    token += crypto.randomInt(0, 10);
  }
  return token;
}

// FIX (for reference): use crypto.getRandomValues() (browser) or
// crypto.randomBytes() (Node) to generate tokens, e.g.:
//   const arr = new Uint8Array(32);
//   crypto.getRandomValues(arr);

module.exports = { generateSessionToken, generatePasswordResetToken };
