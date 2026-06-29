# Bertroldo — Bot de RPG para Discord

> Versão atual: **1.4.0** — veja o [CHANGELOG](CHANGELOG.md) para o histórico completo de alterações.

Bot de assistência para mesas de RPG, especializado em **Warhammer Fantasy Roleplay 4e** e outros sistemas. Roda no servidor **1noDado** e conhece a campanha da **Armada Agazzi**.

---

## Funcionalidades

- Responde perguntas sobre regras, lore e sistemas de RPG (WFRP 4e por padrão, mas também D&D, Call of Cthulhu e outros)
- **Busca semântica (RAG)** na pasta `conhecimento/` — injeta trechos relevantes de regras e lore da campanha em cada resposta
- Mantém histórico de conversa por usuário (até 10 trocas)
- Conhece todos os personagens da **Armada Agazzi** e injeta esse contexto automaticamente em cada resposta
- Associa o Discord ID do jogador ao seu personagem, ajustando o tom da resposta conforme o perfil
- Detecta e neutraliza tentativas de prompt injection sem sair do personagem
- Divide respostas longas automaticamente (respeita o limite de 2000 caracteres do Discord)

---

## Estrutura do Projeto

```
discord-bot/
├── bot.py               # Código principal do bot
├── rag.py               # Indexação e busca semântica (ChromaDB)
├── personagens.json     # Resumos dos personagens da mesa (contexto fixo)
├── requirements.txt     # Dependências Python
├── .env.example         # Template de variáveis de ambiente
├── CHANGELOG.md         # Histórico de versões
├── fichas/              # Fichas narrativas completas dos PJs (legado)
├── conhecimento/        # Base de conhecimento indexada pelo RAG
│   ├── regras/          # Regras de WFRP 4e (um .md por mecânica)
│   └── lore/            # Campanha: PJs, NPCs, locais, aventuras
└── chroma_data/         # Índice vetorial gerado automaticamente (não editar)
```

---

## Base de Conhecimento (RAG)

O módulo `rag.py` indexa todos os arquivos `.md` dentro de `conhecimento/` usando **ChromaDB** com embeddings locais (sem API externa).

### Como funciona

1. Na inicialização do bot, arquivos novos ou alterados são indexados automaticamente.
2. A cada **10 minutos**, o bot verifica mudanças e reindexa o que for necessário.
3. A cada mensagem, os **4 trechos mais relevantes** são buscados e injetados no contexto da IA.

### Adicionar conteúdo

Basta criar ou editar arquivos `.md` em `conhecimento/`. Na próxima inicialização (ou em até 10 minutos), o índice é atualizado.

**Regras de sistema** → `conhecimento/regras/` (ex.: `vantagem.md`, `cura-em-combate.md`)

**Lore da campanha** → `conhecimento/lore/` (PJs, NPCs, locais, capítulos de aventura)

Cada arquivo pode usar frontmatter YAML com `tags` para organização:

```yaml
---
tags:
  - regras
  - wfrp4e
  - combate
sistema: Warhammer Fantasy Roleplay 4ª Edição
fonte: Livro Base (Core Rulebook)
---
```

---

## Personagens da Mesa (Armada Agazzi)

| Chave      | Personagem                           |
|------------|--------------------------------------|
| `ettore`   | Ettore Agazzi — capitão mercenário   |
| `grodnar`  | Grodnar Goldhand — anão aventureiro  |
| `rocco`    | Rocco Niekisch — piromante           |
| `sarah`    | Sarah Everstein — sacerdotisa        |
| `solacruz` | Marial 'Sola' del Solacruz — guardiã |
| `helverth` | Helverth Volkmar — soldado           |
| `jehan`    | Jehan Faugrive — cavaleiro errante   |
| `konrad`   | Konrad — caçador de Altdorf          |

Os resumos ficam em `personagens.json` (sempre presentes no contexto). Fichas narrativas detalhadas estão em `fichas/` e `conhecimento/lore/`.

---

## Configuração

### Pré-requisitos

- Python 3.10+
- Conta de bot no [Discord Developer Portal](https://discord.com/developers/applications)
- Chave de API do [DeepSeek](https://platform.deepseek.com/)

### Instalação

Recomendado usar ambiente virtual (especialmente em Ubuntu, que bloqueia `pip` global):

```bash
cd discord-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Variáveis de ambiente

```bash
cp .env.example .env
```

```ini
# .env
DISCORD_TOKEN=seu_token_do_discord_aqui
DEEPSEEK_API_KEY=sua_chave_deepseek_aqui
```

> O arquivo `.env` está no `.gitignore` e nunca deve ser commitado.

### Executando

```bash
python bot.py
```

Com venv, sem ativar manualmente:

```bash
./venv/bin/python bot.py
```

### Constantes de comportamento

Definidas no topo de `bot.py`:

```python
MAX_HISTORY       = 10    # mensagens mantidas por usuário
LIMITE_CARACTERES = 2000  # tamanho máximo de mensagem de entrada
```

---

## Como usar no Discord

O bot responde apenas quando **mencionado** (`@Bertroldo`) ou em **DM**.

```
@Bertroldo como funciona a Vantagem no WFRP?
@Bertroldo quem são os personagens da Armada Agazzi?
@Bertroldo o que aconteceu com o Ettore em Grosslin?
```

### Comandos administrativos

| Comando       | Descrição |
|---------------|-----------|
| `!recarregar` | Recarrega o `personagens.json` sem reiniciar o bot. Envie mencionando o bot ou em DM. |

> Para atualizar a base RAG (`conhecimento/`), basta editar os arquivos — a reindexação é automática.

---

## Adicionando ou atualizando personagens

Edite `personagens.json`:

```json
{
  "chave_do_personagem": {
    "discord_id": "ID_NUMERICO_DO_DISCORD",
    "resumo": "Nome, origem e traços essenciais do personagem em 2-3 linhas."
  }
}
```

- **`discord_id`** — ID numérico do jogador no Discord (Modo Desenvolvedor em Configurações > Avançado). Use o placeholder `"COLOQUE_O_ID_NUMERICO_DO_DISCORD_AQUI"` se ainda não souber; o personagem aparece na lista da mesa, mas sem contexto individual.
- **`resumo`** — Texto curto injetado no contexto de toda resposta e usado para personalizar o tom quando o jogador fala.

Após editar, envie `!recarregar` no Discord ou reinicie o bot.

---

## Versionamento

O projeto segue [Semantic Versioning](https://semver.org/lang/pt-BR/). Toda mudança relevante é registrada no [CHANGELOG](CHANGELOG.md) e refletida na linha `# version:` no cabeçalho de `bot.py`.
