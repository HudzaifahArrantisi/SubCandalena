"""
Database Manager - FIXED VERSION
"""
import sqlite3
import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from ..utils.helpers import load_config
from .models import Base, Subdomain, ScanSession

def init_db():
    """Initialize database"""
    config = load_config()
    db_path = config['database']['path']
    
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)
    _ensure_subdomain_columns(db_path)
    return engine


def _ensure_subdomain_columns(db_path):
    """Add new columns to existing SQLite databases without requiring Alembic."""
    columns = {
        'url': 'TEXT',
        'ip_address': 'TEXT',
        'a_records': 'TEXT',
        'aaaa_records': 'TEXT',
        'cname': 'TEXT',
        'redirect_chain': 'TEXT',
        'server': 'TEXT',
        'content_type': 'TEXT',
        'response_size': 'INTEGER',
        'tls_issuer': 'TEXT',
        'tls_expiry': 'TEXT',
        'tls_san': 'TEXT',
        'open_ports': 'TEXT',
        'cdn_waf': 'TEXT',
        'risk_level': 'TEXT',
        'risk_reasons': 'TEXT',
        'takeover_candidate': 'TEXT',
        'first_seen': 'DATETIME',
        'last_seen': 'DATETIME'
    }
    try:
        conn = sqlite3.connect(db_path)
        existing = {row[1] for row in conn.execute('PRAGMA table_info(subdomains)').fetchall()}
        for name, sql_type in columns.items():
            if name not in existing:
                conn.execute(f'ALTER TABLE subdomains ADD COLUMN {name} {sql_type}')
        conn.commit()
    finally:
        try:
            conn.close()
        except Exception:
            pass

