#!/usr/bin/env python3
"""Claude Code 会话管理器 - Web UI 版本（无需任何外部依赖）"""

import os, json, shutil, threading, webbrowser, time
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from urllib.parse import urlparse, parse_qs

SESSION_DIR = (
    r"C:\Users\Administrator\AppData\Local\Claude-3p"
    r"\local-agent-mode-sessions"
    r"\4687dffc-7800-4f07-91b8-12da0c913ee0"
    r"\00000000-0000-4000-8000-000000000001"
)

# ── 数据层 ──────────────────────────────────────────────────────
def ts_to_str(ms):
    try: return datetime.fromtimestamp(ms/1000).strftime("%Y-%m-%d %H:%M")
    except: return "—"

def read_audit(folder_path):
    """从 audit.jsonl 中读取消息数量和第一条用户消息内容"""
    audit = os.path.join(folder_path, "audit.jsonl")
    u = a = 0
    first_msg = ""
    if not os.path.isfile(audit):
        return u, a, first_msg
    try:
        with open(audit, "r", encoding="utf-8") as f:
            for line in f:
                entry = json.loads(line)
                t = entry.get("type", "")
                if t == "user":
                    u += 1
                    if not first_msg:
                        content = entry.get("message", {}).get("content", "")
                        if isinstance(content, list):
                            parts = [blk.get("text","") for blk in content
                                     if isinstance(blk, dict) and blk.get("type")=="text"]
                            content = " ".join(parts)
                        first_msg = str(content).replace("\n", " ").strip()
                elif t == "assistant":
                    a += 1
    except:
        pass
    return u, a, first_msg

def load_sessions():
    sessions = []
    if not os.path.isdir(SESSION_DIR): return sessions
    for fname in os.listdir(SESSION_DIR):
        if not (fname.startswith("local_") and fname.endswith(".json")): continue
        jp = os.path.join(SESSION_DIR, fname)
        fp = os.path.join(SESSION_DIR, fname[:-5])
        try:
            with open(jp, "r", encoding="utf-8") as f: d = json.load(f)
        except: d = {}
        u, a, first_msg = read_audit(fp)
        # audit.jsonl 是最准确的来源；若文件夹不存在则回退到 JSON 里的 initialMessage
        if not first_msg:
            first_msg = (d.get("initialMessage") or "").replace("\n", " ").strip()
        sessions.append({
            "id":         fname[:-5],
            "json_path":  jp,
            "folder_path":fp,
            "has_folder": os.path.isdir(fp),
            "title":      d.get("title") or d.get("processName") or "（无标题）",
            "init_msg":   first_msg,
            "model":      d.get("model","—"),
            "time_ms":    d.get("lastActivityAt") or d.get("createdAt") or 0,
            "time_str":   ts_to_str(d.get("lastActivityAt") or d.get("createdAt") or 0),
            "archived":   d.get("isArchived", False),
            "user_msgs":  u,
            "asst_msgs":  a,
        })
    sessions.sort(key=lambda s: s["time_ms"], reverse=True)
    return sessions

def delete_sessions(ids):
    results = []
    for sid in ids:
        jp = os.path.join(SESSION_DIR, sid + ".json")
        fp = os.path.join(SESSION_DIR, sid)
        try:
            if os.path.isfile(jp): os.remove(jp)
            if os.path.isdir(fp):  shutil.rmtree(fp)
            results.append({"id": sid, "ok": True})
        except Exception as e:
            results.append({"id": sid, "ok": False, "error": str(e)})
    return results

def restart_claude():
    """关闭所有 Claude Code 进程并重新启动"""
    import subprocess, sys
    try:
        # 先结束所有 Claude 进程
        subprocess.run(
            ["taskkill", "/F", "/IM", "claude.exe", "/T"],
            capture_output=True
        )
        # 稍等一下确保进程完全退出
        time.sleep(1.2)
        # 重新启动 Claude Code（从 PATH 或常见安装位置查找）
        claude_paths = [
            r"D:\WindowsApps\Claude_1.8555.2.0_x64__pzs8sxrjxfjjc\app\claude.exe",
            r"C:\Users\Administrator\AppData\Local\Programs\claude\claude.exe",
            r"C:\Program Files\claude\claude.exe",
            "claude",
        ]
        launched = False
        for p in claude_paths:
            try:
                subprocess.Popen([p], shell=(p == "claude"))
                launched = True
                break
            except FileNotFoundError:
                continue
        return {"ok": True, "launched": launched}
    except Exception as e:
        return {"ok": False, "error": str(e)}

