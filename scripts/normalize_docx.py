#!/usr/bin/env python3
"""Normalize DOCX text to regular Microsoft YaHei and explicit black.
Usage: python normalize_docx.py input.docx output.docx [--font 'Microsoft YaHei']
Uses only the Python standard library. Images and charts are unchanged.
"""
import argparse
import os
from pathlib import Path
import tempfile
from zipfile import ZipFile

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
def normalize(src, dst, font):
    src, dst = Path(src), Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    # Preserve original XML prefixes: mc:Ignorable and similar attributes
    # refer to prefixes by name, so changing them can break Office loading.
    from xml.dom import minidom
    with ZipFile(src) as zin:
        contents = []
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename.startswith('word/') and info.filename.endswith('.xml'):
                doc = minidom.parseString(data)
                def dchild(parent, local):
                    for node in parent.childNodes:
                        if node.nodeType == node.ELEMENT_NODE and node.namespaceURI == W and node.localName == local:
                            return node
                    node = doc.createElementNS(W, 'w:' + local)
                    if parent.localName == "r" and local == "rPr" and parent.firstChild:
                        parent.insertBefore(node, parent.firstChild)
                    else:
                        parent.appendChild(node)
                    return node
                def dregular(rpr):
                    fonts = dchild(rpr, 'rFonts')
                    for i in range(fonts.attributes.length-1, -1, -1):
                        attr = fonts.attributes.item(i)
                        if 'theme' in attr.name.lower(): fonts.removeAttributeNode(attr)
                    for slot in ('ascii','hAnsi','eastAsia','cs'):
                        fonts.setAttributeNS(W,'w:'+slot,font)
                    color = dchild(rpr,'color')
                    for i in range(color.attributes.length-1,-1,-1):
                        color.removeAttributeNode(color.attributes.item(i))
                    color.setAttributeNS(W,'w:val','000000')
                    for flag in ('b','bCs'):
                        dchild(rpr,flag).setAttributeNS(W,'w:val','0')
                for run in list(doc.getElementsByTagNameNS(W,'r')):
                    dregular(dchild(run,'rPr'))
                for rpr in list(doc.getElementsByTagNameNS(W,'rPr')):
                    dregular(rpr)
                if info.filename == 'word/styles.xml':
                    root = doc.documentElement
                    dregular(dchild(dchild(dchild(root,'docDefaults'),'rPrDefault'),'rPr'))
                    for st in list(doc.getElementsByTagNameNS(W,'style')):
                        dregular(dchild(st,'rPr'))
                data = doc.toxml(encoding='utf-8')
            contents.append((info,data))
    fd,tmp = tempfile.mkstemp(prefix='.report-',suffix='.docx',dir=dst.parent)
    os.close(fd)
    try:
        with ZipFile(tmp,'w') as zout:
            for info,data in contents: zout.writestr(info,data)
        os.replace(tmp,dst)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input'); parser.add_argument('output')
    parser.add_argument('--font',default='Microsoft YaHei')
    args = parser.parse_args()
    normalize(args.input,args.output,args.font)
    print('Saved:',args.output)