class DBManager:
    def __init__(self):
        self.engine = init_db()
        self.Session = sessionmaker(bind=self.engine)
    
    def save_subdomain(self, subdomain_data, **kwargs):
        session = self.Session()
        try:
            # Merge kwargs into subdomain_data if it's a dict
            if isinstance(subdomain_data, dict):
                data = {**subdomain_data, **kwargs}
            else:
                # If subdomain_data is a string, assume it's the subdomain name
                data = {'subdomain': subdomain_data, **kwargs}
            
            now = datetime.utcnow()
            subdomain_name = data.get('subdomain')
            existing = session.query(Subdomain).filter(Subdomain.subdomain == subdomain_name).first()
            if existing:
                for key, value in data.items():
                    if hasattr(existing, key) and value is not None:
                        setattr(existing, key, self._serialize(value))
                existing.last_seen = now
            else:
                data = {key: self._serialize(value) for key, value in data.items()}
                data.setdefault('first_seen', now)
                data.setdefault('last_seen', now)
                subdomain = Subdomain(**data)
                session.add(subdomain)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"⚠️  Database error: {e}")
        finally:
            session.close()
    
    def get_all_subdomains(self, domain=None):
        """Get all subdomains, optionally filtered by domain"""
        session = self.Session()
        try:
            if domain:
                subdomains = session.query(Subdomain).filter(
                    Subdomain.subdomain.like(f'%{domain}%')
                ).all()
            else:
                subdomains = session.query(Subdomain).all()
            
            # Convert to list of dicts
            results = []
            for sub in subdomains:
                results.append({
                    'id': sub.id,
                    'domain': sub.domain,
                    'subdomain': sub.subdomain,
                    'url': sub.url,
                    'ip_address': sub.ip_address,
                    'a_records': self._deserialize(sub.a_records),
                    'aaaa_records': self._deserialize(sub.aaaa_records),
                    'cname': sub.cname,
                    'status_code': sub.status_code,
                    'redirect_chain': self._deserialize(sub.redirect_chain),
                    'server': sub.server,
                    'content_type': sub.content_type,
                    'response_size': sub.response_size,
                    'tls_issuer': sub.tls_issuer,
                    'tls_expiry': sub.tls_expiry,
                    'tls_san': self._deserialize(sub.tls_san),
                    'open_ports': self._deserialize(sub.open_ports),
                    'cdn_waf': sub.cdn_waf,
                    'title': sub.title,
                    'tech_stack': sub.tech_stack,
                    'parameters': self._deserialize(sub.parameters),
                    'risk_score': sub.risk_score,
                    'risk_level': sub.risk_level,
                    'risk_reasons': self._deserialize(sub.risk_reasons),
                    'takeover_candidate': sub.takeover_candidate,
                    'source': sub.source,
                    'created_at': sub.created_at,
                    'first_seen': sub.first_seen,
                    'last_seen': sub.last_seen
                })
            return results
        except Exception as e:
            print(f"⚠️  Database error: {e}")
            return []
        finally:
            session.close()
    
    def update_analysis(self, subdomain_data):
        """Update subdomain with analysis results"""
        session = self.Session()
        try:
            subdomain_name = subdomain_data.get('subdomain')
            if not subdomain_name:
                return
            
            subdomain = session.query(Subdomain).filter(
                Subdomain.subdomain == subdomain_name
            ).first()
            
            if subdomain:
                # Update existing record
                for key, value in subdomain_data.items():
                    if hasattr(subdomain, key):
                        setattr(subdomain, key, self._serialize(value))
                subdomain.last_seen = datetime.utcnow()
                session.commit()
            else:
                self.save_subdomain(subdomain_data)
        except Exception as e:
            session.rollback()
            print(f"⚠️  Database error: {e}")
        finally:
            session.close()
    
    def get_stats(self, domain=None):
        """Get statistics about subdomains"""
        session = self.Session()
        try:
            query = session.query(Subdomain)
            if domain:
                query = query.filter(Subdomain.subdomain.like(f'%{domain}%'))
            
            total = query.count()
            live = query.filter(Subdomain.status_code.isnot(None)).count()
            high_risk = query.filter(Subdomain.risk_score >= 70).count()
            
            return {
                'total': total,
                'live': live,
                'high_risk': high_risk
            }
        except Exception as e:
            print(f"⚠️  Database error: {e}")
            return {'total': 0, 'live': 0, 'high_risk': 0}
        finally:
            session.close()

    def get_results(self, domain=None):
        """Compatibility wrapper used by the API server."""
        results = self.get_all_subdomains(domain)
        stats = self.get_stats(domain)
        return {
            'status': 'success',
            'data': results,
            'count': len(results),
            **stats
        }

    def snapshot(self, domain):
        """Return current result snapshot keyed by subdomain."""
        return {item['subdomain']: item for item in self.get_all_subdomains(domain)}

    @staticmethod
    def diff_snapshots(before, after):
        before_keys = set(before)
        after_keys = set(after)
        changed = []
        for subdomain in sorted(before_keys & after_keys):
            old = before[subdomain]
            new = after[subdomain]
            if old.get('status_code') != new.get('status_code') or old.get('risk_level') != new.get('risk_level'):
                changed.append({
                    'subdomain': subdomain,
                    'old_status': old.get('status_code'),
                    'new_status': new.get('status_code'),
                    'old_risk': old.get('risk_level'),
                    'new_risk': new.get('risk_level')
                })
        return {
            'new': [after[key] for key in sorted(after_keys - before_keys)],
            'removed': [before[key] for key in sorted(before_keys - after_keys)],
            'changed': changed
        }

    def create_scan_session(self, domain, total, high_risk):
        session = self.Session()
        try:
            scan = ScanSession(
                target_domain=domain,
                total_subdomains=total,
                high_risk_count=high_risk,
                scan_completed=datetime.utcnow()
            )
            session.add(scan)
            session.commit()
            return scan.id
        except Exception as e:
            session.rollback()
            print(f"⚠️  Database error: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def _serialize(value):
        if isinstance(value, (list, dict)):
            return json.dumps(value, ensure_ascii=False)
        return value

    @staticmethod
    def _deserialize(value):
        if not isinstance(value, str):
            return value
        try:
            return json.loads(value)
        except Exception:
            return value
