#!/usr/bin/env python3
"""
Modify TV vs Stone game to add:
1. High-DPI canvas support
2. Language switching (Chinese/English)
3. Improved visual fidelity
"""

import re

# Read the original file
with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Line 19 contains the embedded audio data - keep it intact
audio_data_line = lines[18]  # 0-indexed, so line 19 is index 18

# Build the new HTML
new_html = []

# Lines 1-18: HTML header and structure (modify as needed)
new_html.append('<!DOCTYPE html>\n')
new_html.append('<html lang="zh">\n')
new_html.append('<head>\n')
new_html.append('<meta charset="UTF-8">\n')
new_html.append('<meta name="viewport" content="width=device-width,initial-scale=1">\n')
new_html.append('<title>电视机大战圆石头 / TV vs Round Stone — v1.0 Final Build</title>\n')

# Modified CSS with language button
new_html.append('<style>\n')
new_html.append('  html,body{margin:0;height:100%;background:#05070D;overflow:hidden}\n')
new_html.append('  body{display:flex;align-items:center;justify-content:center;font-family:sans-serif}\n')
new_html.append('  #stage{width:780px;height:520px;transform-origin:center center;\n')
new_html.append('         box-shadow:0 0 60px rgba(77,166,255,.14);border-radius:12px;overflow:hidden}\n')
new_html.append('  canvas{display:block;background:#0B0F1A}\n')
new_html.append('  #boot{position:fixed;left:0;right:0;bottom:14px;text-align:center;color:#4A5370;font-size:12px}\n')
new_html.append('  #lang-btn{position:fixed;top:20px;right:20px;padding:8px 16px;background:#1A2332;\n')
new_html.append('             border:2px solid #3A4A66;border-radius:6px;color:#8FA4C8;font-size:14px;\n')
new_html.append('             cursor:pointer;transition:all 0.2s;font-family:sans-serif;z-index:1000}\n')
new_html.append('  #lang-btn:hover{background:#243449;border-color:#4A6A96;color:#A8C0E8}\n')
new_html.append('  #lang-btn:active{transform:scale(0.95)}\n')
new_html.append('</style>\n')
new_html.append('</head>\n')
new_html.append('<body>\n')
new_html.append('<div id="stage"><canvas id="c"></canvas></div>\n')  # Note: removed width/height attributes
new_html.append('<div id="boot"></div>\n')  # Will be filled by JS
new_html.append('<button id="lang-btn"></button>\n')  # Will be filled by JS

# Line 19: Audio data (keep intact)
new_html.append(audio_data_line)

# Now add the modified JavaScript
new_html.append('<script>\n')
new_html.append('"use strict";\n')
new_html.append('/* ============================================================================\n')
new_html.append('   电视机大战圆石头 / TV vs Round Stone — Final Integrated Build v1.0 + HDPi + i18n\n')
new_html.append('   Enhanced with high-DPI support and language switching\n')
new_html.append('   ============================================================================ */\n')
new_html.append('(function () {\n')

