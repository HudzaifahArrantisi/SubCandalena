from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Subdomain(Base):
    __tablename__ = 'subdomains'
    
    id = Column(Integer, primary_key=True)
    domain = Column(String(255), index=True)
    subdomain = Column(String(255), index=True)
    status_code = Column(Integer)
    url = Column(Text)
    ip_address = Column(Text)
    a_records = Column(Text)
    aaaa_records = Column(Text)
    cname = Column(Text)
    redirect_chain = Column(Text)
    server = Column(Text)
    content_type = Column(Text)
    response_size = Column(Integer)
    tls_issuer = Column(Text)
    tls_expiry = Column(Text)
    tls_san = Column(Text)
    open_ports = Column(Text)
    cdn_waf = Column(Text)
    title = Column(Text)
    tech_stack = Column(Text)
    parameters = Column(Text)  # JSON string
    risk_score = Column(Float)
    risk_level = Column(String(20))
    risk_reasons = Column(Text)
    takeover_candidate = Column(String(20))
    source = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    screenshot_hash = Column(String(64))

class ScanSession(Base):
    __tablename__ = 'scan_sessions'
    id = Column(Integer, primary_key=True)
    target_domain = Column(String(255))
    total_subdomains = Column(Integer)
    high_risk_count = Column(Integer)
    scan_completed = Column(DateTime)

def init_db(database_url):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()
