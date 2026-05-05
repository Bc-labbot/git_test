# Git学习与实践过程

## 学习资料来源及相关链接
- [Pro Git 中文版](https://git-scm.com/book/zh/v2) - 全面系统的 Git 学习资料
- [GitHub Docs](https://docs.github.com/zh) - GitHub 官方文档，涵盖仓库管理、SSH配置等
- [Git 官方文档](https://git-scm.com/docs) - 命令参考和指南
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf) - 常用指令速查表
- [廖雪峰 Git 教程](https://www.liaoxuefeng.com/wiki/896043488029600) - 入门友好

## 实践流程

### 1. 安装与初始配置
- 从 [git-scm.com](https://git-scm.com) 下载并安装 Git
- 配置用户名和邮箱：
  ```bash
  git config --global user.name "Your Name"
  git config --global user.email "your_email@example.com"
2. 创建本地仓库并添加远程
在项目文件夹初始化 Git：

bash
git init
创建项目文件（如 main.py）并提交：

bash
git add .
git commit -m "初始化项目"
查看远程仓库地址（初始为空）：

bash
git remote -v
添加远程仓库（首次使用 HTTPS 地址）：

bash
git remote add origin https://github.com/Bc-labbot/git_test.git
3. 配置 SSH 密钥并切换连接方式
生成 SSH 密钥对：

bash
ssh-keygen -t ed25519 -C "your_email@example.com"
将公钥内容添加到 GitHub 账户的 Settings → SSH and GPG keys

测试连接：

bash
ssh -T git@github.com
将远程地址从 HTTPS 修改为 SSH：

bash
git remote set-url origin git@github.com:Bc-labbot/git_test.git
4. 推送代码与问题解决
首次推送，因为远程仓库已存在初始提交（如 README.md），导致推送被拒：

bash
git push --set-upstream origin main
# 报错：non-fast-forward，需要先拉取
拉取远程内容并合并不同历史：

bash
git pull origin main --allow-unrelated-histories
处理可能出现的合并冲突，完成合并提交后再次推送：

bash
git push -u origin main
后续修改代码后，常规提交和推送：

bash
git add .
git commit -m "添加新功能"
git push
主要提交记录及说明
初始化项目 – 创建基本文件结构，包含 main.py 和 .gitignore

配置 Git 用户信息 – 添加全局用户名和邮箱配置（实际在配置文件中体现，非文件提交）

更换远程仓库地址为 SSH – 本地配置修改，未产生文件提交，但影响推送行为

合并远程 README.md – 执行 git pull --allow-unrelated-histories 后自动生成的合并提交，引入了远程原有的说明文件

添加新功能：数据处理模块 – 在 main.py 中增加数据处理函数，并提交

修复合并冲突 – 手动处理 README.md 冲突，保留双方内容并提交

（注：提交记录为实践过程中的典型操作，实际哈希值可在 git log --oneline 中查看）

遇到的问题及解决方法
问题1：fatal: The current branch main has no upstream branch.
现象：执行 git push 时提示当前分支没有设置上游分支，无法推送。
原因：本地 main 分支是新创建的，尚未与远程任何分支建立追踪关系，Git 不知道默认推送到哪里。
解决方法：使用 git push --set-upstream origin main 进行首次推送，-u 参数会在推送的同时建立上游追踪。之后就可以直接使用 git push。

问题2：! [rejected] main -> main (non-fast-forward)
现象：推送时被拒绝，提示“tip of your current branch is behind its remote counterpart”。
原因：远程仓库在创建时包含了 README.md 或 .gitignore 等初始提交，而本地仓库是独立初始化的，两者历史线没有共同祖先，导致无法快进合并。
解决方法：先拉取远程内容并允许合并不相关历史：

bash
git pull origin main --allow-unrelated-histories
解决可能出现的冲突后，提交合并，再执行推送。如果确知远程内容可以丢弃，可使用 git push --force 强制覆盖（谨慎使用）。

问题3：SSH 连接时 Permission denied (publickey)
现象：使用 git@github.com 地址克隆或推送时，提示权限被拒。
原因：本地未生成 SSH 密钥，或公钥未添加到 GitHub 账户。
解决方法：

检查 ~/.ssh 目录下是否存在密钥对（id_ed25519 / id_ed25519.pub）

若没有，用 ssh-keygen -t ed25519 -C "邮箱" 生成

将 .pub 文件内容添加到 GitHub 的 SSH and GPG keys 中

用 ssh -T git@github.com 测试，看到成功提示即可

Git学习心得
通过本次实践，我深刻体会到 Git 作为一个分布式版本控制系统的强大与灵活。从最基础的 add、commit，到分支管理、远程协作，每一步都让我对版本控制有了更清晰的认识。

实际操作中，命令行虽然初学门槛略高，但熟记几个核心命令后，工作效率明显提升。遇到推送冲突或上游分支未设置等问题时，查阅文档和错误提示往往能快速定位原因，这让我养成了先看报错信息、再搜索解决方案的习惯。

特别感触的是 Git 对历史完整性的保护机制——非快进推送被拒绝、合并冲突需手动解决，这些设计看似“麻烦”，实则是团队协作中防止代码丢失的关键。配置 SSH 密钥也让我理解了安全认证的重要性，避免了每次输入密码的繁琐。

经过这番折腾，我已能在日常项目中较熟练地使用 Git 进行版本控制和远程同步。未来计划进一步学习分支策略（如 GitFlow）、rebase 与 cherry-pick 等进阶技巧，让提交历史更加整洁清晰。