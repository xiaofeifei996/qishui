#include <stdio.h>
#include <objc/runtime.h>
#include <objc/message.h>
#include <dispatch/dispatch.h>
#include <CoreFoundation/CoreFoundation.h>

// 声明底层函数
extern "C" {
    id objc_msgSend(id, SEL, ...);
}

// 自动点击逻辑
static void runAutoClicker() {
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(3.0 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
        NSLog(@"[QishuiAutoDylib] 插件开始运行，寻找目标视图...");
        
        // 1. 获取主窗口
        Class UIApplicationClass = objc_getClass("UIApplication");
        id sharedApp = ((id (*)(id, SEL))objc_msgSend)((id)UIApplicationClass, sel_registerName("sharedApplication"));
        id keyWindow = ((id (*)(id, SEL))objc_msgSend)(sharedApp, sel_registerName("keyWindow"));
        if (!keyWindow) {
            // 兼容 iOS 13+ 获取 window 方式
            id windows = ((id (*)(id, SEL))objc_msgSend)(sharedApp, sel_registerName("windows"));
            if (windows) {
                NSUInteger count = ((NSUInteger (*)(id, SEL))objc_msgSend)(windows, sel_registerName("count"));
                if (count > 0) {
                    keyWindow = ((id (*)(id, NSUInteger, SEL))objc_msgSend)(windows, sel_registerName("objectAtIndex:"), 0);
                }
            }
        }
        
        if (keyWindow) {
            NSLog(@"[QishuiAutoDylib] 成功获取主窗口，执行自动化点击巡检");
        }
    });
}

// Constructor 构造函数，在 dylib 加载时自动执行（不经过越狱插件加载器，纯 Mach-O 注入加载）
__attribute__((constructor)) static void entry() {
    NSLog(@"[QishuiAutoDylib] 动态库已成功通过巨魔/注入方式加载！");
    
    // 延迟 2 秒等 App 完全启动
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(2.0 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
        runAutoClicker();
    });
}
