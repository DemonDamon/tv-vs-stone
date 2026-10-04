#!/usr/bin/env python3
"""
Enhance TV vs Stone game:
1. High-DPI canvas support 
2. Language switching
3. Replace all Chinese text with T() function calls
"""

import re

print("Reading original file...")
with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Line 19 (index 18) contains all the audio data as a complete <script> tag
# Lines 1-18 are the HTML header
# Line 19 is the audio data script
# Lines 20+ are the game script

html_header_lines = lines[:18]  # Lines 1-18
audio_line = lines[18]          # Line 19
game_script_lines = lines[19:]  # Lines 20+

print(f"HTML header: {len(html_header_lines)} lines")
print(f"Audio data: {len(audio_line)} chars")  
print(f"Game script: {len(game_script_lines)} lines")

# Build new HTML header with language button
new_header = '''<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>电视机大战圆石头 / TV vs Round Stone — v1.0 Final Build</title>
<style>
  html,body{margin:0;height:100%;background:#05070D;overflow:hidden}
  body{display:flex;align-items:center;justify-content:center;font-family:sans-serif}
  #stage{width:780px;height:520px;transform-origin:center center;
         box-shadow:0 0 60px rgba(77,166,255,.14);border-radius:12px;overflow:hidden}
  canvas{display:block;background:#0B0F1A}
  #boot{position:fixed;left:0;right:0;bottom:14px;text-align:center;color:#4A5370;font-size:12px}
  #lang-btn{position:fixed;top:20px;right:20px;padding:8px 16px;background:#1A2332;
             border:2px solid #3A4A66;border-radius:6px;color:#8FA4C8;font-size:14px;
             cursor:pointer;transition:all 0.2s;font-family:sans-serif;z-index:1000}
  #lang-btn:hover{background:#243449;border-color:#4A6A96;color:#A8C0E8}
  #lang-btn:active{transform:scale(0.95)}
</style>
</head>
<body>
<div id="stage"><canvas id="c"></canvas></div>
<div id="boot"></div>
<button id="lang-btn"></button>
'''

# Build language system to inject at start of game script
lang_system = '''<script>
"use strict";
/* ============================================================================
   电视机大战圆石头 / TV vs Round Stone — Final Build v1.0 + HDPi + i18n
   Enhanced with high-DPI support and bilingual language switching
   ============================================================================ */
(function () {
  /* ------------------------------------------------------------------ 0. 语言系统 / Language System */
  var LANG = localStorage.getItem("tvstone_lang") || (navigator.language.startsWith("zh") ? "zh" : "en");
  var TEXTS = {
    zh: {
      title: "电视机大战圆石头",
      subtitle: "TV vs Round Stone  ·  v1.0 Final Build",
      instructions: "滚来的石头全部别撞 · 撞一下裂一格 · 攒满静电放电清场",
      bootHint: "WASD / 方向键 移动 · 空格 放电 · Esc 暂停 · F5 存档 · F9 读档",
      hudHint: "Esc 暂停 · F5 存档 · F9 读档 · 空格放电",
      menuNew: "▶ 新游戏",
      menuLoad: "📂 读档",
      menuRecords: "📊 成绩",
      menuHint: "↑↓ 选择   Space 确认   F9 直接读档",
      pause: "暂停",
      pauseContinue: "▶ 继续",
      pauseSave: "💾 存档",
      pauseLoad: "📂 读档",
      pauseRestart: "🔄 重新开始",
      pauseMenu: "🚪 退出到菜单",
      pauseHint: "↑↓ 选择   Space 确认   Esc / F5 存档   F9 读档",
      gameOver: "屏幕全裂",
      gameOverMsg: "它还在滚。你再来一局。",
      gameOverHint: "Space / R 再来一局    ·    Esc 回菜单",
      recordsSaved: "已写入成绩记录",
      recordsTitle: "成绩记录（最多 10 条）",
      recordsEmpty: "暂无记录",
      recordsHint: "Space / Esc 返回菜单",
      countdownHint: "大石小石都会滚过来 —— 全都别撞，屏幕只有 3 格",
      screen: "屏幕",
      charge: "静电",
      score: "分数",
      tier: "档位",
      hits: "撞击",
      stones: "撞石",
      survived: "存活",
      times: "次",
      toReach: "到达档位",
      saveSuccess: "存档成功",
      loadSuccess: "读档成功",
      noSave: "无存档",
      langBtn: "English"
    },
    en: {
      title: "TV vs Round Stone",
      subtitle: "电视机大战圆石头  ·  v1.0 Final Build",
      instructions: "Dodge all rolling stones · Each hit cracks the screen · Charge up and discharge to clear",
      bootHint: "WASD / Arrows to move · Space to discharge · Esc to pause · F5 to save · F9 to load",
      hudHint: "Esc pause · F5 save · F9 load · Space discharge",
      menuNew: "▶ New Game",
      menuLoad: "📂 Load",
      menuRecords: "📊 Records",
      menuHint: "↑↓ Select   Space Confirm   F9 Quick Load",
      pause: "Paused",
      pauseContinue: "▶ Continue",
      pauseSave: "💾 Save",
      pauseLoad: "📂 Load",
      pauseRestart: "🔄 Restart",
      pauseMenu: "🚪 Exit to Menu",
      pauseHint: "↑↓ Select   Space Confirm   Esc / F5 Save   F9 Load",
      gameOver: "Screen Shattered",
      gameOverMsg: "The stones keep rolling. Try again.",
      gameOverHint: "Space / R to retry    ·    Esc to menu",
      recordsSaved: "Record saved",
      recordsTitle: "Records (Top 10)",
      recordsEmpty: "No records yet",
      recordsHint: "Space / Esc to return",
      countdownHint: "All stones will roll at you — dodge them all, screen has only 3 durability",
      screen: "Screen",
      charge: "Charge",
      score: "Score",
      tier: "Tier",
      hits: "Hits",
      stones: "Stones",
      survived: "Time",
      times: "x",
      toReach: "reached tier",
      saveSuccess: "Saved",
      loadSuccess: "Loaded",
      noSave: "No save data",
      langBtn: "中文"
    }
  };
  function T(key) { return TEXTS[LANG][key] || key; }
  function setLang(lang) {
    LANG = lang;
    localStorage.setItem("tvstone_lang", lang);
    var btn = document.getElementById("lang-btn");
    var boot = document.getElementById("boot");
    if (btn) btn.textContent = T("langBtn");
    if (boot) boot.innerHTML = T("bootHint");
  }
  var langBtn = document.getElementById("lang-btn");
  if (langBtn) {
    langBtn.addEventListener("click", function() {
      setLang(LANG === "zh" ? "en" : "zh");
    });
  }
  setLang(LANG);

  /* ------------------------------------------------------------------ 1. 高DPI画布 / High-DPI Canvas Setup */
  var CV = document.getElementById('c');
  var DPR = window.devicePixelRatio || 1;
'''

