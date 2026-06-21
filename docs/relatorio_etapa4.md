# Relatório da Etapa 4 – Desenvolvimento da Interface Web e Sistema de Consulta 

# Sistema Inteligente para Consulta ao Diário Oficial do Município de Avaré

---

# 1. Objetivo

A quarta e última etapa do projeto teve como objetivo desenvolver uma interface web intuitiva que permitisse aos usuários consultar o conteúdo do Diário Oficial do Município de Avaré utilizando linguagem natural.

Diferentemente dos mecanismos tradicionais de pesquisa, nos quais é necessário conhecer palavras-chave exatas, o sistema desenvolvido permite que o usuário formule perguntas de maneira semelhante a uma conversa, recebendo respostas fundamentadas nos documentos oficiais previamente processados.

Essa interface representa o ponto de interação entre o usuário e toda a infraestrutura construída nas etapas anteriores.

---

# 2. Tecnologias Utilizadas

Para o desenvolvimento da interface foram utilizadas as seguintes tecnologias:

* Python 3
* Streamlit
* Pandas
* PyTorch
* NumPy
* JSON
* Sentence Transformers

Cada biblioteca desempenha uma função específica.

O Streamlit foi utilizado para construir a interface gráfica, permitindo criar páginas web interativas de forma simples e eficiente. O Pandas organiza os resultados das pesquisas, enquanto o PyTorch e o modelo de embeddings são responsáveis pelo processamento das consultas.

---

# 3. Funcionamento Geral

Sempre que um usuário acessa o sistema, a interface realiza o carregamento dos modelos treinados e dos arquivos necessários para a pesquisa.

Quando uma pergunta é enviada, o sistema executa as seguintes etapas:

1. Recebe a pergunta digitada pelo usuário.
2. Converte a pergunta em um embedding.
3. Pesquisa os documentos mais semelhantes no banco vetorial.
4. Recupera os trechos mais relevantes.
5. Exibe os resultados encontrados juntamente com seus metadados.

Todo esse processo ocorre em poucos segundos.

---

# 4. Interface do Usuário

A interface foi desenvolvida buscando simplicidade e facilidade de utilização.

Os principais elementos presentes na aplicação são:

* Campo para digitação da pergunta.
* Botão de pesquisa.
* Filtros por ano.
* Filtros por tipo de documento.
* Área para exibição dos resultados.
* Expansão dos documentos encontrados.

Essa organização permite que usuários sem conhecimento técnico utilizem o sistema de forma intuitiva.

---

# 5. Sistema de Filtros

Além da busca em linguagem natural, a aplicação oferece filtros adicionais para restringir os resultados.

Entre eles destacam-se:

* Ano da publicação.
* Tipo do documento (Lei, Decreto, Portaria, Edital, etc.).
* Data da publicação.

Esses filtros auxiliam na localização rápida de documentos específicos e reduzem a quantidade de resultados exibidos.

---

# 6. Exibição dos Resultados

Após a pesquisa, os documentos encontrados são apresentados em uma lista organizada.

Cada resultado contém informações como:

* Número da publicação.
* Data.
* Tipo do ato.
* Secretaria responsável.
* Trecho mais relevante do documento.

O usuário pode expandir cada resultado para visualizar mais detalhes do conteúdo recuperado.

Essa abordagem facilita a leitura e evita a necessidade de abrir vários arquivos PDF manualmente.

---

# 7. Fluxo de Funcionamento

O funcionamento completo da aplicação pode ser representado pelo seguinte fluxo:

```text
Usuário
    │
    ▼
Interface Streamlit
    │
    ▼
Pergunta em Linguagem Natural
    │
    ▼
Modelo de Embeddings
    │
    ▼
Busca no Banco Vetorial
    │
    ▼
Recuperação dos Documentos
    │
    ▼
Exibição dos Resultados
```

Esse fluxo integra todas as etapas desenvolvidas ao longo do projeto.

---

# 8. Organização do Projeto

Ao final do desenvolvimento, a estrutura principal do sistema pode ser representada da seguinte forma:

```text
projeto-diario-avare/
│
├── data/
│   ├── pdfs/
│   ├── metadata.csv
│   ├── textos_processados.json
│   ├── embeddings.npy
│   └── indice_vetorial.pkl
│
├── src/
│   ├── scraper.py
│   ├── extract_text.py
│   ├── embeddings.py
│   ├── model.py
│   └── app.py
│
├── notebooks/
│
├── relatorios/
│   ├── relatorio_etapa1.md
│   ├── relatorio_etapa2.md
│   ├── relatorio_etapa3.md
│   └── relatorio_etapa4.md
│
└── README.md
```

Essa organização facilita a manutenção, a expansão do projeto e a compreensão da arquitetura por outros desenvolvedores.

---

# 9. Vantagens do Sistema

O sistema desenvolvido apresenta diversas vantagens em relação às formas tradicionais de consulta ao Diário Oficial:

* Pesquisa em linguagem natural.
* Busca baseada em significado (semântica).
* Respostas mais rápidas.
* Organização automática dos documentos.
* Interface simples e intuitiva.
* Facilidade para localizar leis, decretos e portarias.
* Escalabilidade para inclusão de novas publicações.

Essas características tornam a aplicação útil tanto para servidores públicos quanto para cidadãos interessados em consultar informações oficiais.

---

# 10. Resultados Obtidos

Ao final da implementação, o sistema foi capaz de:

* Coletar automaticamente milhares de documentos do Diário Oficial.
* Extrair e organizar o conteúdo textual.
* Gerar embeddings para todos os documentos.
* Implementar um mecanismo de busca semântica utilizando arquitetura RAG.
* Disponibilizar uma interface web para consultas em linguagem natural.
* Permitir filtragem por ano, data e tipo de documento.
* Exibir respostas fundamentadas em documentos oficiais.

Os testes realizados demonstraram que o sistema consegue localizar rapidamente informações relevantes mesmo quando a pergunta do usuário utiliza palavras diferentes das presentes nos documentos.

---

# 11. Conclusão

A interface web desenvolvida representa a etapa final do projeto e integra todas as funcionalidades implementadas anteriormente.

Por meio da combinação entre técnicas de Processamento de Linguagem Natural, embeddings, busca vetorial e arquitetura RAG, foi possível construir um sistema inteligente capaz de facilitar o acesso às informações publicadas no Diário Oficial do Município de Avaré.

O projeto demonstra como tecnologias modernas de Inteligência Artificial podem ser aplicadas para melhorar o acesso à informação pública, proporcionando consultas mais rápidas, precisas e acessíveis.

Além de atender aos objetivos propostos, a arquitetura desenvolvida permite futuras expansões, como a integração com modelos de linguagem mais avançados, atualização automática das publicações e disponibilização da aplicação em ambiente de produção para uso contínuo.
