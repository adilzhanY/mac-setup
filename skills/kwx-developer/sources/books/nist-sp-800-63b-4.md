# NIST SP 800-63B-4: Digital Identity Guidelines, Authentication and Authenticator Management

Legal free source (US government, public domain): https://pages.nist.gov/800-63-4/sp800-63b.html

## What I read

Section 3.1.1 (passwords) and the reauthentication timeout table (section 2 and Table 1). Not read: the authenticator types beyond passwords, federation (SP 800-63C), identity proofing (SP 800-63A).

## Key lessons used in backend/auth.md

- Passwords as the only factor: minimum 15 characters. Inside MFA: minimum 8. Maximum at least 64. Unicode code points count as one character.
- No composition rules, no periodic forced changes; change only on evidence of compromise.
- Compare new passwords against a blocklist of common, expected and compromised passwords (whole password), and tell the user why it was rejected.
- At most 100 consecutive failed attempts per account before the authenticator is disabled.
- No hints, no knowledge based questions, request the full password, allow password managers and paste, offer show password.
- Salted with at least 32 bits and hashed with a suitable password hashing scheme; a separately stored keyed hash (pepper) is recommended.
- Reauthentication: AAL1 overall at most 30 days; AAL2 overall at most 24 h and inactivity at most 1 h; AAL3 overall at most 12 h (SHALL) and inactivity at most 15 min.