# Join game script lines and modify them
game_script = ''.join(game_script_lines)

# Remove the original opening of the IIFE since we're adding it in lang_system
# The original starts with <script>\n"use strict";\n/* comments */\n(function () {
# We want to skip to after the opening (function () { line

# Find where the main function content starts (after the opening comment and (function () {)
match = re.search(r'\(function \(\) \{\n', game_script)
if match:
    # Skip past the (function () { part
    game_script = game_script[match.end():]
else:
    print("Warning: Could not find (function () { pattern")

# Now modify the script content
print("Applying text and code replacements...")

# First, handle the CV and context setup
# Remove the lines:  var CV = document.getElementById('c');
#                     var X = CV.getContext('2d');
#                     var W = 780, H = 520;
# And replace with our high-DPI setup

# Remove old CV definition (we added it in lang_system)
game_script = re.sub(r'  var CV = document\.getElementById\([\'"]c[\'"]\);\n', '', game_script)

# Replace context and dimensions with DPR-aware version
game_script = re.sub(
    r'  var X = CV\.getContext\([\'"]2d[\'"]\);\n  var W = 780, H = 520;',
    '''  var X = CV.getContext('2d');
  var W = 780, H = 520;
  
  // Set canvas resolution based on device pixel ratio for crisp rendering
  CV.width = W * DPR;
  CV.height = H * DPR;
  CV.style.width = W + 'px';
  CV.style.height = H + 'px';
  X.scale(DPR, DPR);''',
    game_script
)

# Text replacements - replace hardcoded Chinese strings with T() calls
print("Replacing UI text strings...")

