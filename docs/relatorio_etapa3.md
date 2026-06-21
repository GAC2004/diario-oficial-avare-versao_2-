# Relatório da Etapa 3 – Geração de Embeddings e Implementação do Sistema RAG 

# Sistema Inteligente para Consulta ao Diário Oficial do Município de Avaré

---

# 1. Objetivo

Após a coleta dos documentos e a extração dos textos, a terceira etapa do projeto teve como objetivo transformar o conteúdo textual em representações vetoriais (embeddings), permitindo que o sistema realizasse buscas por significado e não apenas por palavras exatas.

Além disso, foi implementada a arquitetura **RAG (Retrieval-Augmented Generation)**, responsável por recuperar os trechos mais relevantes dos documentos antes de gerar uma resposta para o usuário.

Essa abordagem melhora significativamente a precisão das respostas e reduz a ocorrência de informações incorretas (alucinações) em modelos de Inteligência Artificial.

---

# 2. O que são Embeddings?

Embeddings são representações numéricas de textos em um espaço vetorial multidimensional.

Cada documento é convertido em um vetor de números que preserva o significado semântico do conteúdo.

Dessa forma, textos que tratam do mesmo assunto ficam próximos entre si nesse espaço vetorial, mesmo que utilizem palavras diferentes.

Por exemplo:

* "Contratação de servidores públicos"
* "Admissão de funcionários municipais"

Embora utilizem vocabulários distintos, possuem significado semelhante e, consequentemente, embeddings próximos.

---

# 3. Modelo Utilizado

Para gerar os embeddings foi utilizado um modelo pré-treinado da biblioteca **Sentence Transformers**, otimizado para tarefas de busca semântica.

Esse modelo converte automaticamente cada documento em um vetor de alta dimensão, preservando informações de contexto e significado.

A utilização de modelos pré-treinados reduz o tempo de desenvolvimento e oferece excelente desempenho em tarefas de recuperação de informação.

---

# 4. Processo de Geração dos Embeddings

O processamento ocorre em diversas etapas:

1. Carregamento dos textos processados.
2. Leitura individual de cada documento.
3. Conversão do texto em embedding.
4. Armazenamento do vetor correspondente.
5. Associação do vetor ao documento original.

Ao final do processo, cada publicação possui uma representação vetorial pronta para consultas semânticas.

---

# 5. Banco Vetorial

Os embeddings gerados são armazenados em um banco vetorial.

Esse banco permite localizar rapidamente os documentos mais semelhantes à consulta realizada pelo usuário.

Ao invés de pesquisar apenas por palavras-chave, o sistema compara a proximidade entre vetores utilizando medidas matemáticas de similaridade.

Entre as métricas mais utilizadas destacam-se:

* Similaridade do Cosseno (Cosine Similarity)
* Distância Euclidiana
* Produto Escalar

Neste projeto foi utilizada a Similaridade do Cosseno, amplamente empregada em aplicações de Processamento de Linguagem Natural.

---

# 6. Arquitetura RAG

A arquitetura RAG combina dois processos principais:

### Recuperação (Retrieval)

Quando o usuário faz uma pergunta, ela também é convertida em um embedding.

Em seguida, o sistema pesquisa no banco vetorial quais documentos possuem maior similaridade com essa consulta.

São recuperados apenas os documentos mais relevantes.

### Geração (Generation)

Os trechos recuperados são utilizados como contexto para o modelo de linguagem.

Com base nessas informações, o sistema produz uma resposta fundamentada nos documentos oficiais do Diário Oficial.

Essa estratégia aumenta a confiabilidade das respostas e reduz a possibilidade de gerar informações inexistentes.

---

# 7. Fluxo de Funcionamento

O funcionamento completo pode ser resumido da seguinte forma:

```text
Usuário
    │
    ▼
Pergunta
    │
    ▼
Embedding da Pergunta
    │
    ▼
Banco Vetorial
    │
    ▼
Documentos Mais Relevantes
    │
    ▼
Modelo de Linguagem
    │
    ▼
Resposta Baseada nos Documentos
```

Esse fluxo garante que todas as respostas estejam fundamentadas nas informações presentes na base de dados.

---

# 8. Organização dos Arquivos

Após a geração dos embeddings, a estrutura do projeto passa a incluir novos arquivos:

```text
data/
│
├── documentos.json
├── textos_processados.json
├── embeddings.npy
├── metadata.csv
└── indice_vetorial.pkl
```

Os arquivos de embeddings e do índice vetorial são utilizados durante as consultas realizadas pelo sistema.

---

# 9. Benefícios da Busca Semântica

A utilização de embeddings oferece diversas vantagens em relação à busca tradicional baseada em palavras-chave.

Entre elas destacam-se:

* Compreensão do contexto da pergunta.
* Localização de documentos semanticamente semelhantes.
* Maior precisão nos resultados.
* Redução de respostas irrelevantes.
* Melhor experiência para o usuário.

Esses benefícios tornam a pesquisa muito mais eficiente, especialmente em grandes volumes de documentos oficiais.

---

# 10. Resultado Obtido

Ao término desta etapa, o sistema possui:

* Todos os documentos convertidos em embeddings.
* Banco vetorial estruturado.
* Índice para busca rápida.
* Arquivos preparados para recuperação semântica.
* Arquitetura RAG totalmente funcional.

Essa infraestrutura permite responder perguntas em linguagem natural utilizando como base exclusivamente os documentos oficiais armazenados.

---

# 11. Conclusão

A implementação dos embeddings e da arquitetura RAG representa o núcleo inteligente do sistema.

Enquanto os embeddings possibilitam compreender o significado dos textos, o mecanismo RAG garante que as respostas sejam construídas com base em evidências extraídas diretamente do Diário Oficial.

Essa combinação proporciona consultas rápidas, precisas e confiáveis, tornando o sistema capaz de auxiliar usuários na localização de informações específicas sem a necessidade de leitura manual de milhares de documentos.
