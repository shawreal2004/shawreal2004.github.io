# shaw 的手记

Astro 6 静态个人博客。温暖的米白与鼠尾草绿配色，面向计算机视觉学习笔记与研途随笔。依赖版本已在 `pnpm-lock.yaml` 中锁定。

## 已有页面与功能

- 首页、关于我、文章列表、项目页、归档、标签页、404 页面。
- 标题/摘要/标签搜索，以及分类和标签的组合筛选。
- Markdown 写作、数学公式、代码高亮、自动目录、相邻文章导航。
- 手机适配、浅色/深色切换与偏好保存、RSS。
- 已填入 shaw chenyu、上海大学、电子信息、计算机视觉和公开邮箱。
- 三篇内容是**明确标记的示例文章**；没有编造论文成果或实验结果。

## 本地启动

在这台电脑上，双击项目文件夹中的 **`启动博客.cmd`**，即可在后台启动服务并打开浏览器。重复点击会使用已经运行的服务。每次新启动的日志分别保存在 `artifacts/blog-runs/`，文件名包含时间；`events.log` 记录启动时间、进程号和退出码，不再覆盖历史日志。

后台守护脚本会在服务以非零退出码退出时等待 5 秒重启，最多恢复 3 次；达到上限后保留日志并停止重试。电脑关机、重启或休眠时，本地网站仍无法提供访问。恢复功能不包含 Windows 开机自启，也不会停止占用端口的其他程序。

`http://127.0.0.1:4321/` 是本机地址，服务退出或电脑重启后就无法访问；重启后再次双击启动入口即可。它目前还不是公开网站，发布到 GitHub Pages 后才会有无需本地启动的访问地址。

推荐 Node.js 24 LTS 和 pnpm 11.19.0。终端进入本项目目录：

```powershell
pnpm install
pnpm dev
```

打开终端显示的本地地址，默认是 http://127.0.0.1:4321/ 。

如果已有 Node.js / npm 但没有 pnpm，可运行 `npm install -g pnpm@11.19.0` 安装 pnpm。

```powershell
pnpm check    # 检查 Astro 与 TypeScript
pnpm build    # 生成 dist 目录
pnpm preview  # 预览生成后的网站
```

## 修改个人资料

编辑 `src/data/site.ts`。姓名、学校、专业、研究兴趣、简介、邮箱、GitHub、头像和站点文案集中在这里。

- 未提供的入学年份和 GitHub 地址留空，相关字段不会展示。
- 头像放到 `public/images/avatar.jpg`，设置 `avatar: '/images/avatar.jpg'`。
- `public/favicon.svg` 是浏览器标签页图标。
- 文章分类在同一文件的 `categories` 中定义。
- `src/styles/global.css` 顶部的 CSS 变量控制配色。

“关于我”里的长段落在 `src/pages/about.astro`，可按自己的表达修改。

## 新增文章

复制 `templates/article.md` 到 `src/content/blog/`，取一个稳定的英文文件名，例如 `first-pytorch-experiment.md`。文件名会用于文章网址。

```yaml
---
title: '我的第一篇学习记录'
description: '这一篇文章主要讲什么。'
pubDate: 2026-10-05
category: '基础学习'
tags: ['PyTorch', '计算机视觉']
draft: false
demo: false
---
```

正文按照 Markdown 写作，二级和三级标题自动进入目录。日期用 `YYYY-MM-DD`。如需记录修订时间，可加 `updatedDate`。

文章必须以 **UTF-8** 编码保存。在 VS Code 右下角点击编码，选择“通过编码保存” → “UTF-8”；推荐直接使用 VS Code 编辑 Markdown。UTF-16 文件会导致文章信息解析失败，本地页面可能继续显示上一次成功加载的内容。项目包含 `.editorconfig`，供支持它的编辑器采用 UTF-8；博客也会忽略 `~$` 开头的临时 Markdown 文件。

