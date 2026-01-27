from ldap3 import Server, Connection, ALL, NTLM
from app.core.config import settings

class LdapService:
    def __init__(self):
        self.ldap_server = settings.LDAP_SERVER
        self.ldap_domain = settings.LDAP_DOMAIN
        self.base_dn = settings.BASE_DN
        
    def ldap_authenticate(self, username: str, password: str) -> bool:
        user = f"{self.ldap_domain}\\{username}"

        try:
            server = Server(self.ldap_server, get_info=ALL)
            conn = Connection(
                server,
                user=user,
                password=password,
                authentication=NTLM,
                auto_bind=True,
            )
            conn.unbind()
            return True
        except Exception:
            return False

ldap_service = LdapService()
