"""
Database Manager - FIXED VERSION
"""
import sqlite3
import os
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
    return engine

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
                    'status_code': sub.status_code,
                    'title': sub.title,
                    'tech_stack': sub.tech_stack,
                    'parameters': sub.parameters,
                    'risk_score': sub.risk_score,
                    'source': sub.source,
                    'created_at': sub.created_at
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
                        setattr(subdomain, key, value)
                session.commit()
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
            high_risk = query.filter(Subdomain.risk_score > 7).count()
            
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