# ── HTML 界面 ───────────────────────────────────────────────────
HTML = r"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Claude Session Manager</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {
  --bg:       #0D0D14;
  --surface:  #13131F;
  --card:     #18182A;
  --border:   #252535;
  --accent:   #7C6CFF;
  --accent2:  #A99DFF;
  --danger:   #FF5C6A;
  --success:  #3ECF8E;
  --warn:     #F5A623;
  --text:     #E8E8F0;
  --muted:    #6B6B88;
  --arch-bg:  #1A1A28;
  --arch-txt: #55556A;
  --mono:     'JetBrains Mono', monospace;
  --sans:     'DM Sans', sans-serif;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; font-family: var(--sans); background: var(--bg); color: var(--text); overflow: hidden; }

/* ── Layout ── */
.app { display: grid; grid-template-columns: 220px 1fr; height: 100vh; }

/* ── Sidebar ── */
.sidebar {
  background: var(--surface);
  border-right: 1px solid var(--border);
  display: flex; flex-direction: column;
  padding: 28px 0 20px;
}
.logo { padding: 0 22px 28px; border-bottom: 1px solid var(--border); }
.logo-title {
  font-size: 11px; font-weight: 600; letter-spacing: 0.12em;
  color: var(--accent2); text-transform: uppercase; margin-bottom: 4px;
}
.logo-sub { font-size: 18px; font-weight: 600; color: var(--text); line-height: 1.2; }

