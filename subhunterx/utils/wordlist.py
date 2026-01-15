"""
SubHunterX Pro - Wordlist Generator
"""
import os
import itertools
from pathlib import Path

class WordlistGenerator:
    def __init__(self, config):
        self.config = config
        self.base_words = self.load_base_words()
    
    def load_base_words(self):
        """Load base wordlist"""
        wordlist_path = "data/wordlists/subdomains-top1k.txt"
        
        # Create default wordlist if missing
        if not os.path.exists(wordlist_path):
            os.makedirs("data/wordlists", exist_ok=True)
            default_words = [
                'www', 'mail', 'ftp', 'admin', 'api', 'dev', 'test', 'staging',
                'beta', 'demo', 'app', 'web', 'portal', 'dashboard', 'panel',
                'login', 'auth', 'secure', 'vpn', 'remote', 'ssh', 'git',
                'jenkins', 'grafana', 'prometheus', 'kibana', 'elastic',
                'nexus', 'artifactory', 'harbor', 'registry', 'docker',
                'kubernetes', 'k8s', 'cluster', 'master', 'node', 'worker',
                'backup', 'db', 'mysql', 'postgres', 'redis', 'mongo',
                'elasticsearch', 'grafana', 'prometheus', 'alertmanager'
            ]
            with open(wordlist_path, 'w') as f:
                f.write('\n'.join(default_words))
        
        with open(wordlist_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    
    def generate_mutations(self, domain, size=1000):
        """Generate subdomain mutations"""
        mutations = []
        
        # Base words
        for word in self.base_words[:min(100, len(self.base_words))]:
            mutations.append(word)
        
        # Common prefixes/suffixes
        prefixes = ['www', 'api', 'app', 'web', 'dev', 'test', 'staging']
        suffixes = ['.api', '.app', '.dev', '.test']
        
        for prefix in prefixes:
            mutations.append(f"{prefix}.{domain}")
        
        # Mutations
        for word in self.base_words[:50]:
            mutations.extend([
                f"{word}-dev.{domain}",
                f"{word}-staging.{domain}",
                f"{word}-prod.{domain}",
                f"{word}-backup.{domain}"
            ])
        
        return mutations[:size]
    
    def generate_enhanced_wordlist(self, size=1000):
        """Generate enhanced wordlist with mutations"""
        wordlist = []
        
        # Add base words
        wordlist.extend(self.base_words[:min(size//2, len(self.base_words))])
        
        # Add common patterns
        common_patterns = [
            'www', 'api', 'app', 'web', 'dev', 'test', 'staging', 'prod',
            'admin', 'portal', 'dashboard', 'mail', 'ftp', 'vpn', 'cdn',
            'static', 'assets', 'media', 'images', 'img', 'upload', 'uploads',
            'downloads', 'files', 'docs', 'doc', 'blog', 'shop', 'store',
            'db', 'database', 'mysql', 'postgres', 'mongo', 'redis',
            'jenkins', 'gitlab', 'git', 'svn', 'ci', 'build',
            'monitoring', 'metrics', 'grafana', 'prometheus', 'kibana',
            'elastic', 'elasticsearch', 'logstash',
            'backup', 'backups', 'bak', 'old', 'new', 'tmp', 'temp',
            'internal', 'intranet', 'extranet', 'private', 'public',
            'secure', 'auth', 'login', 'sso', 'oauth', 'accounts', 'account',
            'help', 'support', 'helpdesk', 'ticket', 'tickets',
            'beta', 'alpha', 'demo', 'sandbox', 'uat', 'qa',
            'mobile', 'm', 'wap', 'amp',
            'v1', 'v2', 'v3', 'version1', 'version2',
            'old-www', 'www2', 'www3', 'secure-www'
        ]
        
        wordlist.extend(common_patterns)
        
        # Add prefixed/suffixed versions
        prefixes = ['dev-', 'test-', 'staging-', 'prod-', 'uat-', 'qa-']
        suffixes = ['-dev', '-test', '-staging', '-prod', '-uat', '-qa', '-backup']
        
        for base in self.base_words[:50]:
            for prefix in prefixes:
                wordlist.append(f"{prefix}{base}")
            for suffix in suffixes:
                wordlist.append(f"{base}{suffix}")
        
        # Remove duplicates and limit size
        wordlist = list(set(wordlist))
        return wordlist[:size]