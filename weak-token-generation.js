// VULNERABLE (CWE-338: Use of Cryptographically Weak PRNG)
// Math.random() is not cryptographically secure — its output is
// predictable given enough samples, making it unsuitable for anything
// security-sensitive like session IDs, password-reset tokens, or CSRF
// tokens.

function generateSessionToken() {
  return Math.random().toString(36).substring(2); // <-- weak PRNG
}

function generatePasswordResetToken() {
  let token = '';
  for (let i = 0; i < 20; i++) {
    token += Math.floor(Math.random() * 10); // <-- weak PRNG, small space
  }
  return token;
}

// FIX (for reference): use crypto.getRandomValues() (browser) or
// crypto.randomBytes() (Node) to generate tokens, e.g.:
//   const arr = new Uint8Array(32);
//   crypto.getRandomValues(arr);

module.exports = { generateSessionToken, generatePasswordResetToken };
