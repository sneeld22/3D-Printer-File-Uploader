from ldap3 import Server, Connection, ALL, NTLM
from app.core.config import settings

class LdapService:
    def __init__(self):
        self.ldap_server = settings.LDAP_SERVER
        self.ldap_domain = settings.LDAP_DOMAIN
        self.base_dn = settings.BASE_DN
        
    def ldap_authenticate(self, username: str, password: str) -> bool:
        # For ldap.forumsys.com, username must be full DN, so build it:
        user_dn = f"uid={username},{self.base_dn}"
        
        try:
            server = Server(self.ldap_server, get_info=ALL)
            conn = Connection(server, user=user_dn, password=password, auto_bind=True)
            return conn.bound
        except Exception:
            return False

ldap_service = LdapService()
