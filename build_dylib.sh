# 编译脚本：在带 iPhoneOS SDK 的环境下将 QishuiAuto.mm 编译为 arm64 dylib
# 请确保已准备好 SDK 路径或 theos 环境变量

SDK_PATH="/var/mobile/theos/sdks/iPhoneOS16.5.sdk"
if [ ! -d "$SDK_PATH" ]; then
    # 尝试寻找任意可用 SDK
    SDK_PATH=$(ls -d /var/mobile/theos/sdks/iPhoneOS*.sdk 2>/dev/null | head -n 1)
fi

echo "使用 SDK: $SDK_PATH"

clang++ -dynamiclib \
    -target arm64-apple-ios14.0 \
    -isysroot "$SDK_PATH" \
    -framework Foundation \
    -framework UIKit \
    -F"$SDK_PATH/System/Library/Frameworks" \
    QishuiAuto.mm \
    -o QishuiAuto.dylib

echo "编译完成：QishuiAuto.dylib"
ls -la QishuiAuto.dylib
