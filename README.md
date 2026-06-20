# Bertroldo — Bot de RPG para Discord

> Versão atual: **1.2.1** — veja o [CHANGELOG](CHANGELOG.md) para o histórico completo de alterações.

Bot de assistência para mesas de RPG, especializado em **Warhammer Fantasy Roleplay 4e** e outros sistemas. Roda no servidor **1noDado** e conhece a campanha da **Armada Agazzi**.

---

## Funcionalidades

- Responde perguntas sobre regras, lore e sistemas de RPG (WFRP 4e por padrão, mas também D&D, Call of Cthulhu e outros)
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
├── personagens.json     # Fichas resumidas dos personagens da mesa
├── fichas/              # Fichas completas em Markdown (uma por personagem)
└── README.md
```

---

## Personagens da Mesa (Armada Agazzi)

| Chave        | Personagem                          |
|--------------|-------------------------------------|
| `ettore`     | Ettore Agazzi — capitão mercenário  |
| `grodnar`    | Grodnar Goldhand — anão aventureiro |
| `rocco`      | Rocco Niekisch — piromante          |
| `sarah`      | Sarah Everstein — sacerdotisa       |
| `solacruz`   | Marial 'Sola' del Solacruz — guardiã |
| `helverth`   | Helverth Volkmar — soldado          |
| `jehan`      | Jehan Faugrive — cavaleiro errante  |
| `konrad`     | Konrad — caçador de Altdorf         |

Os resumos de cada personagem ficam em `personagens.json`. As fichas completas ficam na pasta `fichas/`.

---

## Configuração

### Pré-requisitos

- Python 3.10+
- Conta de bot no [Discord Developer Portal](https://discord.com/developers/applications)
- Chave de API do [DeepSeek](https://platform.deepseek.com/)

### Instalação

```bash
pip install discord.py aiohttp python-dotenv
```

### Variáveis de ambiente

Copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp .env.example .env
```

```ini
# .env
DISCORD_TOKEN=seu_token_do_discord_aqui
DEEPSEEK_API_KEY=sua_chave_deepseek_aqui
```

> O arquivo `.env` já está no `.gitignore` e nunca será commitado.

As demais constantes de comportamento ficam no topo de `bot.py`:

```python
MAX_HISTORY       = 10    # mensagens mantidas por usuário
LIMITE_CARACTERES = 2000  # tamanho máximo de mensagem de entrada
```

### Executando

```bash
python bot.py
```

---

## Como usar no Discord

O bot responde apenas quando **mencionado** (`@Bertroldo`) ou em **DM**.

```
@Bertroldo quais são as regras de flanqueamento no WFRP?
@Bertroldo quem são os personagens da Armada Agazzi?
```

### Comando administrativo

| Comando        | Descrição |
|----------------|-----------|
| `!recarregar`  | Recarrega o `personagens.json` sem reiniciar o bot. Deve ser enviado mencionando o bot ou em DM. |

---

## Adicionando ou atualizando personagens

Edite `personagens.json` seguindo o formato:

```json
{
  "chave_do_personagem": {
    "discord_id": "ID_NUMERICO_DO_DISCORD",
    "resumo": "Nome, origem e traços essenciais do personagem em 2-3 linhas."Ettore Agazzi.md
Grodnar Goldhand.md
Helverth Volkmar.md
Jehan Faugrive.md
Konrad.md
Marial Eduarda del Solacruz.md
Rocco Niekisch.md
Sarah Everstein.md
```

- **`discord_id`** — ID numérico do jogador no Discord (ative Modo Desenvolvedor em Configurações > Avançado, depois clique com o botão direito no usuário). Deixe o placeholder `"COLOQUE_O_ID_NUMERICO_DO_DISCORD_AQUI"` se ainda não souber; o personagem aparecerá na lista da mesa, mas sem contexto individual.
- **`resumo`** — Texto curto usado pelo bot para contextualizar as respostas. Inclua nome, origem, classe/profissão e traços de personalidade relevantes.

Após editar o arquivo, envie `!recarregar` no Discord para aplicar sem reiniciar o bot.
