#!/bin/bash
# Build script for macOS App Store distribution
# This script creates a properly signed .app bundle for App Store submission

set -e

echo "Building SnapOCR for App Store..."

# Configuration
APP_NAME="SnapOCR"
BUNDLE_ID="com.snapocr.app"
VERSION="2.1.0"
BUILD_NUMBER="210"

# Required environment variables
# CODESIGN_IDENTITY: Your "Apple Distribution" certificate identity
#                  Example: "Apple Distribution: Your Name (TEAM_ID)"
# TEAM_ID: Your Apple Developer Team ID

if [ -z "$CODESIGN_IDENTITY" ]; then
    echo "ERROR: CODESIGN_IDENTITY not set"
    echo "Example: export CODESIGN_IDENTITY='Apple Distribution: Your Name (TEAM_ID)'"
    echo ""
    echo "To find your identity, run:"
    echo "  security find-identity -v -p codesigning"
    exit 1
fi

if [ -z "$TEAM_ID" ]; then
    echo "ERROR: TEAM_ID not set"
    echo "Example: export TEAM_ID='ABCDE12345'"
    echo ""
    echo "Find your Team ID at: https://developer.apple.com/account"
    exit 1
fi

# Find the correct pip command
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    echo "Error: pip not found. Please install Python first."
    exit 1
fi

echo "Using: $PIP_CMD"
echo "Code Sign Identity: $CODESIGN_IDENTITY"
echo "Team ID: $TEAM_ID"

# Install dependencies
echo "Installing dependencies..."
$PIP_CMD install -r requirements.txt
$PIP_CMD install pyinstaller

# Download UniMERNet model if not exists
if [ ! -d "models/UniMERNet" ]; then
    echo "Downloading UniMERNet model..."
    mkdir -p models
    python3 -c "
from huggingface_hub import snapshot_download
snapshot_download(repo_id='Norm/UniMERNet', local_dir='models/UniMERNet')
"
fi

