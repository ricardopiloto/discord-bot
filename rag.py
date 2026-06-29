import os
import hashlib
import chromadb
from chromadb.utils import embedding_functions

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONHECIMENTO_DIR = os.path.join(BASE_DIR, "conhecimento")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_data")

# Embeddings locais (não depende de nenhuma API externa)
embedding_fn = embedding_functions.DefaultEmbeddingFunction()

client = chromadb.PersistentClient(path=CHROMA_DIR)
colecao = client.get_or_create_collection(
    name="wfrp_conhecimento",
    embedding_function=embedding_fn
)

def _hash_arquivo(caminho):
    """Hash do conteúdo do arquivo, usado para detectar mudanças."""
    with open(caminho, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def _dividir_em_chunks(texto, tamanho=800, sobreposicao=100):
    """Divide o texto em pedaços com sobreposição, para preservar
    contexto entre as fronteiras dos chunks."""
    chunks = []
    inicio = 0
    while inicio < len(texto):
        fim = inicio + tamanho
        chunks.append(texto[inicio:fim])
        inicio += tamanho - sobreposicao
    return chunks

def _listar_arquivos_md(diretorio):
    arquivos = []
    for raiz, _, nomes in os.walk(diretorio):
        for nome in nomes:
            if nome.endswith(".md"):
                arquivos.append(os.path.join(raiz, nome))
    return arquivos

def _remover_arquivos_obsoletos(caminhos_relativos_atuais):
    """Remove do índice qualquer arquivo que foi indexado anteriormente
    mas não existe mais em disco (foi apagado ou movido)."""
    todos_metadados = colecao.get()["metadatas"]
    if not todos_metadados:
        return

    arquivos_indexados = {m["arquivo"] for m in todos_metadados}
    arquivos_removidos = arquivos_indexados - caminhos_relativos_atuais

    for caminho_relativo in arquivos_removidos:
        existentes = colecao.get(where={"arquivo": caminho_relativo})
        if existentes["ids"]:
            colecao.delete(ids=existentes["ids"])
            print(f"[RAG] Removido do índice (arquivo não existe mais): {caminho_relativo}")

def reindexar_se_necessario():
    """Verifica todos os arquivos em conhecimento/ e reindexa apenas
    os que mudaram (ou são novos), comparando hash com o que já está
    armazenado nos metadados do ChromaDB. Também remove do índice
    qualquer arquivo que foi apagado do disco desde a última execução."""
    if not os.path.isdir(CONHECIMENTO_DIR):
        os.makedirs(CONHECIMENTO_DIR, exist_ok=True)
        return

    arquivos = _listar_arquivos_md(CONHECIMENTO_DIR)
    caminhos_relativos_atuais = {os.path.relpath(c, CONHECIMENTO_DIR) for c in arquivos}

    _remover_arquivos_obsoletos(caminhos_relativos_atuais)

    for caminho in arquivos:
        hash_atual = _hash_arquivo(caminho)
        caminho_relativo = os.path.relpath(caminho, CONHECIMENTO_DIR)

        # Verifica se já existe algum chunk indexado para esse arquivo
        existentes = colecao.get(where={"arquivo": caminho_relativo})
        hash_indexado = None
        if existentes["metadatas"]:
            hash_indexado = existentes["metadatas"][0].get("hash")

        if hash_indexado == hash_atual:
            continue  # sem mudanças, pula

        # Remove chunks antigos desse arquivo (se houver) antes de reindexar
        if existentes["ids"]:
            colecao.delete(ids=existentes["ids"])

        with open(caminho, "r", encoding="utf-8") as f:
            texto = f.read()

        chunks = _dividir_em_chunks(texto)
        ids = [f"{caminho_relativo}::{i}" for i in range(len(chunks))]
        metadados = [
            {"arquivo": caminho_relativo, "hash": hash_atual, "chunk": i}
            for i in range(len(chunks))
        ]

        colecao.add(documents=chunks, ids=ids, metadatas=metadados)
        print(f"[RAG] Reindexado: {caminho_relativo} ({len(chunks)} chunks)")

def buscar_contexto(pergunta, top_k=4):
    """Busca os chunks mais relevantes para a pergunta/mensagem do jogador.
    Retorna uma string já formatada para injeção no prompt, ou string vazia
    se não houver nada indexado ainda."""
    if colecao.count() == 0:
        return ""

    resultados = colecao.query(query_texts=[pergunta], n_results=top_k)
    chunks = resultados.get("documents", [[]])[0]

    if not chunks:
        return ""

    return "\n\n---\n\n".join(chunks)