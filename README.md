# Trip Planner

手机上编辑行程 → 一键导出静态 HTML（含地图）→ 推到 GitHub → Cloudflare Workers 自动部署给同行的人看。
纯静态、无后端、无登录，数据存在浏览器 localStorage。

## 目录

```
public/
  index.html               ← 编辑器（你自己用，已内置「广州西关六日」）
  t/guangzhou-2027.html    ← 导出的行程（给同行的人看，只读）
  404.html
src/                       ← 源码（改 app 才需要）
  app.html  sample.py  build.py
wrangler.jsonc             ← Workers 静态资源设定
package.json               ← 只有重新 build 才用到（leaflet）
```

## 第一次部署（沿用你现在的 GitHub + Cloudflare Workers）

1. 在 GitHub 建一个新 repo（例如 `trip-planner`），把这整个文件夹推上去。
2. Cloudflare 后台 → Workers & Pages → Create → **Import a repository** → 选这个 repo。
   - Build command：留空
   - Deploy command：`npx wrangler deploy`（默认值）
3. 部署完：
   - 编辑器：`https://trip-planner.<你的子域>.workers.dev`（iPhone 可「添加到主屏幕」）
   - 广州行程：`https://trip-planner.<你的子域>.workers.dev/t/guangzhou-2027`

> Worker 名称来自 `wrangler.jsonc` 的 `name`，想改网址就改这里。

## 日常使用

1. 打开编辑器，右下角 ✎ 进入编辑模式，改天／地点／交通／备忘／行李。
2. 地点的地图位置：编辑地点 → 「地图位置」里搜索或直接点地图；也可以在编辑模式下直接拖动当天地图上的编号标记。
3. 右上「⤓ 导出」→ 下载 `<代号>.html`，放进 repo 的 `public/t/`，commit + push。
   手机上也行：GitHub App／网页 → `public/t` → Add file → Upload files（同名覆盖）。
4. 约 1 分钟后同一个网址就是新版本。

## 地图说明

- 底图用高德瓦片（大陆、海外都能加载，不需要 API key），坐标是高德坐标系（GCJ-02）。
- 坐标只用来画地图；「高德地图」按钮仍用「搜索词＋城市」唤起高德 App，导航以高德搜到的为准。
- 内置广州行程的坐标来自 OpenStreetMap，餐厅大多是**近似位置**（误差可能一两百米），在编辑模式拖一下即可修正。
- Leaflet 已经打包进 HTML，不依赖任何 CDN。

## 注意

- **备份**：数据只在这个浏览器里。换手机、清 Safari 数据前，先在「我的行程」→「备份全部」存 JSON；之后用「导入 JSON」还原。
- **模板**：「我的行程」→「复制当模板」会复制整个行程（行李勾选会清空），再改标题和出发日期即可，所有日期自动顺延。
- 编辑器网址谁都能打开，但每个人看到的都是自己浏览器里的资料，看不到你的行程。

## 修改 app 后重新 build

```
npm install
npm run build      # 把 src/app.html + leaflet + 内置行程打包成 public/index.html
```
