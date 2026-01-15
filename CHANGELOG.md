# Changelog

All notable changes to SubCandalena will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2026-01-15

### 🎉 Initial Release

#### Added
- **Core Features**
  - Multi-threaded subdomain reconnaissance engine
  - 20+ passive reconnaissance sources
  - Intelligent brute force with AI-powered mutations
  - Real-time web dashboard
  - REST API server
  - SQLite database for persistent storage
  
- **Reconnaissance Capabilities**
  - Certificate Transparency monitoring
  - DNS enumeration and zone transfer attempts
  - Search engine dorking (Google, Bing, Yahoo)
  - Archive crawling (Wayback Machine)
  - Security platform integration (VirusTotal, AlienVault)
  - Code repository searching (GitHub, GitLab)
  
- **Analysis Features**
  - HTTP/HTTPS probing
  - Technology detection
  - Screenshot capture
  - SSL/TLS analysis
  - Response analysis
  
- **Output Formats**
  - JSON structured output
  - CSV spreadsheet format
  - HTML report with screenshots
  - Plain text list
  
- **User Interface**
  - Rich CLI with progress bars
  - Interactive web dashboard
  - Real-time statistics
  - Subdomain explorer
  - Screenshot gallery
  
- **Configuration**
  - YAML configuration file
  - Custom wordlist support
  - Thread control
  - Rate limiting
  - Timeout configuration
  
- **Documentation**
  - Comprehensive README
  - 7 detailed tutorials
  - API documentation
  - Configuration guide
  - Security best practices

#### Technical Details
- Python 3.8+ support
- Async/await implementation for performance
- SQLAlchemy ORM for database
- FastAPI for REST API
- Rich library for terminal UI
- Selenium for screenshots

#### Dependencies
- rich==13.7.1
- aiohttp==3.9.1
- requests==2.31.0
- fastapi==0.104.1
- uvicorn==0.24.0
- sqlalchemy==2.0.23
- pillow==10.1.0
- beautifulsoup4==4.12.2
- selenium==4.15.2
- plotly==5.17.0
- pyyaml==6.0.1

### Known Issues
- Screenshot capture may be slow on systems with limited resources
- Some passive sources may have rate limits
- Wildcard DNS detection needs improvement

---

## [Unreleased]

### Planned for v3.1.0
- [ ] Docker containerization
- [ ] Kubernetes cluster scanning
- [ ] Cloud provider integration (AWS, Azure, GCP)
- [ ] Advanced HTML report templates
- [ ] CI/CD pipeline examples
- [ ] Unit tests coverage
- [ ] Performance optimizations

### Planned for v3.2.0
- [ ] Machine learning for subdomain prediction
- [ ] Integration with Burp Suite
- [ ] Integration with OWASP ZAP
- [ ] Mobile application (iOS/Android)
- [ ] WebSocket support for real-time updates
- [ ] Advanced filtering and search

### Planned for v4.0.0
- [ ] Distributed scanning cluster
- [ ] Real-time collaboration features
- [ ] Enterprise SaaS platform
- [ ] Advanced AI-powered reconnaissance
- [ ] Automated exploitation framework
- [ ] Threat intelligence integration

---

## Version History

### Version Numbering
- **Major.Minor.Patch** (e.g., 3.0.0)
- **Major**: Breaking changes
- **Minor**: New features, backwards compatible
- **Patch**: Bug fixes, minor improvements

### Release Tags
- `[Added]` for new features
- `[Changed]` for changes in existing functionality
- `[Deprecated]` for soon-to-be removed features
- `[Removed]` for now removed features
- `[Fixed]` for bug fixes
- `[Security]` for vulnerability fixes

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this changelog.

When contributing:
1. Add your changes under `[Unreleased]` section
2. Use appropriate tags (`[Added]`, `[Fixed]`, etc.)
3. Include brief description of the change
4. Reference issue numbers if applicable

Example:
```markdown
### [Added]
- New passive source integration for subdomain discovery (#123)
- Export functionality for PDF reports (#145)

### [Fixed]
- Fixed timeout issues with slow DNS servers (#156)
- Corrected screenshot path resolution on Windows (#167)
```

---

## Support

For questions about changes or versions:
- Open an issue on GitHub
- Check documentation
- Contact maintainers

---

Last Updated: 2026-01-15
