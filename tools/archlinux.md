# archlinux


> 更新：2020.4.17

## 安装准备

1. 下载最新版镜像，用rufus写入U盘
2. BIOS，Disable Secure Boot. BIOS > Secure Boot > Disabled
3. 确保ACHI模式
4. Win10关闭快速启动（控制面板-电源计划）
5. Win10压缩卷，留出给Linux的空间

## 安装开始

### 分区

1. lsblk 显示所有分区，找到win10带的 EFI 分区和空白分区
2. `cfdisk /dev/sda` 进行分区，在 free space 上选择 New、Write，输入q退出。显示linux分区是/dev/sda9
3. 格式化分区 `mkfs.ext4 /dev/sda9`，这里没做swap分区
4. 挂载根分区 `mount /dev/sda9 /mnt`
5. 挂载ESP分区 `mkdir /mnt/boot` `mount /dev/sda1 /mnt/boot`

### 网络

wifi-menu ，选择并配置无线网络。ping通了就ok。

### 安装

- 修改/etc/pacman.d/mirrorlist，Server = http://mirrors.163.com/archlinux/$repo/os/$arch
- 安装基本系统     `pacstrap /mnt base linux linux-firmware`
- 生成fstab `# genfstab -U /mnt >> /mnt/etc/fstab`
- `arch-chroot /mnt /bin/bash` 进入系统

## 配置

- Locale：编辑`/etc/locale.gen`，去掉三行注释：en_US.UTF-8 UTF-8 zh_CN.UTF-8 UTF-8 zh_TW.UTF-8 UTF-8。执行 `locale-gen`，写入配置 `echo LANG=en_US.UTF-8 > /etc/locale.conf`
- 时间： `tzselect` ，选择亚洲上海，生成时区配置 `hwclock --systohc --utc`
- 主机名：`echo mypc > /etc/hostname`
- 对应的hosts，修改 /etc/hosts
```
127.0.0.1	localhost
::1		localhost
127.0.1.1	myhostname.localdomain	myhostname
```

- **网络配置**：新系统并没有网络包，所以要安装：`pacman -S iw wpa_supplicant dialog`
- 安装其他需要的包，包括桌面环境、启动器
- root密码：`passwd`

## 系统引导

参考官方指引

- exit退出chroot
- 卸载分区：umount -R /mnt
- reboot重启，检查bios里grub是不是第一启动项，正常可以进入arch

### 用户

- 添加普通用户：useradd -m -g users -s /bin/bash laodu
- 设置密码： passwd laodu
- 设置sudo用户：`pacman -S sudo` 执行 visudo，添加一行 `laodu  ALL=(ALL) ALL`

## 系统配置

### 电源

编辑： /etc/systemd/logind.conf 加入以下两行，实现笔记本合盖挂起系统：

    HandleLidSwitch=suspend
    HandleLidSwitchExternalPower=suspend

然后执行：`systemctl restart systemd-logind`

### 图形界面