# Download Tesseract and tessdata
echo "Preparing Tesseract..."
if [ ! -d "tesseract" ]; then
    mkdir -p tesseract tessdata lib

    # Copy tesseract binary
    cp $(which tesseract) tesseract/

    # Copy tessdata
    cp /opt/homebrew/share/tessdata/eng.traineddata tessdata/ 2>/dev/null || \
        curl -L -o tessdata/eng.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata
    cp /opt/homebrew/share/tessdata/chi_sim.traineddata tessdata/ 2>/dev/null || \
        curl -L -o tessdata/chi_sim.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/chi_sim.traineddata

    # Copy libraries
    brew deps tesseract | while read dep; do
        if [ -d "/opt/homebrew/opt/$dep/lib" ]; then
            cp /opt/homebrew/opt/$dep/lib/*.dylib lib/ 2>/dev/null || true
        fi
    done
fi

# Clean previous builds
rm -rf build/ dist/

# Create .app bundle with PyInstaller
echo "Building .app bundle..."
python3 -m PyInstaller \
    --name "$APP_NAME" \
    --windowed \
    --onedir \
    --hidden-import "PIL._tkinter_finder" \
    --hidden-import "pytesseract" \
    --hidden-import "mss" \
    --hidden-import "snapocr" \
    --hidden-import "snapocr.main" \
    --hidden-import "snapocr.core.config" \
    --hidden-import "snapocr.core.ocr" \
    --hidden-import "snapocr.core.clipboard" \
    --hidden-import "snapocr.platform.base" \
    --hidden-import "snapocr.platform.macos" \
    --hidden-import "snapocr.platform.macos_native" \
    --hidden-import "torch" \
    --hidden-import "torchvision" \
    --hidden-import "transformers" \
    --hidden-import "unimernet" \
    --hidden-import "numpy" \
    --add-data "snapocr:snapocr" \
    --add-data "tesseract:tesseract" \
    --add-data "tessdata:tessdata" \
    --add-data "models:models" \
    --add-binary "lib:lib" \
    --osx-bundle-identifier "$BUNDLE_ID" \
    --target-arch arm64 \
    run.py

# Path to the built app
APP_PATH="dist/$APP_NAME.app"

if [ ! -d "$APP_PATH" ]; then
    echo "Error: Failed to build .app bundle"
    exit 1
fi

# Update Info.plist
echo "Updating Info.plist..."
cat > "$APP_PATH/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>zh_CN</string>
    <key>CFBundleDisplayName</key>
    <string>SnapOCR</string>
    <key>CFBundleExecutable</key>
    <string>SnapOCR</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>CFBundleIdentifier</key>
    <string>$BUNDLE_ID</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>SnapOCR</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>$VERSION</string>
    <key>CFBundleVersion</key>
    <string>$BUILD_NUMBER</string>
    <key>LSMinimumSystemVersion</key>
    <string>11.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSHumanReadableCopyright</key>
    <string>Copyright 2024-2025 SnapOCR. All rights reserved.</string>
    <key>NSPrincipalClass</key>
    <string>NSApplication</string>
    <key>NSScreenCaptureUsageDescription</key>
    <string>SnapOCR 需要屏幕截图权限来识别屏幕上的文字内容。</string>
    <key>NSAppleEventsUsageDescription</key>
    <string>SnapOCR 使用 Apple Events 进行屏幕截图。</string>
    <key>LSApplicationCategoryType</key>
    <string>public.app-category.productivity</string>
</dict>
</plist>
EOF

# Embed provisioning profile (required for App Store)
if [ -f "SnapOCR.provisionprofile" ]; then
    echo "Embedding provisioning profile..."
    cp SnapOCR.provisionprofile "$APP_PATH/Contents/embedded.provisionprofile"
else
    echo "WARNING: SnapOCR.provisionprofile not found"
    echo "Download from: https://developer.apple.com/account/resources/profiles"
fi

# Sign all frameworks and libraries first
echo "Signing frameworks and libraries..."
find "$APP_PATH/Contents/Frameworks" -name "*.dylib" -o -name "*.so" 2>/dev/null | while read lib; do
    codesign --force --sign "$CODESIGN_IDENTITY" --options runtime --timestamp "$lib"
done

find "$APP_PATH/Contents/Frameworks" -name "*.framework" -type d 2>/dev/null | while read framework; do
    codesign --force --sign "$CODESIGN_IDENTITY" --options runtime --timestamp --deep "$framework"
done

# Sign the app bundle
echo "Signing application bundle..."
codesign --deep --force --sign "$CODESIGN_IDENTITY" \
    --options runtime \
    --timestamp \
    --entitlements "resources/SnapOCR.entitlements" \
    "$APP_PATH"

# Verify signature
echo "Verifying signature..."
codesign --verify --deep --strict --verbose=2 "$APP_PATH"

# Check entitlements
echo ""
echo "Checking entitlements..."
codesign --display --entitlements - "$APP_PATH"

# Create signed package for App Store
echo ""
echo "Creating signed package..."
PRODUCT_BUILD="$APP_NAME-$VERSION.pkg"
productbuild --component "$APP_PATH" /Applications --sign "$CODESIGN_IDENTITY" "dist/$PRODUCT_BUILD"

# Create ZIP for notarization
echo ""
echo "Creating ZIP for notarization..."
cd dist
zip -r "$APP_NAME-$VERSION.zip" "$APP_NAME.app"

echo ""
echo "=========================================="
echo "Build complete!"
echo "=========================================="
echo ""
echo "Output files:"
echo "  - App Bundle: $APP_PATH"
echo "  - Package:    dist/$PRODUCT_BUILD"
echo "  - ZIP:        dist/$APP_NAME-$VERSION.zip"
echo ""
echo "=========================================="
echo "Next Steps for App Store Submission"
echo "=========================================="
echo ""
echo "1. NOTARIZATION (Required for distribution)"
echo "   xcrun notarytool submit dist/$APP_NAME-$VERSION.zip \\"
echo "     --apple-id YOUR_APPLE_ID \\"
echo "     --team-id $TEAM_ID \\"
echo "     --password APP_SPECIFIC_PASSWORD \\"
echo "     --wait"
echo ""
echo "2. STAPLE (After notarization succeeds)"
echo "   xcrun stapler staple $APP_PATH"
echo ""
echo "3. UPLOAD TO APP STORE CONNECT"
echo "   - Open Transporter app"
echo "   - Drag and drop dist/$PRODUCT_BUILD"
echo "   - Or use: xcrun altool --upload-app -f dist/$PRODUCT_BUILD"
echo ""
echo "4. SUBMIT FOR REVIEW"
echo "   - Go to App Store Connect"
echo "   - Select your app"
echo "   - Choose the build"
echo "   - Submit for review"
echo ""
