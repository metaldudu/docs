# RetroArch/Lakka

## Lakka 安装笔记

1. 烧录优盘部分略

2. 解决eeepc1000h进入看到logo小花后，定时闪烁问题。进入启动到命令行模式：

保持capslock键大写打开（笔记本本机键盘无效，外接USB键盘），开机出现“ SYSLINUX 6.04 EDD 6.04-pre1 Copyright (C) 1994-2015 H. Peter Anvin et al
boot: linux tty retroarch=0

然后 ctrl + alt + f3，会进入命令行。

nano ~/.config/retroarch/retroarch.cfg

添加一行：`menu_shader_pipeline = "0"` ，重启

3.eeepc1000h实测2.2nightly版本无法刷新wifi （Lakka-Generic.i386-2.2-devel-20190117000709-r28252-gf5f1896.img）

类似的问题：https://github.com/libretro/RetroArch/issues/7227

4. acer aspire one d271，实测安装后停留在小花界面。怀疑显卡不支持，放弃。

20190220

## archlinux安装

按照官方说明，直接pacman： `sudo pacman -Sy retroarch`