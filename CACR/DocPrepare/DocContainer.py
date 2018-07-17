#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author:ChenXuhan
import re
class DocContainer:
    #过滤HTML中的标签
    # 将HTML中标签等信息去掉
    # @param htmlstr HTML字符串.
    def removeAnnotation(htmlstr):
        # 先过滤CDATA
        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
        re_br = re.compile('<br\s*?/?>')  # 处理换行
        re_h = re.compile('</?\w+[^>]*>')  # HTML标签
        re_comment = re.compile('<!--[^>]*-->')  # HTML注释
        s = re_cdata.sub('', htmlstr)  # 去掉CDATA
        s = re_script.sub('', s)  # 去掉SCRIPT
        s = re_style.sub('', s)  # 去掉style
        s = re_br.sub('\n', s)  # 将br转换为换行
        s = re_h.sub('', s)  # 去掉HTML 标签
        s = re_comment.sub('', s)  # 去掉HTML注释
        # 去掉多余的空行
        blank_line = re.compile('\n+')
        s = blank_line.sub('\n', s)
        return s


if __name__ == '__main__':
    html = "<p>I want to use a track-bar to change a form's opacity.</p> <p>This is my code:</p> <pre><code>decimal trans = trackBar1.Value / 5000;this.Opacity = trans;</code></pre><p>When I try to build it, I get this error:</p>\
     \
     <blockquote>\
       <p>Cannot implicitly convert type 'decimal' to 'double'.</p>\
     </blockquote>\
     <p>I tried making <code>trans</code> a <code>double</code>, but then the control doesn't work. This code has worked fine for me in VB.NET in the past. </p>\
     "
    result = DocContainer.removeAnnotation(html)
    print(result)