# Gemini CLI 啟動說明

本文件說明如何在命令列介面 (CLI) 中啟動和使用 Gemini。

## 1. 環境準備

在啟動 Gemini CLI 之前，請確保您的環境已正確設定。

### 1.1 建立並啟用虛擬環境 (建議)

為了避免套件衝突，強烈建議使用虛擬環境。

```bash
python3 -m venv gemini_env
source gemini_env/bin/activate
```

### 1.2 安裝必要的套件

在虛擬環境啟用後，安裝 Google Generative AI 套件 (如果您的 CLI 依賴此套件)：

```bash
pip install google-generativeai
```

## 2. 設定 Gemini API Key

您需要一個 Gemini API Key 才能與 Gemini 模型互動。請將您的 API Key 設定為環境變數，以確保安全性。

```bash
export GOOGLE_API_KEY="YOUR_API_KEY"
```

請將 `YOUR_API_KEY` 替換為您實際的 Gemini API Key。

## 3. 啟動 Gemini CLI

Gemini CLI 的啟動方式取決於其具體的實作。以下是一些常見的啟動方式：

### 3.1 直接執行 CLI 程式

如果 Gemini CLI 是一個獨立的可執行檔或 Python 腳本，您可以直接執行它。

**範例：**

假設您的 Gemini CLI 程式是 `gemini_cli.py` 或已安裝為 `gemini` 命令。

```bash
# 如果是 Python 腳本
python gemini_cli.py [commands] [arguments]

# 如果已安裝為命令
gemini [commands] [arguments]
```

**常見的 CLI 互動範例：**

*   **啟動互動模式：**
    ```bash
gemini chat
    ```

*   **發送單次查詢：**
    ```bash
gemini ask "What is the capital of France?"
    ```

*   **查看幫助訊息：**
    ```bash
gemini --help
    ```

### 3.2 從 Python 腳本中呼叫 (如果 CLI 提供了程式化介面)

某些 CLI 工具也可能提供 Python 程式化介面，允許您從自己的 Python 腳本中呼叫其功能。

**範例：`my_cli_script.py`**

```python
import subprocess
import os

# 確保 API Key 已設定
os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY" # 僅用於示範，實際應從環境變數讀取

# 呼叫 Gemini CLI 命令
command = ["gemini", "ask", "Tell me a short poem."]
result = subprocess.run(command, capture_output=True, text=True)

print("Stdout:", result.stdout)
print("Stderr:", result.stderr)
print("Exit Code:", result.returncode)
```

**執行方式：**

```bash
python my_cli_script.py
```

---
**重要提示：**
請務必保護您的 API Key，不要將其直接硬編碼在程式碼中或公開分享。使用環境變數是推薦的做法。

具體的 CLI 命令和參數可能因 Gemini CLI 的版本和實作而異。請參考您所使用的 Gemini CLI 的官方文件以獲取最準確的資訊。