# -*- coding: utf-8 -*-
"""
汽水音乐 iOS 自动化点击脚本（越狱本地运行版）
基于 Frida / Objective-C 运行时或在本地配合辅助点击。
由于用户在设备上已有 frida-server 17.26.1 运行，这里提供一个直接通过 Python + Frida 
在越狱 iOS 上自动寻找和点击汽水音乐广告按钮的脚本（免 ADB，直接操作越狱本机）。
"""
import sys
import time

try:
    import frida
except ImportError:
    print("请先安装 frida 客户端: pip install frida frida-tools")
    sys.exit(1)

BUNDLE_ID = "com.soda.music"  # 汽水音乐包名

JS_CODE = """
console.log("=== 汽水音乐自动化脚本已注入 ===");

function clickClass(className) {
    try {
        var cls = ObjC.classes[className];
        if (!cls) return false;
        
        // 尝试寻找视图并触发点击
        var views = ObjC.chooseSync(cls);
        for (var i = 0; i < views.length; i++) {
            var v = views[i];
            // 检查是否在窗口中可见
            if (v.window() != null) {
                console.log("找到目标视图: " + className + ", 尝试触发点击/action");
                // 常见广告按钮触发方式
                if (typeof v.onClick === 'function') {
                    v.onClick();
                    return true;
                } else if (typeof v.onTapGesture === 'function') {
                    v.onTapGesture(null);
                    return true;
                } else if (typeof v.clonedTap === 'function') {
                    v.clonedTap();
                    return true;
                }
            }
        }
    } catch(e) {
        // ignore
    }
    return false;
}

setInterval(function() {
    // 定期检查开屏广告跳过按钮、奖励领取按钮等
    clickClass("STAd.SplashAdSkipButton");
    clickClass("STAd.FeedRewardEntranceView");
}, 1000);
"""

def on_message(message, data):
    if message['type'] == 'send':
        print(f"[*] {message['payload']}")
    elif message['type'] == 'error':
        print(f"[!] {message['stack']}")

def main():
    print(f"正在附加到 {BUNDLE_ID} ...")
    try:
        session = frida.attach(BUNDLE_ID)
    except Exception as e:
        print(f"附加失败: {e}。提示：该 App 可能有反调试，请尝试用 spawn 模式启动。")
        print("正在尝试 spawn 模式...")
        pid = frida.get_usb_device().spawn([BUNDLE_ID])
        session = frida.get_usb_device().attach(pid)
        frida.get_usb_device().resume(pid)

    script = session.create_script(JS_CODE)
    script.on('message', on_message)
    script.load()
    print("[+] 脚本运行中，按 Ctrl+C 退出...")
    
    try:
        sys.stdin.read()
    except KeyboardInterrupt:
        print("退出。")

if __name__ == '__main__':
    main()
