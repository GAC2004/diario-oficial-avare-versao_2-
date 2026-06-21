"""
app.py - Interface web para o Diario Oficial de Avare.
Execute: python src/app.py
Acessa:  http://127.0.0.1:5000
"""

import sys
import threading
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from flask import Flask, request, jsonify
from rag import DiarioOficialRAG
import scraper
import extractor
import embedder

app = Flask(__name__)
rag = DiarioOficialRAG()

# Estado global do pipeline de atualizacao (roda em thread separada)
pipeline_status = {
    "running":  False,
    "log":      [],
    "done":     False,
}
pipeline_lock = threading.Lock()


def _log(msg: str):
    with pipeline_lock:
        pipeline_status["log"].append(msg)
    print(msg)


def run_pipeline():
    """Executa scraper -> extractor -> embedder (incremental) e recarrega o RAG."""
    with pipeline_lock:
        pipeline_status["running"] = True
        pipeline_status["done"]    = False
        pipeline_status["log"]     = []

    try:
        _log("Etapa 1/3 — Verificando novas edicoes no Diario Oficial...")
        scraper.run_scraper()
        _log("Etapa 1/3 concluida.")

        _log("Etapa 2/3 — Extraindo texto dos PDFs novos...")
        extractor.run_extractor()
        _log("Etapa 2/3 concluida.")

        _log("Etapa 3/3 — Atualizando indice vetorial (embeddings)...")
        result = embedder.update_index()
        if result:
            _log(f"Etapa 3/3 concluida — {result.get('novos_documentos', 0)} novo(s) "
                 f"documento(s), {result.get('novos_chunks', 0)} novo(s) trecho(s).")
        else:
            _log("Etapa 3/3 concluida.")

        rag.reload()
        _log("Base de dados atualizada e recarregada com sucesso!")

    except Exception as e:
        _log(f"ERRO: {e}")

    finally:
        with pipeline_lock:
            pipeline_status["running"] = False
            pipeline_status["done"]    = True


