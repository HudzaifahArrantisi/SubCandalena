# Security Policy

## 🔒 Supported Versions

Currently supported versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 3.0.x   | ✅ Yes             |
| < 3.0   | ❌ No              |

## 🚨 Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### ⚠️ Do NOT:
- Open a public issue
- Disclose the vulnerability publicly
- Test the vulnerability on systems you don't own

### ✅ Do:
1. **Email us privately**: security@subcandalena.com
2. **Include details**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### 📧 Email Template

```
Subject: [SECURITY] Vulnerability Report for SubCandalena

Vulnerability Type: [e.g., Remote Code Execution, SQL Injection]
Affected Version: [e.g., 3.0.0]
Severity: [Low/Medium/High/Critical]

Description:
[Detailed description of the vulnerability]

Steps to Reproduce:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Impact:
[What can an attacker do with this vulnerability?]

Proof of Concept:
[Code or screenshots demonstrating the issue]

Suggested Fix:
[If you have ideas on how to fix it]

Your Name: [Optional]
Contact: [Your email for follow-up]
```

## 🔐 Response Timeline

- **24 hours**: Initial acknowledgment
- **7 days**: Preliminary assessment
- **30 days**: Fix development and testing
- **90 days**: Public disclosure (coordinated)

## 🏆 Security Acknowledgments

We appreciate security researchers who responsibly disclose vulnerabilities:

- [Your Name] - [Vulnerability Type] - [Date]
- [Researcher Name] - [CVE-XXXX] - [Date]

## 🛡️ Security Best Practices

When using SubCandalena:

### For Users:
1. **Authorization**: Only scan domains you own or have permission to test
2. **Rate Limiting**: Use appropriate rate limits to avoid detection as malicious
3. **Data Protection**: Handle discovered data responsibly
4. **Updates**: Keep SubCandalena updated to the latest version
5. **Configuration**: Review and secure your `config.yaml` file

### For Developers:
1. **Input Validation**: Always validate user inputs
2. **Dependencies**: Keep dependencies updated
3. **API Keys**: Never commit API keys or secrets
4. **Code Review**: Review security-sensitive changes carefully
5. **Testing**: Test security features thoroughly

## 🔍 Known Security Considerations

### Tool Purpose
SubCandalena is a **reconnaissance tool** intended for:
- Authorized penetration testing
- Bug bounty hunting (within program scope)
- Security research on owned assets

### Legal Disclaimer
Users are responsible for ensuring their use complies with:
- Applicable laws and regulations
- Target organization's policies
- Bug bounty program rules

## 🚦 Security Features

Current security features:
- ✅ Rate limiting to prevent abuse
- ✅ Configurable timeouts
- ✅ No automatic exploitation
- ✅ Secure database storage
- ✅ Input validation

Planned security features:
- 🔄 API authentication
- 🔄 Encrypted configuration
- 🔄 Audit logging
- 🔄 User access controls

## 📚 Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Database](https://cwe.mitre.org/)
- [CVE Database](https://cve.mitre.org/)

## 📞 Contact

- Security Email: security@subcandalena.com
- PGP Key: [Coming Soon]
- Bug Bounty Program: [Coming Soon]

---

Thank you for helping keep SubCandalena and its users safe! 🙏