- 分类可选：基础学习、论文阅读、实验与复现、研途随笔。
- `draft: true` 的文章不会生成文章页，也不进入列表、归档、标签和 RSS。需要发布时改成 `false`。
- 草稿仍在源代码仓库中，公开仓库里的草稿不是私密内容。私人日记应放在仓库之外。
- **未来日期不会自动延迟发布**，计划中的文章请保留 `draft: true`。
- `demo: true` 会显示示例标记和文章提示。真实文章用 `false`。
- 删除 `src/content/blog/` 中三篇示例后，就只显示自己的文章；空列表仍能正常显示。

公式可写成 `$x^2$`，独立公式用两行 `$$` 包围。代码块注明语言，例如 `python`。

图片可以与 Markdown 放在一起，用相对路径引用；相对图片会参与 Astro 的 Markdown 图片处理。需要直接访问的附件可放在 `public/`。压缩大型实验图片后再提交，模型权重和数据集不放进网站仓库。

## 发布到 GitHub Pages

项目已包含 `.github/workflows/deploy.yml`，仅部署推送到 `main` 分支的版本。

1. 在 GitHub 创建自己的仓库。个人主页推荐命名为 `你的GitHub用户名.github.io`，也支持其他仓库名。
2. 上传源码（包括 `pnpm-lock.yaml` 和 `pnpm-workspace.yaml`），排除 `node_modules`、`dist` 和 `.astro`。
3. 仓库 Settings → Pages → Build and deployment → Source 选 **GitHub Actions**。
4. 推送到 `main`，或在 Actions 页面手动运行部署工作流。
5. 部署完成后，在 Pages 页面查看网站地址。

GitHub Actions 环境下自动根据仓库名确定域名和路径：

- `username.github.io` 仓库 → `https://username.github.io/`
- `my-blog` 仓库 → `https://username.github.io/my-blog/`

自动推导仅覆盖 github.com 的常规账户，不覆盖 GitHub Enterprise 或随机私有站点域名；这类情况请显式设置 `SITE_URL` 和 `BASE_PATH`。

### 自定义域名

在仓库 Settings → Secrets and variables → Actions → Variables 设置：

- `SITE_URL`：完整域名，例如 `https://blog.example.com`。
- `BASE_PATH`：`/`（通常可留空）。

同时在 Pages 设置中绑定域名，按 GitHub 官方指南配置 DNS；创建 `public/CNAME`，内容为域名（不含协议）。推送后重新部署。

### 本地检查子路径部署

```powershell
$env:SITE_URL = 'https://example.github.io'
$env:BASE_PATH = '/my-blog'
pnpm build
pnpm preview
Remove-Item Env:SITE_URL
Remove-Item Env:BASE_PATH
```

无部署域名配置时，构建使用本地地址，便于预览。正式发布由 GitHub 环境或显式 `SITE_URL` 生成正确的 canonical 与 RSS；配置正式地址后也会生成站点地图。

## 目录

```text
src/data/site.ts          个人资料和文案
src/content/blog/        Markdown 文章
src/content.config.ts    文章字段校验
src/components/          文章卡片与首页插画
src/layouts/Base.astro   导航、页脚和主题切换
src/pages/               网站页面
src/styles/global.css    配色与排版
public/                  图标、头像与附件
templates/article.md     写作模板（不参与构建）
```

目前没有绑定 GitHub 账号，也没有上传或公开发布。上线时还需要你的 GitHub 仓库地址。

## 首版验证

- Astro 检查：17 个文件，0 错误、0 警告、0 提示。
- 生产构建：15 个页面生成成功。
- 浏览器：搜索、空结果、清除筛选、分类与标签组合筛选、主题偏好保存、公式、代码与目录锚点通过；无页面脚本错误。
- 响应式：9 个页面在 1440、390、320 像素宽度无横向溢出；19 个内部链接返回成功。
- 部署：已模拟 GitHub Pages 的 `/research-notes/` 子路径，检查页面资源、canonical、RSS 和站点地图；草稿及其独有标签未被发布。
- 依赖构建工具会输出 Markdown 旧配置和依赖注释的提示，当前不影响检查或构建成功。

本地预览截图保存在 `artifacts/`，该目录不会上传到源码仓库。
