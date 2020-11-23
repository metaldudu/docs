# zsh使用笔记

## 安装

直接安装 `zsh`, `oh-my-zsh-git`

修改默认shell

	chsh -s /bin/zsh

之后需要注销当前用户

## 配置

	copy /usr/share/oh-my-zsh/zshrc ~/.zshrc

然后 `source ~/.zshrc` 更新一下


### 修改环境变量

拷贝原有bashrc的内容即可

### 主题

修改 .zshrc 主题部分，改成 

	ZSH_THEME="ys"

备选主题： agnoster / 

### 插件

### archlinux

添加了许多archlinux的命令别名（使用alias命令可以查看所有的），常用的：

- pacin='sudo pacman -S'
- pacupg='sudo pacman -Syu'
- 

#### autojump

https://github.com/wting/autojump ，待学习



----------------


todo：

1. 环境变量失效了，待修正
2. 学习用自定义alias
3. 