- 安装显卡： `pacman -S xf86-video-inte`
- 安装桌面环境：`pacman -S mate mate-extra`
- 安装显示管理器： `pacman -S lightdm-gtk-greeter` 执行 ` systemctl enable lightdm`
- 如果使用startx进入桌面,编辑xinitrc，参考[Xinit](https://wiki.archlinux.org/index.php/Xinit_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87))
- 桌面系统要显示中文，就在`.xprofile` 文件添加：　`export LC_ALL="zh_CN.UTF-8"`

### 声音（MagicBook2019）

安装 alsa-utils 和  pulseaudio，前者可以使用 alsamixer 来调整声音设备音量，取消静音按m键；后者在任务栏显示声音图标。运行 `aplay- l` 可以看到当前音频设备：

    card 0: Generic [HD-Audio Generic], device 3: HDMI 0 [HDMI 0]
    Subdevices: 1/1
      Subdevice #0: subdevice #0
    card 0: Generic [HD-Audio Generic], device 7: HDMI 1 [HDMI 1]
      Subdevices: 1/1
      Subdevice #0: subdevice #0
    card 1: Generic_1 [HD-Audio Generic], device 0: ALC256 Analog [ALC256 Analog]
      Subdevices: 1/1
      Subdevice #0: subdevice #0

默认应该选择 card1 ，所以建立 `~/.asoundrc` ，内容如下：

    defaults.pcm.card 1
    defaults.pcm.device 0
    defaults.ctl.card 1
注销一下就可以了。

### 触控板

sudo pacman -S xf86-input-synaptics

### 移动硬盘

安装 `ntfs-3g udevil`，重启后自动识别免输入密码

### 源

添加源，编辑 /etc/pacman.conf 。[清华大学的ArchlinuxCN镜像](https://mirror.tuna.tsinghua.edu.cn/help/archlinuxcn/)：

    [archlinuxcn]
    SigLevel = Optional TrustedOnly
    Server = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch

20190618，弃用了yaourt，改用[yay](https://github.com/Jguer/yay)。源修改参考：[AUR 镜像使用帮助](https://mirror.tuna.tsinghua.edu.cn/help/AUR/) （yay 的临时目录在 ~/.cache/yay）

### pacman

确保安装了 `pacman -S --needed base-devel`
执行`pacman -Syy`

#### 常用pacman命令

pacman -Syu 升级系统
pacman -Syy 同步软件列表
pacman -Scc 清理软件包
pacman -S xxx 安装
pacman -Ss xxx 查询
pacman -R xxx 卸载
pacman -Qs xxx 查询已安装包

invalid pgp key错误解决 : `$ sudo pacman-key --refresh-keys`

### 环境变量

编辑 `~/.bashrc`，加入

`export PATH=$PATH:/somepath`

### 字体

查看中文字体： `fc-list :lang=zh`

- 等宽字体： `pacman -S ttf-dejavu`
- emoji： `noto-fonts-emoji`
- 文泉驿微米黑： `pacman -S wqy-microhei`
- 思源宋体和黑体： adobe-source-han-serif-cn-fonts 和 adobe-source-han-sans-cn-fonts，避免安装 otc 字体产生混乱。

常用软件添加字体，如思源宋体 Source Han Serif CN


### 中文输入法

- pacman -S fcitx  fcitx-im fcitx-configtool 
- 中州韵输入法：`pacman -S fcitx-rime librime`
- 需要编辑 `.xprofile` 文件,添加如下:

```
export XMODIFIERS=@im=fcitx
export QT_IM_MODULE=fcitx
export GTK_IM_MODULE=fcitx
```

rim默认显示繁体，我只需要明月拼音简化字这个方案，所以在`~/.config/fcitx/rime/`下面建立文件 `default.custom.yaml`，加入如下内容然后重新部署。

    patch:
      schema_list:
        - schema: luna_pinyin_simp

### 网络配置

使用 networkmanager 管理无线网络，参考[wiki](https://wiki.archlinux.org/index.php/NetworkManager_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87))

托盘图标不见了，用 `nm-applet &` 重启

### 键盘快捷键

- 截图：flameshot gui > win+3
- 窗口移动：win+方向键
- 主文件夹：win+E
- 隐藏所有窗口：win+E
- 在albert 里设置快捷键：win+1，并设置随系统启动

### zsh

```cpp
chsh -s `which zsh`
```

### 翻墙

参考：https://www.xzymoe.com/linux-ssr/ ，本机socket5代理

查询本机ip： `$curl ipinfo.io`

### 美化

安装图标 `numix-icon-theme` 主题：`arc-gtk-theme`

## 软件

### 坚果云

    pacman -S nutstore jre10-openjdk

选择其他jre环境报错，原因不明

### 网易云音乐

托盘菜单无法显示，最小化之后只能手动杀死进程。参考[这里](https://forum.ubuntu.org.cn/viewtopic.php?f=74&t=484624)解决：

修改启动命令为 `env XDG_CURRENT_DESKTOP=Unity netease-cloud-music`

### SSH and git

- 安装 openssh git
- 创建本地ssh key：` ssh-keygen -t rsa -C "youremail@example.com"`
- 复制 `~.ssh/id_rsa.pub` 内容到github-Account settings-SSH Keys，Title随意
- 配置git，参考：https://www.runoob.com/w3cnote/git-guide.html

### Syncthing

- 安装 syncthing / syncthing-gtk
- 加入服务： `sudo systemctl enable syncthing@laodu.service`
- 启动服务： `sudo systemctl start syncthing@laodu.service`
- 本机地址： http://127.0.0.1:8384/

### 其他软件

- 微信：`yay -S wewechat` 无法运行的解决方案：alias wx='google-chrome-stable --app=https://wx.qq.com/'
- 电子书工具：calibre / pandoc / sigil / kindlegen
- 图像：gimp flashshot
- 文件传输：android-file-transfer（如果file manager不支持MTP就安装这个）
- 影音：VLC

---

## 使用中出现的问题

### dell Inspiron 13/7000

- Fn+Esc 键可以锁定F1-F12功能键。开始我以为是系统问题，google了才知道是硬件设计。
- 只有一个耳机插口，安装`alsa-utils`后，可以按F4进入capture页面，在 headphone 部分按空格，切换插口是播放还是录音

### Mate桌面更新后不显示标题栏

是marco进程无法启动，运行：

`marco --replace &`

`disown`

https://www.addictivetips.com/ubuntu-linux-tips/fix-a-frozen-mate-linux-desktop/

后续补充：每次启动都要运行一次 marco 命令，这个bug是某次更新后出现的，奇怪了。

### /boot容量不足

https://wusiyu.me/archlinux-remove-initramfs-linux-fallback-img/

参考这个贴子，是 initramfs-linux-fallback.img 这个文件太大了。而折腾 /boot 分区又太麻烦，这个100M的大小是win10默认的（？），所以按照这个帖子，编辑掉 

/etc/mkinitcpio.d/linux.preset 文件中default内容。旧：

```
# mkinitcpio preset file for the 'linux' package

ALL_config="/etc/mkinitcpio.conf"
ALL_kver="/boot/vmlinuz-linux"

PRESETS=('default' 'fallback')

#default_config="/etc/mkinitcpio.conf"
default_image="/boot/initramfs-linux.img"
#default_options=""

#fallback_config="/etc/mkinitcpio.conf"
fallback_image="/boot/initramfs-linux-fallback.img"
fallback_options="-S autodetect"
```

新：

```
# mkinitcpio preset file for the 'linux' package

ALL_config="/etc/mkinitcpio.conf"
ALL_kver="/boot/vmlinuz-linux"

PRESETS=('default')

#default_config="/etc/mkinitcpio.conf"
default_image="/boot/initramfs-linux.img"
#default_options=""
```



