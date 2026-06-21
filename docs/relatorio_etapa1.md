# Relatório da Etapa 1 – Coleta dos Dados

# Sistema Inteligente para Consulta ao Diário Oficial do Município de Avaré

---

# 1. Objetivo

A primeira etapa do desenvolvimento do sistema teve como objetivo realizar a coleta automatizada de todas as edições do Diário Oficial do Município de Avaré disponibilizadas pelo portal oficial.

Como a quantidade de documentos publicados é muito grande e distribuída ao longo de diversos anos, tornou-se inviável realizar esse processo manualmente. Dessa forma, foi desenvolvido um scraper em Python capaz de acessar automaticamente a API do Diário Oficial, recuperar os metadados das publicações e efetuar o download dos arquivos PDF correspondentes.

O resultado dessa etapa constitui a base de dados utilizada por todas as fases posteriores do projeto.

---

# 2. Tecnologias Utilizadas

Durante a implementação foram utilizadas as seguintes bibliotecas:

* Python 3
* Requests
* Pandas
* BeautifulSoup
* Concurrent Futures
* TQDM
* JSON
* OS

Cada biblioteca possui uma finalidade específica dentro do processo de coleta.

A biblioteca Requests realiza todas as requisições HTTP necessárias para comunicação com a API.

O BeautifulSoup interpreta páginas HTML quando necessário.

O Pandas organiza todos os metadados em tabelas estruturadas.

A biblioteca Concurrent Futures permite executar downloads em paralelo, reduzindo significativamente o tempo total de processamento.

Já o TQDM fornece barras de progresso durante a execução do programa.

---

# 3. Funcionamento Geral

Inicialmente o programa estabelece conexão com a API do Diário Oficial.

Em seguida são obtidas todas as publicações disponíveis para o município de Avaré.

Para cada publicação são extraídos diversos metadados importantes, incluindo:

* Identificador da publicação
* Data
* Ano
* Número da edição
* Quantidade de páginas
* Tipo do documento
* Secretaria responsável
* URL do PDF

Após essa etapa, todas as URLs são utilizadas para efetuar automaticamente o download dos documentos.

Os arquivos são armazenados localmente na pasta destinada aos PDFs.

---

# 4. Organização dos Arquivos

Após a execução do scraper a estrutura do projeto torna-se semelhante à seguinte:

```text
data/
│
├── pdfs/
│   ├── 2018/
│   ├── 2019/
│   ├── 2020/
│   ├── ...
│   └── 2026/
│
└── metadata.csv
```

Todos os PDFs ficam organizados por ano.

Além disso, um arquivo CSV contendo todos os metadados das publicações é gerado automaticamente.

Esse arquivo será utilizado pelas próximas etapas do projeto.

---

# 5. Download Paralelo

Uma das principais otimizações implementadas foi o download concorrente dos arquivos.

Ao invés de baixar um documento por vez, diversos downloads são executados simultaneamente utilizando múltiplas threads.

Essa estratégia reduz significativamente o tempo total de coleta dos documentos.

Durante os testes observou-se uma redução expressiva no tempo necessário para baixar milhares de arquivos.

---

# 6. Tratamento de Erros

Durante o processo de coleta podem ocorrer falhas temporárias na conexão ou indisponibilidade momentânea do servidor.

Para aumentar a robustez do sistema foram implementadas diversas estratégias de tratamento de erros:

* Tentativas automáticas de reconexão.
* Timeout para requisições lentas.
* Continuação da execução mesmo quando um arquivo específico apresenta erro.
* Registro das falhas em log.

Essas medidas garantem maior estabilidade durante a execução.

---

# 7. Resultado Obtido

Ao término desta etapa o sistema produz dois conjuntos principais de dados:

* Todos os arquivos PDF do Diário Oficial.
* Um banco de metadados estruturado em formato CSV.

Esses dados representam a matéria-prima utilizada para todas as etapas seguintes do projeto.

---

# 8. Conclusão

A etapa de coleta de dados constitui a base de todo o sistema desenvolvido.

A automatização do processo permitiu reunir milhares de documentos oficiais de forma rápida, organizada e confiável.

Além de eliminar a necessidade de downloads manuais, o scraper garante que novas publicações possam ser incorporadas ao sistema com facilidade, tornando possível manter a base de dados sempre atualizada.

Essa etapa fornece todos os documentos necessários para que as próximas fases realizem a extração do texto, geração dos embeddings e construção do sistema de busca inteligente baseado em Inteligência Artificial.
