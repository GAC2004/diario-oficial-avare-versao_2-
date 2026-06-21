# Relatório de Exploração e Processamento de Dados — Diário Oficial Inteligente de Avaré (RAG)

**Disciplina:** Redes Neurais e Inteligência Artificial Aplicada  
**Instituição:** Faculdade de Engenharia e Administração Paulista de Avaré (FEAP)  
**Curso:** Engenharia da Computação  

---

# 1. Introdução

Este documento descreve o processo de exploração, coleta, processamento e construção da base de dados do projeto **Diário Oficial Inteligente de Avaré**, um sistema baseado em **RAG (Retrieval-Augmented Generation)** para consulta semântica de documentos públicos municipais.

O objetivo do sistema é permitir que usuários realizem perguntas em linguagem natural sobre publicações oficiais do município, recuperando automaticamente os trechos mais relevantes a partir de uma base vetorial.

O pipeline integra técnicas de **Web Scraping, NLP, embeddings semânticos e busca vetorial com FAISS**.

---

# 2. Fonte dos Dados

Os dados são obtidos do portal oficial da Imprensa Oficial do Município de Avaré:

https://imprensaoficialmunicipal.com.br/avare

O portal disponibiliza edições do Diário Oficial contendo:

- Leis
- Decretos
- Portarias
- Atos administrativos
- Publicações diversas

Cada edição pode ser baixada em formato PDF.

---

# 3. Arquitetura Geral do Sistema

O sistema é composto por quatro módulos principais:

- scraper.py → Coleta de PDFs  
- extractor.py → Extração de texto dos PDFs  
- embedder.py → Geração de embeddings + índice FAISS  
- rag.py → Busca semântica (RAG)  
- app.py → Interface Web (Flask)

Fluxo geral:

PDFs → Texto → Chunks → Embeddings → FAISS → Consulta semântica

---

# 4. Coleta de Dados (Web Scraping)

A coleta é realizada pelo módulo:

src/scraper.py

### Funcionalidades:

- Acesso ao portal oficial  
- Identificação de edições por seção (Leis, Decretos, Portarias)  
- Extração de IDs das publicações  
- Download automático dos PDFs  
- Organização por período (AAAA-MM)

### Estrutura de armazenamento:

data/pdfs/AAAA-MM/edicao_ID.pdf

---

# 5. Extração de Texto dos PDFs

A extração é feita pelo módulo:

src/extractor.py

Utilizando a biblioteca pdfplumber.

### Processo:

- Leitura página por página  
- Extração de texto bruto  
- Organização estruturada em JSON  
- Concatenação em texto completo  

### Estrutura gerada:

{
  "source": "arquivo.pdf",
  "date": "2026-05",
  "pages": [{"page": 1, "text": "..."}],
  "full_text": "texto completo..."
}

---

# 6. Geração da Base Vetorial

A vetorização é realizada pelo módulo:

src/embedder.py

### Tecnologias utilizadas:

- FAISS (similaridade vetorial)
- Sentence Transformers
- Modelo: paraphrase-multilingual-MiniLM-L12-v2

### Processo:

- Divisão dos textos em chunks  
- Geração de embeddings  
- Normalização vetorial  
- Indexação no FAISS  
- Salvamento de metadados  

### Saída:

vector_db/
 ├── index.faiss
 └── metadata.pkl

---

# 7. Sistema RAG (Retrieval-Augmented Generation)

Implementado em:

src/rag.py

### Funcionamento:

1. Usuário faz pergunta  
2. Pergunta é convertida em embedding  
3. Busca vetorial no FAISS  
4. Filtragem por ano/mês (opcional)  
5. Retorno dos trechos mais relevantes  

### Características:

- Busca semântica (não apenas palavras-chave)  
- Suporte a filtros temporais  
- Ranking por similaridade  
- Retorno de fontes originais  

---

# 8. Interface Web

A interface foi desenvolvida com Flask.

### Funcionalidades:

- Campo de pergunta em linguagem natural  
- Filtros por ano e mês  
- Controle de top-k resultados  
- Visualização de trechos relevantes  
- Exibição de score de relevância  
- Pipeline de atualização em tempo real  

---

# 9. Pipeline de Atualização

O sistema possui pipeline automatizado:

scraper → extractor → embedder → reload RAG

Executado em thread separada.

### Etapas:

1. Verificação de novas edições  
2. Extração de PDFs  
3. Atualização do índice vetorial  
4. Recarregamento do sistema RAG  

---

# 10. Tecnologias Utilizadas

| Tecnologia | Finalidade |
|------------|-----------|
| Python | Linguagem principal |
| Flask | Interface web |
| Requests | Requisições HTTP |
| BeautifulSoup | Scraping HTML |
| pdfplumber | Extração de texto PDF |
| FAISS | Busca vetorial |
| PyTorch | Embeddings |
| Sentence Transformers | NLP |
| Threading | Pipeline assíncrono |
| Pickle | Persistência de dados |

---

# 11. Principais Desafios

## 11.1 Estrutura variável dos PDFs

Os documentos possuem formatação inconsistente.

---

## 11.2 PDFs sem texto

Algumas edições são imagens digitalizadas.

---

## 11.3 Performance do embedding

Alto custo computacional na geração dos vetores.

---

## 11.4 Sincronização do pipeline

Necessidade de controle de concorrência com threads.

---

# 12. Características do Sistema

- Busca semântica avançada  
- Atualização incremental  
- Interface web interativa  
- Pipeline automatizado  
- Estrutura escalável  

---

# 13. Resultados Obtidos

- Consulta inteligente de documentos públicos  
- Recuperação precisa de trechos relevantes  
- Redução do tempo de busca manual  
- Organização estruturada de PDFs  

---

# 14. Conclusão

O projeto demonstra a aplicação de técnicas modernas de IA e NLP na análise de documentos públicos.

A utilização de RAG com FAISS permite buscas semânticas mais inteligentes do que métodos tradicionais baseados em palavras-chave.

O sistema automatiza todo o fluxo: coleta, processamento, indexação e consulta dos dados do Diário Oficial de Avaré.