# Add language system first
new_html.append('  /* ------------------------------------------------------------------ 0. 语言系统 */\n')
new_html.append('  var LANG = localStorage.getItem("tvstone_lang") || (navigator.language.startsWith("zh") ? "zh" : "en");\n')
new_html.append('  var TEXTS = {\n')
new_html.append('    zh: {\n')
new_html.append('      title: "电视机大战圆石头",\n')
new_html.append('      subtitle: "TV vs Round Stone  ·  v1.0 Final Build",\n')
new_html.append('      instructions: "滚来的石头全部别撞 · 撞一下裂一格 · 攒满静电放电清场",\n')
new_html.append('      bootHint: "WASD / 方向键 移动 · 空格 放电 · Esc 暂停 · F5 存档 · F9 读档",\n')
new_html.append('      hudHint: "Esc 暂停 · F5 存档 · F9 读档 · 空格放电",\n')
new_html.append('      menuNew: "▶ 新游戏",\n')
new_html.append('      menuLoad: "📂 读档",\n')
new_html.append('      menuRecords: "📊 成绩",\n')
new_html.append('      menuHint: "↑↓ 选择   Space 确认   F9 直接读档",\n')
new_html.append('      pause: "暂停",\n')
new_html.append('      pauseContinue: "▶ 继续",\n')
new_html.append('      pauseSave: "💾 存档",\n')
new_html.append('      pauseLoad: "📂 读档",\n')
new_html.append('      pauseRestart: "🔄 重新开始",\n')
new_html.append('      pauseMenu: "🚪 退出到菜单",\n')
new_html.append('      pauseHint: "↑↓ 选择   Space 确认   Esc / F5 存档   F9 读档",\n')
new_html.append('      gameOver: "屏幕全裂",\n')
new_html.append('      gameOverMsg: "它还在滚。你再来一局。",\n')
new_html.append('      gameOverHint: "Space / R 再来一局    ·    Esc 回菜单",\n')
new_html.append('      recordsSaved: "已写入成绩记录",\n')
new_html.append('      recordsTitle: "成绩记录（最多 10 条）",\n')
new_html.append('      recordsEmpty: "暂无记录",\n')
new_html.append('      recordsHint: "Space / Esc 返回菜单",\n')
new_html.append('      countdownHint: "大石小石都会滚过来 —— 全都别撞，屏幕只有 3 格",\n')
new_html.append('      screen: "屏幕",\n')
new_html.append('      charge: "静电",\n')
new_html.append('      score: "分数",\n')
new_html.append('      tier: "档位",\n')
new_html.append('      hits: "撞击",\n')
new_html.append('      survived: "存活",\n')
new_html.append('      times: "次",\n')
new_html.append('      saveSuccess: "存档成功",\n')
new_html.append('      loadSuccess: "读档成功",\n')
new_html.append('      noSave: "无存档",\n')
new_html.append('      langBtn: "English"\n')
new_html.append('    },\n')
new_html.append('    en: {\n')
new_html.append('      title: "TV vs Round Stone",\n')
new_html.append('      subtitle: "电视机大战圆石头  ·  v1.0 Final Build",\n')
new_html.append('      instructions: "Dodge all rolling stones · Each hit cracks the screen · Charge up and discharge to clear",\n')
new_html.append('      bootHint: "WASD / Arrows to move · Space to discharge · Esc to pause · F5 to save · F9 to load",\n')
new_html.append('      hudHint: "Esc pause · F5 save · F9 load · Space discharge",\n')
new_html.append('      menuNew: "▶ New Game",\n')
new_html.append('      menuLoad: "📂 Load",\n')
new_html.append('      menuRecords: "📊 Records",\n')
new_html.append('      menuHint: "↑↓ Select   Space Confirm   F9 Quick Load",\n')
new_html.append('      pause: "Paused",\n')
new_html.append('      pauseContinue: "▶ Continue",\n')
new_html.append('      pauseSave: "💾 Save",\n')
new_html.append('      pauseLoad: "📂 Load",\n')
new_html.append('      pauseRestart: "🔄 Restart",\n')
new_html.append('      pauseMenu: "🚪 Exit to Menu",\n')
new_html.append('      pauseHint: "↑↓ Select   Space Confirm   Esc / F5 Save   F9 Load",\n')
new_html.append('      gameOver: "Screen Shattered",\n')
new_html.append('      gameOverMsg: "The stones keep rolling. Try again.",\n')
new_html.append('      gameOverHint: "Space / R to retry    ·    Esc to menu",\n')
new_html.append('      recordsSaved: "Record saved",\n')
new_html.append('      recordsTitle: "Records (Top 10)",\n')
new_html.append('      recordsEmpty: "No records yet",\n')
new_html.append('      recordsHint: "Space / Esc to return",\n')
new_html.append('      countdownHint: "All stones will roll at you — dodge them all, screen has only 3 durability",\n')
new_html.append('      screen: "Screen",\n')
new_html.append('      charge: "Charge",\n')
new_html.append('      score: "Score",\n')
new_html.append('      tier: "Tier",\n')
new_html.append('      hits: "Hits",\n')
new_html.append('      survived: "Time",\n')
new_html.append('      times: "x",\n')
new_html.append('      saveSuccess: "Saved",\n')
new_html.append('      loadSuccess: "Loaded",\n')
new_html.append('      noSave: "No save data",\n')
new_html.append('      langBtn: "中文"\n')
new_html.append('    }\n')
new_html.append('  };\n')
new_html.append('  function T(key) { return TEXTS[LANG][key] || key; }\n')
new_html.append('  function setLang(lang) {\n')
new_html.append('    LANG = lang;\n')
new_html.append('    localStorage.setItem("tvstone_lang", lang);\n')
new_html.append('    document.getElementById("lang-btn").textContent = T("langBtn");\n')
new_html.append('    document.getElementById("boot").innerHTML = T("bootHint");\n')
new_html.append('  }\n')
new_html.append('  document.getElementById("lang-btn").addEventListener("click", function() {\n')
new_html.append('    setLang(LANG === "zh" ? "en" : "zh");\n')
new_html.append('  });\n')
new_html.append('  setLang(LANG);\n\n')

# Continue with rest of lines starting from line 20 (original script start)
# But we need to modify specific parts for high-DPI support
# Let me read the rest and inject modifications

print("Generating modified JavaScript...")

# Write initial part
with open('index_modified.html', 'w', encoding='utf-8') as f:
    f.writelines(new_html)

print(f"Created header with {len(new_html)} lines")
print("Now need to process and modify the JavaScript section...")
