# Changelog

Todas as mudanças relevantes do projeto são documentadas aqui.
Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).
Versionamento segue [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [1.2.1] - 2026-06-20

### Adicionado
- Complementado a descrição da Armada Agazzi em `bot.py`

## [1.2.0] - 2026-06-19

### Adicionado
- Suporte a arquivo `.env` para armazenar `DISCORD_TOKEN` e `DEEPSEEK_API_KEY` via `python-dotenv`
- Arquivo `.env.example` como template de referência para novos ambientes
- Validação na inicialização: bot encerra com erro claro se as variáveis de ambiente estiverem ausentes

### Alterado
- `bot.py` passa a ler as chaves de API via `os.getenv()` em vez de strings literais no código

---

## [1.1.0] - 2026-06-19

### Adicionado
- Contexto da **Armada Agazzi** injetado automaticamente em todas as respostas — o bot agora sabe que os personagens formam um grupo de mercenários liderado por Ettore Agazzi
- Menção à Armada Agazzi no `SYSTEM_PROMPT`

### Corrigido
- `carregar_personagens()` retorna agora duas estruturas separadas:
  - `personagens_todos`: lista com **todos** os personagens do JSON, independente de ter `discord_id` válido (resolve o problema de Helverth e Konrad não aparecerem na listagem)
  - `personagens_por_discord_id`: índice apenas para IDs numéricos reais (usado para personalização individual)
- `discord_id` com valor placeholder (`"COLOQUE_O_ID_NUMERICO_DO_DISCORD_AQUI"`) não é mais tratado como ID válido — verificação trocada de `if discord_id:` para `discord_id.isdigit()`
- `montar_lista_personagens_da_mesa()` itera sobre `personagens_todos`, garantindo que nenhum personagem fique de fora ao responder "quem são os personagens"
- Comando `!recarregar` atualiza corretamente as duas variáveis globais

---

## [1.0.0] - 2026-06-19

### Adicionado
- Bot inicial **Bertroldo** para o servidor Discord 1noDado
- Integração com a API **DeepSeek** (`deepseek-chat`) para respostas geradas por LLM
- Histórico de conversa por usuário (até `MAX_HISTORY` trocas, padrão 10)
- Limite de tamanho de mensagem de entrada (`LIMITE_CARACTERES`, padrão 2000)
- Carregamento de personagens via `personagens.json` com indexação por `discord_id`
- Contexto individual por jogador: resumo do personagem injetado no system prompt quando o Discord ID corresponde a um cadastro
- Proteção contra **prompt injection**: detecção via regex de padrões suspeitos com reforço silencioso no contexto
- Personalidade do Bertroldo definida no `SYSTEM_PROMPT`: especialista em WFRP 4e, satírico e cômico, com regras fixas de identidade
- Comando administrativo `!recarregar` para recarregar `personagens.json` sem reiniciar o bot
- Suporte a **DM** e menções no canal
- Divisão automática de respostas longas (acima de 1900 caracteres)
