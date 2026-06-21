---

# 📘 Diário Oficial Inteligente de Avaré

Projeto Final da disciplina **Redes Neurais e IA Aplicada**, desenvolvido na **Faculdade de Engenharia e Administração Paulista de Avaré (FEAP)**.

🎓 **Curso:** Bacharelado em Engenharia da Computação

---

# 👨‍🏫 Professor Responsável

**Prof. Fernando Oliveira**

---

# 👥 Equipe

- Gabriela Arruda Carriel
- Stela Veiga Monteiro
- José Leonardo Pereira dos Santos
- Maria Júlia da Costa Teixeira
- Enzo Fortes
- Yehudi Witzel de Oliveira

---

# Como Executar o Sistema

## O que é este projeto

Este projeto utiliza Inteligência Artificial para coletar, processar e classificar publicações do Diário Oficial do Município de Avaré. O sistema realiza automaticamente a coleta das edições, extrai o texto dos documentos PDF, treina um modelo de classificação e disponibiliza uma interface web para pesquisa e consulta dos atos oficiais.

---

# Requisitos

Antes de executar o projeto, verifique se possui instalado:

* Python 3.11
* Git
* Pip
* Ambiente virtual (venv)

Caso ainda não possua o Python instalado, faça o download em:

https://www.python.org/downloads/release/python-3119/

---

# 1. Clonar o projeto

Abra o terminal e execute:

```bash
git clone https://github.com/GAC2004/diario-oficial-avare-versao_2
```

Depois entre na pasta do projeto:

```bash
cd projeto-diario-avare
```

---

# 2. Criar o ambiente virtual

Windows

```bash
python -m venv venv
```

Linux/Mac

```bash
python3 -m venv venv
```

---

# 3. Ativar o ambiente virtual

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

Quando estiver ativo aparecerá algo semelhante a:

```
(venv)
```

no início do terminal.

---

# 4. Instalar as dependências

Execute:

```bash
pip install -r requirements.txt
```

A instalação pode demorar alguns minutos dependendo da velocidade da internet.

---

# 5. Coletar os dados

Execute o scraper responsável por baixar as publicações do Diário Oficial.

```bash
python src/scraper.py
```

Ao final será criado o dataset contendo todas as publicações encontradas.

---

# 6. Extrair o texto dos PDFs

Depois execute:

```bash
python src/extract_text.py
```

Este script realiza:

* leitura dos PDFs;
* extração do texto;
* limpeza dos dados;
* preparação para treinamento.

---

# 7. Treinar o modelo

Com os textos preparados execute:

```bash
python src/train.py
```

O treinamento irá gerar os arquivos do modelo utilizados posteriormente pela aplicação.

---

# 8. Executar a aplicação

Inicie o sistema:

```bash
streamlit run src/app.py
```

O navegador abrirá automaticamente.

Caso isso não aconteça, acesse:

```
http://localhost:8501
```

---

# Como utilizar

A aplicação permite pesquisar e classificar documentos do Diário Oficial.

É possível:

* pesquisar palavras-chave;
* selecionar o ano da publicação;
* selecionar o tipo do ato;
* visualizar o texto extraído;
* verificar a categoria prevista pelo modelo;
* consultar a probabilidade da classificação.

---

# Estrutura do projeto

```
projeto-diario-avare/

│

├── src/

│   ├── scraper.py

│   ├── extract_text.py

│   ├── train.py

│   ├── dataset.py

│   ├── model.py

│   └── app.py

│

├── data/

├── models/

├── docs/

├── notebooks/

├── requirements.txt

└── README.md
```

---

# Encerrando o sistema

Para finalizar a aplicação pressione:

```
CTRL + C
```

no terminal.

---

# Problemas comuns

## Python não reconhecido

Verifique se o Python foi instalado corretamente e adicionado ao PATH.

---

## Ambiente virtual não ativa

No Windows PowerShell execute:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Depois tente ativar novamente o ambiente virtual.

---

## Erro de bibliotecas

Execute novamente:

```bash
pip install -r requirements.txt
```

---

## Aplicação não abre

Verifique se o comando

```bash
streamlit run src/app.py
```

foi executado sem erros.

---

## Erro ao encontrar arquivos

Confira se a estrutura das pastas do projeto permanece igual à do repositório original.

# Licença

Projeto desenvolvido exclusivamente para fins acadêmicos na disciplina de Inteligência Artificial.
