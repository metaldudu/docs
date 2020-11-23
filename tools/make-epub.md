## epub制作

### 文本来源

- txt
- 网页抓取
- OCR：ABBYY FineReader / [百度AI](https://cloud.baidu.com/product/ocr/general)

### 正则表达式

使用正则表达式来修改txt文档。以vscode为例：

- 替换“第一章”为“## 第一章”，替换`(第.*章)` 为 `## $1`
- 换行后插入空白行，替换`\n` 为 `\n\n`
- 匹配数字开头的行：`^[0-9][\s\S]*` 或 `^[0-9]+.*`
- 非负整数 \d+

文档：[Regular Expressions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions)

## 使用pandoc转换文档

pandoc可以方便的生成带有目录的epub文档，以修改的好的markdown文本文档进行转换，例如

`pandoc 1.md -o 1.epub`

## 转换格式

- calibre 的命令行模式：`ebook-convert "book.epub" "book.mobi"`
- kindlegen ，某些epub用 calibre 转换会失败

## 自写的python脚本

- [txt2md.py](https://github.com/metaldudu/py/blob/master/txt2md.py)
- [md2epub.py](https://github.com/metaldudu/py/blob/master/md2epub.py)

## 修正编码

显示编码： `fiel -i 1.txt` ，或者安装 enca

- 显示编码： `enca 1.txt`
- 转换成UTF-8： `enca -x UTF-8 1.txt`
- 转换多个文件： `enca -x UTF-8 *`
- 另存： `enca -x UTF-8 <1.txt> 2.txt`
- 最好指定定语言： `enca -L zh_CN -x UTF-8 1.txt`