.stats { padding: 20px 16px; display: flex; flex-direction: column; gap: 8px; }
.stat-card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 10px; padding: 12px 14px;
  display: flex; align-items: center; gap: 12px;
  cursor: pointer; transition: border-color .2s;
}
.stat-card:hover { border-color: var(--accent); }
.stat-card.active-filter { border-color: var(--accent); background: #1e1e38; }
.stat-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.stat-dot.all  { background: var(--accent2); }
.stat-dot.live { background: var(--success); }
.stat-dot.arch { background: var(--muted); }
.stat-num  { font-size: 22px; font-weight: 600; line-height: 1; }
.stat-label{ font-size: 11px; color: var(--muted); margin-top: 1px; }

.sidebar-actions { margin-top: auto; padding: 0 12px; display: flex; flex-direction: column; gap: 6px; }
.btn-side {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 14px; border-radius: 8px; border: none;
  font-family: var(--sans); font-size: 13px; font-weight: 500;
  cursor: pointer; transition: background .15s, color .15s; text-align: left; width: 100%;
}
.btn-side.refresh { background: var(--card); color: var(--text); }
.btn-side.refresh:hover { background: var(--border); }
.btn-side.delete-sel { background: rgba(255,92,106,.12); color: var(--danger); }
.btn-side.delete-sel:hover { background: rgba(255,92,106,.22); }
.btn-side.delete-all { background: transparent; color: var(--muted); }
.btn-side.delete-all:hover { background: var(--card); color: var(--text); }
.btn-icon { font-size: 15px; }

/* ── Main ── */
.main { display: flex; flex-direction: column; overflow: hidden; }

.topbar {
  background: var(--surface); border-bottom: 1px solid var(--border);
  padding: 14px 24px; display: flex; align-items: center; gap: 14px; flex-shrink: 0;
}
.search-wrap {
  flex: 1; display: flex; align-items: center; gap: 10px;
  background: var(--card); border: 1px solid var(--border);
  border-radius: 8px; padding: 8px 14px;
  transition: border-color .2s;
}
.search-wrap:focus-within { border-color: var(--accent); }
.search-icon { color: var(--muted); font-size: 14px; }
.search-input {
  flex: 1; background: none; border: none; outline: none;
  font-family: var(--sans); font-size: 13px; color: var(--text);
}
.search-input::placeholder { color: var(--muted); }
.sel-info {
  font-size: 12px; color: var(--muted); white-space: nowrap;
  font-family: var(--mono); min-width: 80px; text-align: right;
}

/* ── Table ── */
.table-wrap { flex: 1; overflow-y: auto; padding: 16px 24px 80px; }
.table-wrap::-webkit-scrollbar { width: 6px; }
.table-wrap::-webkit-scrollbar-track { background: transparent; }
.table-wrap::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

table { width: 100%; border-collapse: collapse; }
thead th {
  text-align: left; font-size: 10px; font-weight: 600;
  letter-spacing: .1em; text-transform: uppercase; color: var(--muted);
  padding: 0 12px 10px; position: sticky; top: 0; background: var(--bg); z-index: 1;
}
th:first-child { padding-left: 0; width: 36px; }

tbody tr {
  border-radius: 8px; cursor: pointer;
  transition: background .12s;
}
tbody tr:hover td { background: var(--card); }
tbody tr.selected td { background: #1e1e38; }
tbody tr.archived { opacity: .55; }
tbody tr.archived:hover { opacity: .75; }

td {
  padding: 10px 12px; font-size: 13px;
  border-bottom: 1px solid rgba(255,255,255,.035);
  vertical-align: middle;
}
td:first-child { padding-left: 0; width: 36px; }

.cb { width: 16px; height: 16px; accent-color: var(--accent); cursor: pointer; }

.badge {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 2px 8px; border-radius: 20px;
  font-size: 10px; font-weight: 600; letter-spacing: .04em;
  white-space: nowrap;
}
.badge.live { background: rgba(62,207,142,.15); color: var(--success); }
.badge.arch { background: rgba(107,107,136,.15); color: var(--muted); }

.time-cell { font-family: var(--mono); font-size: 11px; color: var(--muted); white-space: nowrap; }
.title-cell { font-weight: 500; max-width: 180px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.init-cell  { color: var(--muted); font-size: 12px; max-width: 340px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.msgs-cell  { font-family: var(--mono); font-size: 12px; color: var(--accent2); text-align: center; }
.model-cell { font-family: var(--mono); font-size: 11px; color: var(--muted); max-width: 160px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.folder-cell { text-align: center; font-size: 13px; }

/* ── Status bar ── */
.statusbar {
  position: fixed; bottom: 0; right: 0;
  width: calc(100vw - 220px);
  background: var(--surface); border-top: 1px solid var(--border);
  padding: 8px 24px; font-size: 11px; color: var(--muted);
  display: flex; align-items: center; gap: 20px; font-family: var(--mono);
}
.status-ok   { color: var(--success); }
.status-err  { color: var(--danger); }
kbd {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 4px; padding: 1px 5px; font-size: 10px; color: var(--muted);
}

/* ── Modal ── */
.overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,.7);
  backdrop-filter: blur(6px);
  display: flex; align-items: center; justify-content: center;
  z-index: 100; opacity: 0; pointer-events: none;
  transition: opacity .2s;
}
.overlay.show { opacity: 1; pointer-events: all; }
.modal {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 16px; width: 480px; max-width: 90vw;
  overflow: hidden;
  transform: scale(.95); transition: transform .2s;
}
.overlay.show .modal { transform: scale(1); }
.modal-header {
  background: linear-gradient(135deg, rgba(255,92,106,.2), rgba(255,92,106,.05));
  border-bottom: 1px solid rgba(255,92,106,.2);
  padding: 20px 24px;
  display: flex; align-items: center; gap: 12px;
}
.modal-icon { font-size: 22px; }
.modal-title { font-size: 16px; font-weight: 600; }
.modal-subtitle { font-size: 12px; color: var(--muted); margin-top: 2px; }
.modal-body { padding: 20px 24px; }
.modal-list {
  max-height: 240px; overflow-y: auto;
  background: var(--bg); border: 1px solid var(--border);
  border-radius: 8px; margin-bottom: 16px;
}
.modal-list::-webkit-scrollbar { width: 4px; }
.modal-list::-webkit-scrollbar-thumb { background: var(--border); }
.modal-item {
  display: flex; align-items: flex-start; gap: 10px;
  padding: 10px 14px; border-bottom: 1px solid var(--border);
}
.modal-item:last-child { border-bottom: none; }
.modal-item-icon { font-size: 14px; margin-top: 1px; flex-shrink: 0; }
.modal-item-title { font-size: 13px; font-weight: 500; }
.modal-item-sub   { font-size: 11px; color: var(--muted); font-family: var(--mono); margin-top: 2px; }
.modal-warn { font-size: 12px; color: var(--danger); display: flex; align-items: center; gap: 6px; }
.modal-footer { padding: 16px 24px; border-top: 1px solid var(--border); display: flex; justify-content: flex-end; gap: 10px; }
.btn { padding: 8px 20px; border-radius: 8px; border: none; font-family: var(--sans); font-size: 13px; font-weight: 500; cursor: pointer; transition: background .15s, opacity .15s; }
.btn:disabled { opacity: .5; cursor: not-allowed; }
.btn-ghost  { background: var(--border); color: var(--text); }
.btn-ghost:hover:not(:disabled) { background: #353548; }
.btn-danger { background: var(--danger); color: #fff; }
.btn-danger:hover:not(:disabled) { background: #ff4455; }

/* ── Empty state ── */
.empty { text-align: center; padding: 80px 20px; color: var(--muted); }
.empty-icon { font-size: 48px; margin-bottom: 16px; }
.empty h3 { font-size: 16px; font-weight: 500; color: var(--text); margin-bottom: 6px; }
.empty p { font-size: 13px; }

/* ── Toast ── */
.toast {
  position: fixed; bottom: 50px; left: 50%; transform: translateX(-50%) translateY(20px);
  background: var(--card); border: 1px solid var(--border);
  border-radius: 10px; padding: 10px 20px;
  font-size: 13px; font-weight: 500;
  opacity: 0; pointer-events: none; transition: all .3s; z-index: 200;
  display: flex; align-items: center; gap: 8px;
}
.toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }
.toast.ok  { border-color: var(--success); color: var(--success); }
.toast.err { border-color: var(--danger);  color: var(--danger); }

/* ── Scrollbar fix ── */
.table-wrap { scrollbar-gutter: stable; }
</style>
</head>
<body>
<div class="app">

<!-- ── Sidebar ── -->
<aside class="sidebar">
  <div class="logo">
    <div class="logo-title">Session Manager</div>
    <div class="logo-sub">Claude Code<br>会话管理</div>
  </div>
  <div class="stats">
    <div class="stat-card active-filter" data-filter="all" onclick="setFilter('all',this)">
      <div><div class="stat-dot all"></div></div>
      <div><div class="stat-num" id="s-all">0</div><div class="stat-label">全部会话</div></div>
    </div>
    <div class="stat-card" data-filter="live" onclick="setFilter('live',this)">
      <div><div class="stat-dot live"></div></div>
      <div><div class="stat-num" id="s-live">0</div><div class="stat-label">活跃</div></div>
    </div>
    <div class="stat-card" data-filter="arch" onclick="setFilter('arch',this)">
      <div><div class="stat-dot arch"></div></div>
      <div><div class="stat-num" id="s-arch">0</div><div class="stat-label">已归档</div></div>
    </div>
  </div>
  <div class="sidebar-actions">
    <button class="btn-side refresh" onclick="loadSessions()"><span class="btn-icon">↺</span> 刷新列表</button>
    <button class="btn-side delete-sel" onclick="deleteSelected()"><span class="btn-icon">⌫</span> 删除选中</button>
    <button class="btn-side delete-all" onclick="deleteAll()"><span class="btn-icon">✕</span> 清空全部</button>
  </div>
</aside>

<!-- ── Main ── -->
<div class="main">
  <div class="topbar">
    <div class="search-wrap">
      <span class="search-icon">⌕</span>
      <input class="search-input" id="search" placeholder="搜索标题或首条消息…" oninput="renderTable()">
    </div>
    <div class="sel-info" id="sel-info">已选 0 条</div>
  </div>

  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th><input type="checkbox" class="cb" id="cb-all" onchange="toggleAll(this)"></th>
          <th>状态</th>
          <th>时间</th>
          <th>标题</th>
          <th>首条消息</th>
          <th style="text-align:center">消息数</th>
          <th>模型</th>
          <th style="text-align:center">文件夹</th>
        </tr>
      </thead>
      <tbody id="tbody"></tbody>
    </table>
    <div class="empty" id="empty" style="display:none">
      <div class="empty-icon">📭</div>
      <h3>没有找到会话</h3>
      <p>尝试修改搜索条件或刷新列表</p>
    </div>
  </div>

  <div class="statusbar">
    <span id="status-text">正在加载…</span>
    <span style="margin-left:auto; display:flex; gap:16px;">
      <span><kbd>Del</kbd> 删除选中</span>
      <span><kbd>F5</kbd> 刷新</span>
      <span><kbd>Ctrl+A</kbd> 全选</span>
    </span>
  </div>
</div>
</div>

<!-- ── Confirm Modal ── -->
<div class="overlay" id="overlay" onclick="e=>e.target===this&&closeModal()">
  <div class="modal">
    <div class="modal-header">
      <div class="modal-icon">⚠️</div>
      <div>
        <div class="modal-title" id="modal-title">确认删除</div>
        <div class="modal-subtitle" id="modal-subtitle"></div>
      </div>
    </div>
    <div class="modal-body">
      <div class="modal-list" id="modal-list"></div>
      <div class="modal-warn">⚠ 此操作将同时删除 JSON 文件与对应文件夹，不可撤销</div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-ghost" onclick="closeModal()">取消</button>
      <button class="btn btn-danger" id="confirm-btn" onclick="execDelete()">确认删除</button>
    </div>
  </div>
</div>

<!-- ── Toast ── -->
<div class="toast" id="toast"></div>

<script>
let sessions = [];
let filter   = 'all';
let pending  = [];

async function loadSessions() {
  setStatus('正在加载…');
  try {
    const r = await fetch('/api/sessions');
    sessions = await r.json();
    updateStats();
    renderTable();
  } catch(e) {
    setStatus('⚠ 加载失败：' + e.message, 'err');
  }
}

function updateStats() {
  const arch = sessions.filter(s=>s.archived).length;
  document.getElementById('s-all').textContent  = sessions.length;
  document.getElementById('s-live').textContent = sessions.length - arch;
  document.getElementById('s-arch').textContent = arch;
}

function setFilter(f, el) {
  filter = f;
  document.querySelectorAll('.stat-card').forEach(c=>c.classList.remove('active-filter'));
  el.classList.add('active-filter');
  renderTable();
}

function getVisible() {
  const kw = document.getElementById('search').value.trim().toLowerCase();
  return sessions.filter(s => {
    if (filter==='live' && s.archived) return false;
    if (filter==='arch' && !s.archived) return false;
    if (kw && !s.title.toLowerCase().includes(kw) && !s.init_msg.toLowerCase().includes(kw)) return false;
    return true;
  });
}

function renderTable() {
  const vis = getVisible();
  const tbody = document.getElementById('tbody');
  const empty = document.getElementById('empty');
  tbody.innerHTML = '';
  empty.style.display = vis.length ? 'none' : 'block';

  vis.forEach((s,i) => {
    const tr = document.createElement('tr');
    tr.className = s.archived ? 'archived' : '';
    tr.dataset.id = s.id;
    tr.onclick = (e) => { if(e.target.type!=='checkbox') toggleRow(tr, s.id); };

    const msgs = s.user_msgs + s.asst_msgs;
    const badgeCls = s.archived ? 'badge arch' : 'badge live';
    const badgeTxt = s.archived ? '🗄 归档' : '● 活跃';

    tr.innerHTML = `
      <td><input type="checkbox" class="cb row-cb" data-id="${s.id}" onclick="e=>e.stopPropagation();syncCbAll()"></td>
      <td><span class="${badgeCls}">${badgeTxt}</span></td>
      <td class="time-cell">${s.time_str}</td>
      <td class="title-cell" title="${esc(s.title)}">${esc(s.title)}</td>
      <td class="init-cell"  title="${esc(s.init_msg)}">${esc(s.init_msg) || '<span style="color:#3a3a55">（空）</span>'}</td>
      <td class="msgs-cell">${msgs > 0 ? msgs : '—'}</td>
      <td class="model-cell" title="${esc(s.model)}">${esc(s.model)}</td>
      <td class="folder-cell">${s.has_folder ? '📁' : '—'}</td>
    `;
    tbody.appendChild(tr);
  });

  syncSelInfo();
  const shown = vis.length;
  setStatus(`共 ${sessions.length} 条会话  ·  显示 ${shown} 条`);
}

function esc(s) {
  return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function getSelected() {
  return [...document.querySelectorAll('.row-cb:checked')].map(c=>c.dataset.id);
}

function toggleRow(tr, id) {
  const cb = tr.querySelector('.row-cb');
  cb.checked = !cb.checked;
  tr.classList.toggle('selected', cb.checked);
  syncCbAll(); syncSelInfo();
}

function toggleAll(master) {
  document.querySelectorAll('.row-cb').forEach(cb => {
    cb.checked = master.checked;
    cb.closest('tr').classList.toggle('selected', master.checked);
  });
  syncSelInfo();
}

function syncCbAll() {
  const all = document.querySelectorAll('.row-cb');
  const chk = document.querySelectorAll('.row-cb:checked');
  const master = document.getElementById('cb-all');
  master.indeterminate = chk.length > 0 && chk.length < all.length;
  master.checked = chk.length === all.length && all.length > 0;
  syncSelInfo();
}

function syncSelInfo() {
  const n = getSelected().length;
  document.getElementById('sel-info').textContent = `已选 ${n} 条`;
}

function getSessionsById(ids) {
  return sessions.filter(s=>ids.includes(s.id));
}

function showModal(targets) {
  pending = targets;
  document.getElementById('modal-title').textContent = `确认删除 ${targets.length} 条会话`;
  document.getElementById('modal-subtitle').textContent = `同时删除对应的 JSON 文件与文件夹`;
  const list = document.getElementById('modal-list');
  list.innerHTML = targets.map(s=>`
    <div class="modal-item">
      <div class="modal-item-icon">${s.has_folder ? '📁' : '📄'}</div>
      <div>
        <div class="modal-item-title">${esc(s.title)} ${s.archived?'<span style="color:var(--muted);font-size:11px">🗄 归档</span>':''}</div>
        <div class="modal-item-sub">${s.time_str} · ${s.user_msgs+s.asst_msgs} 条消息 · ${esc(s.init_msg.slice(0,50))}${s.init_msg.length>50?'…':''}</div>
      </div>
    </div>
  `).join('');
  document.getElementById('overlay').classList.add('show');
}

function closeModal() {
  document.getElementById('overlay').classList.remove('show');
  pending = [];
}

function deleteSelected() {
  const ids = getSelected();
  if (!ids.length) { toast('请先勾选要删除的会话', 'err'); return; }
  showModal(getSessionsById(ids));
}

function deleteAll() {
  const vis = getVisible();
  if (!vis.length) { toast('没有可删除的会话', 'err'); return; }
  showModal(vis);
}

async function execDelete() {
  const btn = document.getElementById('confirm-btn');
  btn.disabled = true; btn.textContent = '删除中…';
  try {
    const ids = pending.map(s=>s.id);
    const r = await fetch('/api/delete', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ids})
    });
    const res = await r.json();
    const ok  = res.filter(r=>r.ok).length;
    const err = res.filter(r=>!r.ok).length;
    closeModal();
    await loadSessions();

    if (!err) {
      // 重启 Claude Code
      btn.textContent = '正在重启…';
      toast(`✓ 已删除 ${ok} 条，正在重启 Claude Code…`, 'ok');
      try {
        const rr = await fetch('/api/restart', { method: 'POST' });
        const rd = await rr.json();
        if (!rd.ok) toast('⚠ 重启失败：' + (rd.error||'未知错误'), 'err');
      } catch(e) {
        toast('⚠ 重启请求失败：' + e.message, 'err');
      }
    } else {
      toast(`删除完成，${ok} 成功 ${err} 失败`, 'err');
    }
  } catch(e) {
    toast('删除请求失败：' + e.message, 'err');
  } finally {
    btn.disabled = false; btn.textContent = '确认删除';
  }
}

function setStatus(msg, cls='') {
  const el = document.getElementById('status-text');
  el.textContent = msg;
  el.className = cls ? 'status-'+cls : '';
}

let toastTimer;
function toast(msg, type='ok') {
  const el = document.getElementById('toast');
  el.textContent = msg; el.className = 'toast show ' + type;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(()=>el.classList.remove('show'), 3000);
}

// 键盘快捷键
document.addEventListener('keydown', e => {
  if (e.key==='Delete' && !e.target.matches('input')) deleteSelected();
  if (e.key==='F5') { e.preventDefault(); loadSessions(); }
  if (e.key==='a' && e.ctrlKey) { e.preventDefault(); document.getElementById('cb-all').click(); }
  if (e.key==='Escape') closeModal();
});

loadSessions();
</script>
</body>
</html>
"""

# ── HTTP 服务器 ─────────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_): pass  # 静默日志

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/" or path == "/index.html":
            self._send(200, "text/html; charset=utf-8", HTML.encode())
        elif path == "/api/sessions":
            data = json.dumps(load_sessions(), ensure_ascii=False).encode()
            self._send(200, "application/json", data)
        else:
            self._send(404, "text/plain", b"Not Found")

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/api/delete":
            length = int(self.headers.get("Content-Length", 0))
            body   = json.loads(self.rfile.read(length))
            result = delete_sessions(body.get("ids", []))
            data   = json.dumps(result, ensure_ascii=False).encode()
            self._send(200, "application/json", data)
        elif path == "/api/restart":
            result = restart_claude()
            data   = json.dumps(result, ensure_ascii=False).encode()
            self._send(200, "application/json", data)
        else:
            self._send(404, "text/plain", b"Not Found")

    def _send(self, code, ctype, body):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", len(body))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

def main():
    port = 18765
    server = HTTPServer(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{port}"
    print(f"\n  Claude Session Manager")
    print(f"  ── 已启动：{url}")
    print(f"  ── 按 Ctrl+C 退出\n")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  已退出")

if __name__ == "__main__":
    main()
