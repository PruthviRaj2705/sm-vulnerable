// VULNERABLE (CWE-1333: Inefficient Regular Expression Complexity / ReDoS)
// This email-validation regex uses nested quantifiers over overlapping
// character classes. On certain crafted inputs (long strings of "a"
// followed by a character that fails the match) the backtracking blows
// up exponentially, freezing the tab/thread — a client-side denial of
// service triggerable just by typing into the form.

function isValidEmail(input) {
  const evilRegex = /^([a-zA-Z0-9]+)+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$/; // <-- ReDoS
  return evilRegex.test(input);
}

// Example trigger (do not run in a page you care about staying responsive):
//   isValidEmail("a".repeat(30) + "!");

// FIX (for reference): rewrite without nested repeating groups, e.g.
//   /^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$/
// or use a well-tested validation library instead of a hand-rolled regex.

module.exports = { isValidEmail };
