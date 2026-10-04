#!/usr/bin/env python3
"""
Quick verification script to test the enhanced game
"""

import re

def check_index_html():
    """Verify all improvements are in place"""
    
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = {
        'High-DPI canvas resolution': (
            'CV.width = W * DPR' in content and 
            'CV.height = H * DPR' in content
        ),
        'Context scaling': 'X.scale(DPR, DPR)' in content,
        'Device pixel ratio detection': 'window.devicePixelRatio' in content,
        'Language system': 'var TEXTS = {' in content,
        'Chinese language dict': 'zh: {' in content,
        'English language dict': 'en: {' in content,
        'Translation function': 'function T(key)' in content,
        'Language toggle button': 'id="lang-btn"' in content,
        'Language persistence': 'localStorage.getItem("tvstone_lang")' in content,
        'Browser language detection': 'navigator.language.startsWith("zh")' in content,
        'Audio data preserved': 'window.AUDIO_B64' in content and len(content) > 2000000,
        'Title translation': "T('title')" in content,
        'Menu translation': "T('menuNew')" in content,
        'HUD translation': "T('screen')" in content and "T('charge')" in content,
        'Pause menu translation': "T('pause')" in content,
        'Game over translation': "T('gameOver')" in content,
    }
    
    print('=' * 60)
    print('TV vs Stone - Enhancement Verification')
    print('=' * 60)
    print()
    
    all_passed = True
    for feature, passed in checks.items():
        status = '✅' if passed else '❌'
        print(f'{status} {feature}')
        if not passed:
            all_passed = False
    
    print()
    print('=' * 60)
    
    if all_passed:
        print('✅ ALL CHECKS PASSED!')
        print()
        print('The game has been successfully enhanced with:')
        print('  • High-DPI canvas support for crisp rendering')
        print('  • Bilingual language switching (Chinese/English)')
        print('  • Language toggle button with persistence')
        print('  • All embedded audio preserved')
        print()
        print('File size:', f'{len(content):,}', 'bytes')
        print()
        print('Ready to deploy! 🚀')
        return True
    else:
        print('❌ SOME CHECKS FAILED')
        print('Please review the implementation.')
        return False

if __name__ == '__main__':
    success = check_index_html()
    exit(0 if success else 1)
