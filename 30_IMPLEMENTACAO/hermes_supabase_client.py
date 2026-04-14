"""
Hermes Supabase Client

Módulo de integração entre o Hermes Agent e o banco de dados Supabase.
Fornece funções de consulta estruturada para o cérebro relacional do agente.

Uso:
    from hermes_supabase_client import HermesClient
    
    client = HermesClient()
    
    # Buscar contexto de um processo
    context = client.fetch_matter_context("Caso Leonardo Tepedino")
    
    # Listar repositórios ativos
    repos = client.list_repositories()
"""

import os
import json
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()


class HermesClient:
    """Cliente Supabase para o Secretário-Agente LKE"""
    
    def __init__(self):
        self._client: Optional[Client] = None
    
    @property
    def client(self) -> Client:
        """Lazy loading do cliente Supabase"""
        if self._client is None:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
            
            if not url or not key:
                raise ValueError(
                    "Falha de segurança: SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY "
                    "devem estar definidos no .env"
                )
            
            self._client = create_client(url, key)
        
        return self._client
    
    # ============================================================
    # CONSULTAS DE PROCESSOS (MATTERS)
    # ============================================================
    
    def fetch_matter_context(self, matter_title: str) -> str:
        """
        Busca contexto completo de um processo/jurídico.
        
        Retorna JSON estruturado com:
        - Dados do processo
        - Cliente vinculado
        - Repositório onde estão os documentos
        - Status e resumo
        
        Args:
            matter_title: Título ou parte do título do processo
            
        Returns:
            JSON string com os dados ou mensagem de erro
        """
        try:
            response = self.client.table("matters") \
                .select("""
                    id, title, court_id, status, case_summary,
                    clients:client_id (full_name, document_id, email),
                    repositories:repository_id (name, physical_path, node_name)
                """) \
                .ilike("title", f"%{matter_title}%") \
                .execute()
            
            if not response.data:
                return json.dumps({
                    "error": "Processo não encontrado",
                    "query": matter_title,
                    "suggestion": "Verifique o título ou use list_matters()"
                }, indent=2)
            
            return json.dumps(response.data[0], indent=2, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                "error": "Falha na consulta",
                "details": str(e)
            })
    
    def list_matters(self, status: str = None, limit: int = 20) -> str:
        """
        Lista processos cadastrados.
        
        Args:
            status: Filtrar por status (ACTIVE, CLOSED, etc.)
            limit: Número máximo de resultados
            
        Returns:
            JSON string com lista de processos
        """
        try:
            query = self.client.table("matters") \
                .select("id, title, court_id, status, case_summary") \
                .order("created_at", desc=True) \
                .limit(limit)
            
            if status:
                query = query.eq("status", status.upper())
            
            response = query.execute()
            
            return json.dumps({
                "count": len(response.data),
                "matters": response.data
            }, indent=2, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    # ============================================================
    # CONSULTAS DE CLIENTES
    # ============================================================
    
    def find_client(self, name: str = None, document: str = None) -> str:
        """
        Busca cliente por nome ou documento.
        
        Args:
            name: Nome ou parte do nome
            document: CPF/CNPJ
            
        Returns:
            JSON string com dados do cliente
        """
        try:
            query = self.client.table("clients").select("*")
            
            if name:
                query = query.ilike("full_name", f"%{name}%")
            elif document:
                query = query.eq("document_id", document)
            else:
                return json.dumps({"error": "Informe name ou document"})
            
            response = query.execute()
            
            if not response.data:
                return json.dumps({"error": "Cliente não encontrado"})
            
            return json.dumps(response.data[0], indent=2, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def list_clients(self, limit: int = 50) -> str:
        """Lista todos os clientes cadastrados"""
        try:
            response = self.client.table("clients") \
                .select("id, full_name, document_id, email") \
                .order("full_name") \
                .limit(limit) \
                .execute()
            
            return json.dumps({
                "count": len(response.data),
                "clients": response.data
            }, indent=2, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    # ============================================================
    # CONSULTAS DE REPOSITÓRIOS
    # ============================================================
    
    def list_repositories(self, node: str = None, repo_type: str = None) -> str:
        """
        Lista repositórios cadastrados.
        
        Args:
            node: Filtrar por node (Aspire, Inspirion)
            repo_type: Filtrar por tipo (OBSIDIAN, GITHUB, etc.)
            
        Returns:
            JSON string com lista de repositórios
        """
        try:
            query = self.client.table("repositories") \
                .select("id, name, physical_path, node_name, repo_type") \
                .order("name")
            
            if node:
                query = query.eq("node_name", node)
            if repo_type:
                query = query.eq("repo_type", repo_type.upper())
            
            response = query.execute()
            
            return json.dumps({
                "count": len(response.data),
                "repositories": response.data
            }, indent=2, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def get_repository_path(self, repo_name: str) -> str:
        """
        Retorna o caminho físico de um repositório.
        
        Útil para o Hermes saber onde acessar os documentos.
        
        Args:
            repo_name: Nome do repositório
            
        Returns:
            JSON string com path e node
        """
        try:
            response = self.client.table("repositories") \
                .select("name, physical_path, node_name, repo_type") \
                .eq("name", repo_name) \
                .execute()
            
            if not response.data:
                return json.dumps({
                    "error": "Repositório não encontrado",
                    "query": repo_name
                })
            
            return json.dumps(response.data[0], indent=2, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    # ============================================================
    # CONSULTAS DE FERRAMENTAS E SKILLS
    # ============================================================
    
    def list_tools(self, active_only: bool = True) -> str:
        """Lista ferramentas disponíveis"""
        try:
            query = self.client.table("tools").select("*")
            
            if active_only:
                query = query.eq("is_active", True)
            
            response = query.execute()
            
            return json.dumps({
                "count": len(response.data),
                "tools": response.data
            }, indent=2, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def list_skills(self) -> str:
        """Lista skills de agentes cadastradas"""
        try:
            response = self.client.table("agent_skills") \
                .select("""
                    id, name, description,
                    tools:tool_id (name, command_prefix)
                """) \
                .execute()
            
            return json.dumps({
                "count": len(response.data),
                "skills": response.data
            }, indent=2, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    # ============================================================
    # CONSULTAS DE CREDENCIAIS
    # ============================================================
    
    def get_credential_ref(self, service: str) -> str:
        """
        Retorna referência de credencial (NÃO o valor).
        
        O agente usa isso para saber onde buscar a credencial
        real (env, arquivo, etc.)
        
        Args:
            service: Nome do serviço (GOOGLE_WORKSPACE, etc.)
            
        Returns:
            JSON string com referência da credencial
        """
        try:
            response = self.client.table("vault_credentials") \
                .select("service_name, credential_id, metadata") \
                .eq("service_name", service.upper()) \
                .execute()
            
            if not response.data:
                return json.dumps({
                    "error": "Credencial não encontrada",
                    "service": service,
                    "available_services": self._list_services()
                })
            
            return json.dumps(response.data[0], indent=2, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def _list_services(self) -> List[str]:
        """Lista serviços com credenciais cadastradas"""
        try:
            response = self.client.table("vault_credentials") \
                .select("service_name") \
                .execute()
            
            return [r["service_name"] for r in response.data]
            
        except:
            return []
    
    # ============================================================
    # LOG DE SESSÕES
    # ============================================================
    
    def log_session(self, matter_id: str = None, skill_id: str = None,
                    agent_name: str = "Hermes", input_payload: dict = None,
                    output_summary: str = None, execution_time_ms: int = None) -> str:
        """
        Registra uma sessão de trabalho no log.
        
        Args:
            matter_id: ID do processo relacionado
            skill_id: ID da skill utilizada
            agent_name: Nome do agente
            input_payload: Dados de entrada
            output_summary: Resumo da saída
            execution_time_ms: Tempo de execução em milissegundos
            
        Returns:
            JSON string com ID da sessão criada
        """
        try:
            data = {
                "agent_name": agent_name,
                "input_payload": input_payload,
                "output_summary": output_summary,
                "execution_time_ms": execution_time_ms
            }
            
            if matter_id:
                data["matter_id"] = matter_id
            if skill_id:
                data["skill_used"] = skill_id
            
            # Remover None values
            data = {k: v for k, v in data.items() if v is not None}
            
            response = self.client.table("work_sessions").insert(data).execute()
            
            return json.dumps({
                "success": True,
                "session_id": response.data[0]["id"]
            })
            
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def get_recent_sessions(self, limit: int = 10) -> str:
        """Lista sessões recentes"""
        try:
            response = self.client.table("work_sessions") \
                .select("""
                    id, agent_name, output_summary, 
                    execution_time_ms, created_at,
                    matters:title (title)
                """) \
                .order("created_at", desc=True) \
                .limit(limit) \
                .execute()
            
            return json.dumps({
                "count": len(response.data),
                "sessions": response.data
            }, indent=2, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({"error": str(e)})


# ============================================================
# FUNÇÕES DE CONVENIÊNCIA (para uso direto)
# ============================================================

def get_client() -> HermesClient:
    """Retorna instância do cliente Hermes"""
    return HermesClient()


def fetch_matter_context(matter_title: str) -> str:
    """Função de conveniência para buscar contexto de processo"""
    return HermesClient().fetch_matter_context(matter_title)


# ============================================================
# CLI DE TESTE
# ============================================================

if __name__ == "__main__":
    import sys
    
    client = HermesClient()
    
    if len(sys.argv) < 2:
        print("Uso: python hermes_supabase_client.py <comando> [args]")
        print("\nComandos:")
        print("  matters                    - Lista processos")
        print("  matter <titulo>            - Busca contexto de processo")
        print("  clients                    - Lista clientes")
        print("  repos                      - Lista repositórios")
        print("  tools                      - Lista ferramentas")
        print("  sessions                   - Sessões recentes")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "matters":
        print(client.list_matters())
    elif cmd == "matter":
        if len(sys.argv) < 3:
            print("Uso: matter <titulo>")
        else:
            print(client.fetch_matter_context(sys.argv[2]))
    elif cmd == "clients":
        print(client.list_clients())
    elif cmd == "repos":
        print(client.list_repositories())
    elif cmd == "tools":
        print(client.list_tools())
    elif cmd == "sessions":
        print(client.get_recent_sessions())
    else:
        print(f"Comando desconhecido: {cmd}")
