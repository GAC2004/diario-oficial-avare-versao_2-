# Relatório da Etapa 2 – Extração e Processamento dos Textos 

# Sistema Inteligente para Consulta ao Diário Oficial do Município de Avaré

---

# 1. Objetivo

Após a coleta dos arquivos PDF realizada na etapa anterior, foi necessário transformar esses documentos em texto para que pudessem ser utilizados por algoritmos de Inteligência Artificial.

Os modelos de linguagem e de busca semântica trabalham sobre textos e não diretamente sobre arquivos PDF. Assim, esta etapa teve como objetivo extrair todo o conteúdo textual das publicações, realizar a limpeza dos dados e organizar as informações em um formato estruturado.

O resultado é uma base textual pronta para a geração dos embeddings e para a implementação do sistema de Recuperação Aumentada por Geração (RAG).

---

# 2. Tecnologias Utilizadas

As principais bibliotecas utilizadas nesta etapa foram:

* Python 3
* PyMuPDF (fitz)
* Pandas
* JSON
* OS
* TQDM
* Regex (re)

Cada ferramenta possui uma função específica no processo.

O PyMuPDF é responsável por abrir os arquivos PDF e extrair o conteúdo textual de cada página. O Pandas organiza os dados em tabelas estruturadas, enquanto o módulo `re` é utilizado para realizar a limpeza do texto por meio de expressões regulares. O TQDM fornece barras de progresso durante a execução.

---

# 3. Processo de Extração

Inicialmente o programa percorre todos os arquivos PDF armazenados na etapa anterior.

Para cada documento são executadas as seguintes operações:

1. Abertura do arquivo PDF.
2. Leitura de todas as páginas.
3. Extração do texto de cada página.
4. Concatenação do conteúdo em um único texto.
5. Associação do texto aos metadados da publicação.

Ao final do processo, cada edição do Diário Oficial passa a possuir um registro contendo tanto suas informações de identificação quanto seu conteúdo textual.

---

# 4. Limpeza dos Dados

Os textos extraídos diretamente dos PDFs podem conter elementos que dificultam a busca semântica, como espaços duplicados, quebras de linha excessivas, caracteres especiais e símbolos desnecessários.

Para melhorar a qualidade dos dados, foi implementado um processo de pré-processamento que realiza:

* Remoção de espaços repetidos.
* Padronização das quebras de linha.
* Eliminação de caracteres inválidos.
* Normalização do texto.
* Organização da estrutura textual.

Essas etapas tornam o conteúdo mais adequado para o processamento por modelos de linguagem.

---

# 5. Estrutura dos Dados

Após a extração, cada documento passa a conter informações semelhantes ao exemplo abaixo:

```json
{
  "id": 831975,
  "data": "2026-06-15",
  "ano": 2026,
  "tipo": "Lei",
  "secretaria": "Administração",
  "texto": "Conteúdo completo extraído do Diário Oficial..."
}
```

Essa estrutura facilita o acesso às informações durante as próximas etapas do projeto.

---

# 6. Organização dos Arquivos

Ao término da execução, os dados processados ficam organizados da seguinte forma:

```text
data/
│
├── pdfs/
├── metadata.csv
├── documentos.json
└── textos_processados.json
```

O arquivo `textos_processados.json` contém o texto completo de cada documento juntamente com seus metadados.

Essa organização simplifica o carregamento das informações pelo sistema de busca.

---

# 7. Tratamento de Exceções

Durante a leitura dos arquivos PDF podem ocorrer problemas, como:

* Arquivos corrompidos.
* PDFs protegidos.
* Páginas sem texto.
* Falhas de leitura.

Para evitar interrupções na execução, o sistema implementa tratamento de exceções, registrando os erros encontrados e continuando o processamento dos demais documentos.

Essa abordagem aumenta a confiabilidade do sistema e reduz a necessidade de intervenção manual.

---

# 8. Preparação para Embeddings

Após a limpeza e organização dos textos, os documentos encontram-se prontos para a próxima etapa do projeto: a geração dos embeddings.

Os embeddings representam cada texto por meio de vetores numéricos capazes de capturar seu significado semântico. Esses vetores permitirão realizar buscas inteligentes mesmo quando a consulta do usuário não utilizar exatamente as mesmas palavras presentes nos documentos.

---

# 9. Resultado Obtido

Ao final desta etapa, o sistema produz uma base textual estruturada contendo:

* Texto completo de todas as publicações.
* Metadados associados a cada documento.
* Arquivos organizados para processamento posterior.
* Conteúdo preparado para geração de embeddings.

Essa base representa a principal fonte de conhecimento utilizada pelo sistema de Inteligência Artificial.

---

# 10. Conclusão

A etapa de extração e processamento dos textos transforma documentos em formato PDF em uma base textual organizada e padronizada.

Esse processo é fundamental para que os algoritmos de busca semântica possam compreender o conteúdo das publicações e responder perguntas de forma precisa.

Com os textos devidamente tratados, o sistema encontra-se preparado para gerar embeddings e construir um mecanismo eficiente de recuperação de informações baseado em Inteligência Artificial.
