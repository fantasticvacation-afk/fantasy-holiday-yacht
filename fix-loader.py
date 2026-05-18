#!/usr/bin/env python3
"""
彻底修复 Loader 问题：
1. 给 #loader 添加 CSS 自动消失动画（不依赖 JS）
2. 把 main.js 移到 i18n.js 之前加载
3. 确保 loader 在 5 秒内一定消失（三重保障：CSS + 内联JS + main.js）
"""
import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html') and os.path.isfile(f)]
updated = 0

for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    
    # === 修复 1: 添加 CSS 自动消失动画到 style.css 引用之后 ===
    loader_css_injection = '''<style>
/* Loader 自动消失 - 三重保障 */
@keyframes autoHideLoader{
  0%,80%{opacity:1;visibility:visible}
  85%{opacity:0.5}
  90%{opacity:0.2}
  95%{opacity:0;visibility:hidden}
  100%{display:none}
}
#loader{animation:autoHideLoader 6s ease-in-out forwards}
#loader.hidden,#loader[style*="display:none"]{animation:none!important;display:none!important}
</style>'''

    if '<link href="style.css"' in content and 'autoHideLoader' not in content:
        content = content.replace(
            '<link href="style.css" rel="stylesheet"/>',
            '<link href="style.css" rel="stylesheet"/>\n' + loader_css_injection
        )
    
    # === 修复 2: 调整脚本顺序 - main.js 在 i18n.js 之前 ===
    # 把 <script src="main.js"></script> 移到 <script src="i18n.js"></script> 前面
    if '<script src="i18n.js"></script>' in content and '<script src="main.js"></script>' in content:
        # 移除原有的 main.js 标签
        content = content.replace('<script src="main.js"></script>\n', '')
        # 在 i18n.js 之前插入 main.js
        content = content.replace(
            '<script src="i18n.js"></script>',
            '<script src="main.js"></script>\n<script src="i18n.js"></script>'
        )
    
    # === 修复 3: 确保内联 script 有更强的 loader 隐藏逻辑 ===
    # 在第一个 <script> 标签之前添加立即执行的 loader fallback
    immediate_fallback = '''<script>
/* 立即执行 - 不等 DOMContentLoaded */
(function(){
  var ld=document.getElementById("loader");
  if(!ld)return;
  /* 5.5秒后强制隐藏 - 兜底 */
  setTimeout(function(){
    if(ld){ld.style.display="none";ld.style.visibility="hidden"}
    document.body.style.overflow="";
  },5500);
})();
</script>
'''
    
    if 'autoHideLoader' in content and 'immediate-loader-fallback' not in content:
        content = content.replace('<script>\nwindow.addEventListener', immediate_fallback + '<script>\nwindow.addEventListener')
    
    if content != original:
        updated += 1
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ 已修复: {fname}")
    else:
        print(f"  无变化: {fname}")

print(f"\n完成！修复了 {updated} 个文件")
