# QishuiAuto TrollStore Dylib

这是一个专为巨魔（TrollStore）注入设计的原生 Objective-C 动态库（`.dylib`），用于在**无越狱环境（绕过越狱检测）**下自动跳过汽水音乐的开屏广告、自动点击“领取奖励”等。

## 文件说明
- `QishuiAuto.mm`：核心源码，利用 `__attribute__((constructor))` 在 App 加载时自动初始化，并通过纯 ObjC 运行时巡检并触发点击。
- `.github/workflows/build_dylib.yml`：GitHub Actions 自动编译配置。

## 如何使用 GitHub Actions 编译

1. 将本仓库推送到您的 GitHub 个人账号（例如 `xiaofeifei996/qishui` 或新建一个仓库）。
2. 进入 GitHub 仓库的 **Actions** 页面，手动触发一次 `Build QishuiAuto Dylib` 工作流。
3. 等待编译完成后，在 Actions 运行详情页面下方的 **Artifacts** 处下载 `QishuiAuto-dylib` 压缩包，解压即可得到 `QishuiAuto.dylib`。
4. 使用巨魔注入工具（或通过脚本解包 IPA）将该 `.dylib` 注入到汽水音乐安装包中。