HTML = """<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Diario Oficial de Avare — Consulta Inteligente</title>
<style>
  :root {
    --bg:        #f1f3f6;
    --card:      #ffffff;
    --primary:   #1d3557;
    --primary-2: #2a4a76;
    --accent:    #2a9d8f;
    --text:      #1f2933;
    --muted:     #6b7785;
    --border:    #e1e5ea;
    --radius:    10px;
  }

  * { box-sizing: border-box; }

  body {
    margin: 0;
    font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
  }

  header {
    background: var(--primary);
    color: white;
    padding: 22px 32px;
  }

  header h1 {
    margin: 0;
    font-size: 22px;
    font-weight: 600;
  }

  header p {
    margin: 4px 0 0;
    font-size: 13px;
    opacity: 0.8;
  }

  .layout {
    display: grid;
    grid-template-columns: 280px 1fr;
    gap: 24px;
    max-width: 1200px;
    margin: 24px auto;
    padding: 0 20px;
  }

  @media (max-width: 880px) {
    .layout { grid-template-columns: 1fr; }
  }

  .card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 18px 20px;
    margin-bottom: 20px;
  }

  .card h2, .card h3 {
    margin-top: 0;
    font-size: 15px;
    color: var(--primary);
  }

  .stat-row {
    display: flex;
    justify-content: space-between;
    font-size: 13px;
    padding: 6px 0;
    border-bottom: 1px solid var(--border);
  }
  .stat-row:last-child { border-bottom: none; }
  .stat-row span:last-child { font-weight: 600; color: var(--primary); }

  textarea, select, input[type=text] {
    width: 100%;
    padding: 10px 12px;
    font-size: 14px;
    border: 1px solid var(--border);
    border-radius: 6px;
    font-family: inherit;
    background: #fff;
  }

  textarea { resize: vertical; }

  label {
    display: block;
    font-size: 12px;
    color: var(--muted);
    margin: 10px 0 4px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.03em;
  }

  .filtros {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }

  button {
    border: none;
    border-radius: 6px;
    padding: 10px 22px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: opacity 0.15s;
  }
  button:hover { opacity: 0.88; }
  button:disabled { opacity: 0.5; cursor: not-allowed; }

  .btn-primary { background: var(--primary); color: white; }
  .btn-accent  { background: var(--accent); color: white; }
  .btn-ghost   { background: var(--border); color: var(--text); }

  .exemplos { margin-top: 12px; display: flex; flex-wrap: wrap; gap: 6px; }
  .ex {
    background: #eef2f6; color: var(--primary-2);
    border: 1px solid var(--border);
    padding: 6px 12px; border-radius: 20px; font-size: 12px;
    cursor: pointer; font-weight: 500;
  }
  .ex:hover { background: #dde6ef; }

  .trecho {
    background: var(--card);
    border: 1px solid var(--border);
    border-left: 5px solid var(--accent);
    border-radius: var(--radius);
    padding: 16px 18px;
    margin-bottom: 14px;
  }

  .trecho-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 10px;
    font-size: 13px;
    color: var(--muted);
  }

  .badge {
    background: var(--accent);
    color: white;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 12px;
    font-weight: 700;
  }

  .trecho-fonte { font-weight: 600; color: var(--primary); }

  .trecho-texto {
    white-space: pre-wrap;
    font-size: 14px;
    line-height: 1.7;
    color: var(--text);
  }

  .fontes-box {
    background: #eef6f5;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 14px 18px;
    font-size: 13px;
    color: var(--muted);
    line-height: 1.6;
  }

  .loading, .empty {
    color: var(--muted);
    font-style: italic;
    padding: 30px;
    text-align: center;
  }

  .pipeline-log {
    background: #0d1b2a;
    color: #9fe6d4;
    font-family: "Consolas", monospace;
    font-size: 12px;
    border-radius: 6px;
    padding: 10px 12px;
    max-height: 180px;
    overflow-y: auto;
    margin-top: 10px;
    display: none;
    line-height: 1.5;
  }

  .status-dot {
    display: inline-block;
    width: 9px; height: 9px;
    border-radius: 50%;
    background: #ccc;
    margin-right: 6px;
  }
  .status-dot.on { background: #2a9d8f; }
</style>
</head>
<body>

<header>
  <h1>Diario Oficial de Avare — Consulta Inteligente</h1>
  <p>Busca semantica sobre publicacoes oficiais do municipio (2018–2026)</p>
</header>

<div class="layout">

  <!-- SIDEBAR -->
  <div>
    <div class="card">
      <h2>Estatisticas da Base</h2>
      <div class="stat-row"><span>Documentos</span><span id="st-docs">-</span></div>
      <div class="stat-row"><span>Trechos indexados</span><span id="st-chunks">-</span></div>
      <div class="stat-row"><span>Periodo inicial</span><span id="st-inicio">-</span></div>
      <div class="stat-row"><span>Periodo final</span><span id="st-fim">-</span></div>
    </div>

    <div class="card">
      <h2>Atualizar Base de Dados</h2>
      <p style="font-size:13px; color:var(--muted); margin-top:0;">
        Verifica novas edicoes no Diario Oficial, extrai o texto e
        atualiza o indice de busca automaticamente.
      </p>
      <button id="btn-pipeline" class="btn-accent" onclick="iniciarPipeline()">
        <span class="status-dot" id="pipeline-dot"></span>Atualizar agora
      </button>
      <div class="pipeline-log" id="pipeline-log"></div>
    </div>
  </div>

  <!-- MAIN -->
  <div>
    <div class="card">
      <h2>Pergunte sobre o Diario Oficial</h2>

      <textarea id="pergunta" rows="3" placeholder="Ex: Quais decretos foram publicados em maio de 2026?"></textarea>

      <div class="filtros">
        <div>
          <label>Ano</label>
          <select id="filtro-ano">
            <option value="">Todos</option>
          </select>
        </div>
        <div>
          <label>Mes</label>
          <select id="filtro-mes">
            <option value="">Todos</option>
            <option value="01">Janeiro</option>
            <option value="02">Fevereiro</option>
            <option value="03">Marco</option>
            <option value="04">Abril</option>
            <option value="05">Maio</option>
            <option value="06">Junho</option>
            <option value="07">Julho</option>
            <option value="08">Agosto</option>
            <option value="09">Setembro</option>
            <option value="10">Outubro</option>
            <option value="11">Novembro</option>
            <option value="12">Dezembro</option>
          </select>
        </div>
      </div>

      <label>Numero de resultados</label>
      <select id="filtro-topk">
        <option value="5">5</option>
        <option value="8">8</option>
        <option value="10">10</option>
        <option value="15">15</option>
      </select>

      <div style="margin-top:14px;">
        <button class="btn-primary" onclick="consultar()">Consultar</button>
        <button class="btn-ghost" onclick="limpar()">Limpar</button>
      </div>

      <div class="exemplos">
        <span class="ex" onclick="setar('Quais decretos foram publicados?')">Decretos</span>
        <span class="ex" onclick="setar('Houve contratacao ou admissao de pessoal?')">Contratacoes</span>
        <span class="ex" onclick="setar('Quais portarias foram emitidas?')">Portarias</span>
        <span class="ex" onclick="setar('Quais licitacoes foram publicadas?')">Licitacoes</span>
        <span class="ex" onclick="setar('Quais servidores foram convocados para pericia medica?')">Pericias medicas</span>
      </div>
    </div>

    <div id="resultado"></div>
  </div>

</div>

<script>
function setar(texto) {
  document.getElementById('pergunta').value = texto;
}

function limpar() {
  document.getElementById('pergunta').value = '';
  document.getElementById('filtro-ano').value = '';
  document.getElementById('filtro-mes').value = '';
  document.getElementById('resultado').innerHTML = '';
}

function carregarStats() {
  fetch('/stats').then(r => r.json()).then(data => {
    document.getElementById('st-docs').textContent   = data.total_docs;
    document.getElementById('st-chunks').textContent = data.total_chunks;
    document.getElementById('st-inicio').textContent = data.periodo_inicio;
    document.getElementById('st-fim').textContent    = data.periodo_fim;

    const sel = document.getElementById('filtro-ano');
    sel.innerHTML = '<option value="">Todos</option>';
    data.anos.forEach(ano => {
      const opt = document.createElement('option');
      opt.value = ano;
      opt.textContent = ano;
      sel.appendChild(opt);
    });
  });
}

function consultar() {
  const pergunta = document.getElementById('pergunta').value.trim();
  if (!pergunta) { alert('Digite uma pergunta.'); return; }

  const ano   = document.getElementById('filtro-ano').value;
  const mesNum = document.getElementById('filtro-mes').value;
  const topk  = document.getElementById('filtro-topk').value;

  let mes = null;
  if (ano && mesNum) mes = ano + '-' + mesNum;

  const div = document.getElementById('resultado');
  div.innerHTML = '<div class="card loading">Buscando trechos relevantes...</div>';

  fetch('/consultar', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({pergunta: pergunta, ano: ano || null, mes: mes, top_k: parseInt(topk)})
  })
  .then(r => r.json())
  .then(data => {
    if (!data.trechos || data.trechos.length === 0) {
      div.innerHTML = '<div class="card empty">Nenhum resultado encontrado para os filtros aplicados.</div>';
      return;
    }

    let html = '';
    data.trechos.forEach((t, i) => {
      const score = Math.round(t.score * 100);
      html += `<div class="trecho">
        <div class="trecho-header">
          <span class="trecho-fonte">Trecho ${i+1} — ${t.source}</span>
          <span><span class="badge">${score}% relevancia</span> &nbsp; periodo ${t.date}</span>
        </div>
        <div class="trecho-texto">${t.text}</div>
      </div>`;
    });

    if (data.sources && data.sources.length > 0) {
      html += `<div class="fontes-box"><strong>Documentos consultados:</strong><br>${data.sources.join('<br>')}</div>`;
    }

    div.innerHTML = html;
  })
  .catch(() => {
    div.innerHTML = '<div class="card empty">Erro ao consultar. Verifique se o servidor esta rodando.</div>';
  });
}

document.getElementById('pergunta').addEventListener('keydown', function(e) {
  if (e.ctrlKey && e.key === 'Enter') consultar();
});

// ---- Pipeline de atualizacao ----
let pipelineInterval = null;

function iniciarPipeline() {
  const btn = document.getElementById('btn-pipeline');
  const log = document.getElementById('pipeline-log');
  const dot = document.getElementById('pipeline-dot');

  btn.disabled = true;
  dot.classList.add('on');
  log.style.display = 'block';
  log.textContent = 'Iniciando atualizacao...\\n';

  fetch('/pipeline/start', {method: 'POST'}).then(() => {
    pipelineInterval = setInterval(verificarPipeline, 1500);
  });
}

function verificarPipeline() {
  fetch('/pipeline/status').then(r => r.json()).then(data => {
    const log = document.getElementById('pipeline-log');
    log.textContent = data.log.join('\\n');
    log.scrollTop = log.scrollHeight;

    if (!data.running && data.done) {
      clearInterval(pipelineInterval);
      document.getElementById('btn-pipeline').disabled = false;
      document.getElementById('pipeline-dot').classList.remove('on');
      carregarStats();
    }
  });
}

carregarStats();
</script>
</body>
</html>"""


@app.route("/")
def index():
    return HTML


@app.route("/stats")
def stats():
    return jsonify(rag.stats())


@app.route("/consultar", methods=["POST"])
def consultar():
    data     = request.get_json()
    pergunta = data.get("pergunta", "").strip()
    ano      = data.get("ano") or None
    mes      = data.get("mes") or None
    top_k    = int(data.get("top_k", 5))

    if not pergunta:
        return jsonify({"trechos": [], "sources": []})

    result = rag.ask(pergunta, top_k=top_k, ano=ano, mes=mes)
    return jsonify(result)


@app.route("/pipeline/start", methods=["POST"])
def pipeline_start():
    with pipeline_lock:
        if pipeline_status["running"]:
            return jsonify({"started": False, "reason": "ja em execucao"})

    thread = threading.Thread(target=run_pipeline, daemon=True)
    thread.start()
    return jsonify({"started": True})


@app.route("/pipeline/status")
def pipeline_status_route():
    with pipeline_lock:
        return jsonify(dict(pipeline_status))


if __name__ == "__main__":
    print("\n Acesse: http://127.0.0.1:5000\n")
    app.run(host="127.0.0.1", port=5000, debug=False)