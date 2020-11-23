# 电子书相关

- 20170307建立 20190814更新

---

## calibre

### 分享

1. 开启本地服务
2. 配置邮件，通过邮箱发送到kindle，[配置方法教程](https://bookfere.com/tools#calibre)
3. usb连接，kindle、手机都可以识别

### 插件

- EpubSplit - 分割epub电子书，适合对合集电子书拆分
- Find Duplicate - 清理重复电子书
- DeDRM - 移除DRM（数字版权保护），购买正版书后可以去除保护并编辑修改


### calibre-web

[calibre-web](https://github.com/janeczku/calibre-web) 可以使用Calibre 生成的数据库和电子书文件，发布成在线图书馆，通过浏览器或OPDS服务访问。

### caibre 与 fcitx

之前一直没有折腾成功，今天（20180806）终于搞定。

根据帖子[1](https://luyangp.github.io/fcitx-for-qt/) [2](https://groups.google.com/forum/#!topic/fcitx/9e4TI39_4sk)，原理应该是arch 系统里的fcitx的qt库，与calibre 自带的库版本不一致，导致 calibre 里无法启动输入法。解决方法是把系统的qt库拷贝到 calibre 对应目录，但之前试了几次都没有成功。操作完毕就可以正常输入。

安装好 fcitx-qt5，拷贝两个文件：

1. `usr/lib/libFcitxQt5DBusAddons.so.1`，需要拷贝到 `/opt/calibre/lib`
2. `usr/lib/qt/plugins/platforminputcontexts/libfcitxplatforminputcontextplugin.so`，需要覆盖到 `/opt/calibre/lib/qt_plugins/platforminputcontexts`

文件的位置来自官方的包信息：[fcitx-qt5 1.2.3-2 File List](https://www.archlinux.org/packages/community/x86_64/fcitx-qt5/files/)






