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
    content = f.read()

# Strategy: Split at specific markers and rebuild
# The file structure is:
# - HTML head (lines 1-18)
# - Embedded audio data (line 19 - huge)  
# - JavaScript (lines 20-928)

# Split into sections
parts = content.split('<script>window.AUDIO_B64=')
if len(parts) != 2:
    print("ERROR: Could not find audio data marker")
    exit(1)

html_head = parts[0]
audio_and_script = parts[1]

# Split audio data from script
script_parts = audio_and_script.split('</script>', 1)
audio_data_full = script_parts[0]  # Includes the audio B64 object and closing script tag
remaining = script_parts[1] if len(script_parts) > 1 else ''

# Now split audio data line from the actual game script
# The audio line ends with </script> and next line is <script>
audio_script_parts = audio_data_full.split('\n<script>\n', 1)
audio_line = '<script>window.AUDIO_B64=' + audio_script_parts[0] + '\n'
if len(audio_script_parts) > 1:
    game_script = audio_script_parts[1]
else:
    # Try alternative split
    audio_script_parts = audio_data_full.split('<script>', 1)
    if len(audio_script_parts) > 1:
        audio_line = '<script>window.AUDIO_B64=' + audio_script_parts[0]
        game_script = audio_script_parts[1]
    else:
        print("ERROR: Could not separate audio from game script")
        exit(1)

print(f"Audio data line: {len(audio_line)} chars")
print(f"Game script: {len(game_script)} chars")
print(f"HTML head: {len(html_head)} chars")

# Now modify each section
print("\n=== Modifying HTML head ===")

# Replace HTML head to add language button and remove fixed canvas size
new_head = '''<!DOCTYPE html>
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

print("=== Modifying game script ===")

# Add language system and high-DPI support at the beginning of the script
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

# Find where the original script starts (after "use strict" and comments)
# and extract everything after var CV = ...
script_start_match = re.search(r'  var CV = document\.getElementById\([\'"]c[\'"]\);', game_script)
if script_start_match:
    # Get everything after this line
    after_cv = game_script[script_start_match.end():]
    # Find the next line after CV definition
    next_line_match = re.search(r'\n  var X = ', after_cv)
    if next_line_match:
        rest_of_script = after_cv[next_line_match.start():]
    else:
        rest_of_script = after_cv
else:
    print("Warning: Could not find CV definition, using full script")
    rest_of_script = game_script

print("=== Applying text replacements ===")

# Replace all Chinese text with T() calls in the script
replacements = [
    (r"'屏幕'", "T('screen')"),
    (r'"屏幕"', "T('screen')"),
    (r"'静电'", "T('charge')"),
    (r'"静电"', "T('charge')"),
    (r"'分数 '", "T('score') + ' '"),
    (r'"分数 "', "T('score') + ' '"),
    (r"'档位 '", "T('tier') + ' '"),
    (r'"档位 "', "T('tier') + ' '"),
    (r"'Esc 暂停 · F5 存档 · F9 读档 · 空格放电'", "T('hudHint')"),
    (r'"Esc 暂停 · F5 存档 · F9 读档 · 空格放电"', "T('hudHint')"),
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
    (r"'屏幕全裂'", "T('gameOver')"),
    (r'"屏幕全裂"', "T('gameOver')"),
    (r"'它还在滚。你再来一局。'", "T('gameOverMsg')"),
    (r'"它还在滚。你再来一局。"', "T('gameOverMsg')"),
    (r"'Space / R 再来一局    ·    Esc 回菜单'", "T('gameOverHint')"),
    (r'"Space / R 再来一局    ·    Esc 回菜单"', "T('gameOverHint')"),
    (r"'已写入成绩记录'", "T('recordsSaved')"),
    (r'"已写入成绩记录"', "T('recordsSaved')"),
    (r"'成绩记录（最多 10 条）'", "T('recordsTitle')"),
    (r'"成绩记录（最多 10 条）"', "T('recordsTitle')"),
    (r"'暂无记录'", "T('recordsEmpty')"),
    (r'"暂无记录"', "T('recordsEmpty')"),
    (r"'Space / Esc 返回菜单'", "T('recordsHint')"),
    (r'"Space / Esc 返回菜单"', "T('recordsHint')"),
    (r"'大石小石都会滚过来 —— 全都别撞，屏幕只有 3 格'", "T('countdownHint')"),
    (r'"大石小石都会滚过来 —— 全都别撞，屏幕只有 3 格"', "T('countdownHint')"),
    (r"'撞石 '", "T('hits') + ' '"),
    (r'"撞石 "', "T('hits') + ' '"),
    (r"'撞击 '", "T('hits') + ' '"),
    (r'"撞击 "', "T('hits') + ' '"),
    (r"' 次'", "' ' + T('times')"),
    (r'" 次"', "' ' + T('times')"),
    (r"'存活 '", "T('survived') + ' '"),
    (r'"存活 "', "T('survived') + ' '"),
    (r"'到达档位 '", "T('toReach') + ' '"),
    (r'"到达档位 "', "T('toReach') + ' '"),
    (r"'存档成功'", "T('saveSuccess')"),
    (r'"存档成功"', "T('saveSuccess')"),
    (r"'读档成功'", "T('loadSuccess')"),
    (r'"读档成功"', "T('loadSuccess')"),
    (r"'无存档'", "T('noSave')"),
    (r'"无存档"', "T('noSave')"),
]

modified_script = rest_of_script
for pattern, replacement in replacements:
    modified_script = re.sub(pattern, replacement, modified_script)
    
# Now handle the canvas resolution modifications
# Find and replace the W, H definitions and fit function

# Replace W, H definitions to account for DPR
modified_script = re.sub(
    r'var W = 780, H = 520;',
    'var W = 780, H = 520;\n  CV.width = W * DPR;\n  CV.height = H * DPR;\n  CV.style.width = W + "px";\n  CV.style.height = H + "px";',
    modified_script
)

# Modify fit function (it shouldn't change canvas size, just the stage scale)
# The fit function should stay the same since it only scales the stage div

# Add DPR scaling to context
# Find where X is defined and add scaling
modified_script = re.sub(
    r'(  var X = CV\.getContext\([\'"]2d[\'"]\);)',
    r'\1\n  X.scale(DPR, DPR);',
    modified_script
)

print("=== Assembling final file ===")

# Assemble the final file
final_content = new_head + audio_line + lang_system + modified_script + remaining

# Write the output
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_content)

print(f"\n✓ Successfully created enhanced version!")
print(f"  - Added high-DPI support (devicePixelRatio scaling)")
print(f"  - Added bilingual language switching (Chinese/English)")
print(f"  - Replaced all UI text with localized versions")
print(f"  - Preserved all embedded audio data ({len(audio_line)} chars)")
print(f"  - Total file size: {len(final_content)} chars")