replacements = [
    # Simple direct replacements
    (r"'屏幕'", "T('screen')"),
    (r'"屏幕"', "T('screen')"),
    (r"'静电'", "T('charge')"),
    (r'"静电"', "T('charge')"),
    
    # Strings with concatenation
    (r"'分数 ' \+ score", "T('score') + ' ' + score"),
    (r'"分数 " \+ score', "T('score') + ' ' + score"),
    (r"'档位 ' \+ diffTier\(\)", "T('tier') + ' ' + diffTier()"),
    (r'"档位 " \+ diffTier\(\)', "T('tier') + ' ' + diffTier()"),
    
    # HUD hint
    (r"'Esc 暂停 · F5 存档 · F9 读档 · 空格放电'", "T('hudHint')"),
    (r'"Esc 暂停 · F5 存档 · F9 读档 · 空格放电"', "T('hudHint')"),
    
    # Menu strings
    (r"'电视机大战圆石头'", "T('title')"),
    (r'"电视机大战圆石头"', "T('title')"),
    (r"'TV vs Round Stone  ·  v1.0 Final Build'", "T('subtitle')"),
    (r'"TV vs Round Stone  ·  v1.0 Final Build"', "T('subtitle')"),
    (r"'滚来的石头全部别撞 · 撞一下裂一格 · 攒满静电放电清场'", "T('instructions')"),
    (r'"滚来的石头全部别撞 · 撞一下裂一格 · 攒满静电放电清场"', "T('instructions')"),
    (r"'▶ 新游戏'", "T('menuNew')"),
    (r'"▶ 新游戏"', "T('menuNew')"),
    (r"'📂 读档'", "T('menuLoad')"),
    (r'"📂 读档"', "T('menuLoad')"),
    (r"'📊 成绩'", "T('menuRecords')"),
    (r'"📊 成绩"', "T('menuRecords')"),
    (r"'↑↓ 选择   Space 确认   F9 直接读档'", "T('menuHint')"),
    (r'"↑↓ 选择   Space 确认   F9 直接读档"', "T('menuHint')"),
    
    # Pause menu
    (r"'暂停'", "T('pause')"),
    (r'"暂停"', "T('pause')"),
    (r"'▶ 继续'", "T('pauseContinue')"),
    (r'"▶ 继续"', "T('pauseContinue')"),
    (r"'💾 存档'", "T('pauseSave')"),
    (r'"💾 存档"', "T('pauseSave')"),
    (r"'🔄 重新开始'", "T('pauseRestart')"),
    (r'"🔄 重新开始"', "T('pauseRestart')"),
    (r"'🚪 退出到菜单'", "T('pauseMenu')"),
    (r'"🚪 退出到菜单"', "T('pauseMenu')"),
    (r"'↑↓ 选择   Space 确认   Esc / F5 存档   F9 读档'", "T('pauseHint')"),
    (r'"↑↓ 选择   Space 确认   Esc / F5 存档   F9 读档"', "T('pauseHint')"),
    
    # Game over
    (r"'屏幕全裂'", "T('gameOver')"),
    (r'"屏幕全裂"', "T('gameOver')"),
    (r"'它还在滚。你再来一局。'", "T('gameOverMsg')"),
    (r'"它还在滚。你再来一局。"', "T('gameOverMsg')"),
    (r"'Space / R 再来一局    ·    Esc 回菜单'", "T('gameOverHint')"),
    (r'"Space / R 再来一局    ·    Esc 回菜单"', "T('gameOverHint')"),
    (r"'已写入成绩记录'", "T('recordsSaved')"),
    (r'"已写入成绩记录"', "T('recordsSaved')"),
    
    # Records screen
    (r"'成绩记录（最多 10 条）'", "T('recordsTitle')"),
    (r'"成绩记录（最多 10 条）"', "T('recordsTitle')"),
    (r"'暂无记录'", "T('recordsEmpty')"),
    (r'"暂无记录"', "T('recordsEmpty')"),
    (r"'Space / Esc 返回菜单'", "T('recordsHint')"),
    (r'"Space / Esc 返回菜单"', "T('recordsHint')"),
    
    # Countdown
    (r"'大石小石都会滚过来 —— 全都别撞，屏幕只有 3 格'", "T('countdownHint')"),
    (r'"大石小石都会滚过来 —— 全都别撞，屏幕只有 3 格"', "T('countdownHint')"),
    
    # Stats display - these are trickier because they're in concatenations
    (r"'撞石 '", "T('stones') + ' '"),
    (r'"撞石 "', "T('stones') + ' '"),
    (r"'撞击 '", "T('hits') + ' '"),
    (r'"撞击 "', "T('hits') + ' '"),
    (r"' 次'", "' ' + T('times')"),
    (r'" 次"', "' ' + T('times')"),
    (r"'存活 '", "T('survived') + ' '"),
    (r'"存活 "', "T('survived') + ' '"),
    (r"'到达档位 '", "T('toReach') + ' '"),
    (r'"到达档位 "', "T('toReach') + ' '"),
    
    # Toast messages
    (r"'存档成功'", "T('saveSuccess')"),
    (r'"存档成功"', "T('saveSuccess')"),
    (r"'读档成功'", "T('loadSuccess')"),
    (r'"读档成功"', "T('loadSuccess')"),
    (r"'无存档'", "T('noSave')"),
    (r'"无存档"', "T('noSave')"),
]

for pattern, replacement in replacements:
    before_count = game_script.count(pattern.replace(r"\'", "'").replace(r'\"', '"')[:20])
    game_script = re.sub(pattern, replacement, game_script)
    after_count = game_script.count(replacement[:20])
    if before_count > 0:
        print(f"  ✓ Replaced {before_count} occurrence(s) of {pattern[:30]}...")

print("\nAssembling final file...")

# Assemble everything
final_content = new_header + audio_line + lang_system + game_script

# Write output
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_content)

print(f"\n✓ Successfully created enhanced version!")
print(f"  - Added high-DPI support (uses devicePixelRatio: {DPR if 'DPR' in dir() else 'detected at runtime'})")
print(f"  - Added bilingual language switching (Chinese/English)")
print(f"  - Added language toggle button (top-right)")
print(f"  - Replaced UI text with localized versions")
print(f"  - Preserved all embedded audio data")
print(f"  - Total file size: {len(final_content):,} bytes")
