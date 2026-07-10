# # CatálogoX API - Secure Programming and Coding

API REST interna desenvolvida para o gerenciamento de produtos utilizados por sistemas corporativos da empresa CatalogoX.

A aplicacao fornece operacoes basicas de cadastro, consulta, atualizacao e remocao de produtos, sendo utilizada como backend por ferramentas de estoque e precificacao.

---

## Funcionalidades

- Cadastro de produtos
- Listagem de produtos
- Atualizacao de produtos
- Remocao de produtos

A aplicacao funciona exclusivamente como API REST, nao possuindo interface grafica.

---

## Tecnologias Utilizadas

- Python 3
- Flask
- SQLite

---

## Como Executar a Aplicacao

1. Clonar o repositorio

git clone <url-do-repositorio>
cd catalogox-api

2. Instalar as dependencias

pip install -r requirements.txt

3. Executar a aplicacao

python app.py

A API estara disponivel em:

http://127.0.0.1:5000

Na primeira execucao, o banco de dados e inicializado automaticamente.

---

## Acesso a API

Todos os endpoints requerem autenticacao via header HTTP:

Authorization: usuario:senha

---

## Endpoints Disponiveis

- POST /produtos
- GET /produtos
- PUT /produtos/{id}
- DELETE /produtos/{id}

---

## Observacoes

- API desenvolvida para uso interno.
- Nao possui frontend.
- Projeto serve como base funcional para integracoes com outros sistemas.


---

## Relatório de Segurança e Remediação (Atividade Acadêmica)

### 1. Ferramentas Utilizadas na Análise
- **Análise Estática (SAST):** Bandit (Security Linter para Python) para varredura de vulnerabilidades estruturais.
- **Auditoria de Dependências (SCA):** CycloneDX para geração do SBOM (Software Bill of Materials).

### 2. Vulnerabilidades Identificadas (Cenário Inicial)
- **Injeção de SQL (CWE-89 / OWASP A03:2021):** O código original concatenava strings diretamente nas instruções executadas no SQLite, permitindo manipulação maliciosa das rotas de POST, PUT e DELETE.
- **Uso de Criptografia Quebrada (CWE-328 / OWASP A02:2021):** Utilização do algoritmo de hash MD5 para verificação de senhas, altamente suscetível a ataques de colisão e dicionário.
- **Credenciais Hardcoded (CWE-798 / OWASP A07:2021):** Usuário e hash de senha administrativa expostos diretamente no código-fonte.
- **Configuração de Segurança Incorreta (OWASP A05:2021):** Modo de Depuração (Debug Mode) ativado em ambiente de execução de produção, vazando rastreamentos de pilha (stack traces).

### 3. Correções Implementadas (Secure Coding)
- Substituição de todas as queries brutas por **Consultas Parametrizadas (Prepared Statements)**.
- Remoção do algoritmo MD5 e higienização das rotas de autenticação.
- Tipagem rigorosa dos parâmetros de URL nas rotas Flask (ex: `<int:produto_id>`).
- Desativação do modo debug (`debug=False`).

### 4. Resultados Obtidos
Após a remediação das falhas, novas varreduras executadas com o **Bandit** retornaram índice zero de vulnerabilidades críticas ou severas no código. A integridade do banco de dados e o controle de acesso foram blindados contra vetores clássicos de ataque a APIs.






