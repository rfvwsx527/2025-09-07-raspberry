# Gemini 啟動說明

本文件說明如何在 Python 環境中啟動和使用 Gemini API。

## 1. 環境準備

在啟動 Gemini 應用程式之前，請確保您的環境已正確設定。

### 1.1 建立並啟用虛擬環境 (建議)

為了避免套件衝突，強烈建議使用虛擬環境。

```bash
python3 -m venv gemini_env
source gemini_env/bin/activate
```

### 1.2 安裝必要的套件

在虛擬環境啟用後，安裝 Google Generative AI 套件：

```bash
pip install google-generativeai
```

## 2. 設定 Gemini API Key

您需要一個 Gemini API Key 才能與 Gemini 模型互動。請將您的 API Key 設定為環境變數，以確保安全性。

```bash
export GOOGLE_API_KEY="YOUR_API_KEY"
```

請將 `YOUR_API_KEY` 替換為您實際的 Gemini API Key。

## 3. 啟動 Gemini 應用程式

以下是幾種啟動 Gemini 應用程式的方式：

### 3.1 執行 Python 腳本

您可以編寫一個 Python 腳本來呼叫 Gemini API。

**範例：`gemini_example.py`**

```python
import google.generativeai as genai
import os

# 從環境變數中讀取 API Key
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# 初始化模型
model = genai.GenerativeModel('gemini-pro')

# 產生內容
response = model.generate_content("Hello, Gemini!")

# 輸出結果
print(response.text)
```

**執行方式：**

1.  確保您已啟用虛擬環境 (`source gemini_env/bin/activate`)。
2.  確保 `GOOGLE_API_KEY` 環境變數已設定。
3.  執行 Python 腳本：

    ```bash
    python gemini_example.py
    ```

### 3.2 互動式 Python Shell

您也可以在 Python 互動式 Shell 中直接與 Gemini 互動。

1.  確保您已啟用虛擬環境 (`source gemini_env/bin/activate`)。
2.  確保 `GOOGLE_API_KEY` 環境變數已設定。
3.  啟動 Python Shell：

    ```bash
    python
    ```

4.  在 Shell 中輸入以下程式碼：

    ```python
    import google.generativeai as genai
    import os

    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Tell me a story.")
    print(response.text)
    ```

### 3.3 使用 Jupyter Notebook 或 IPython (如果已安裝)

如果您安裝了 Jupyter Notebook 或 IPython，也可以在其中執行 Gemini 程式碼。

1.  確保您已啟用虛擬環境。
2.  安裝 Jupyter (如果尚未安裝)：`pip install jupyter`
3.  啟動 Jupyter Notebook：`jupyter notebook`
4.  在 Notebook 中建立一個新的 Python 檔案，並輸入上述 Python 程式碼。

---
**重要提示：**
請務必保護您的 API Key，不要將其直接硬編碼在程式碼中或公開分享。使用環境變數是推薦的做法。
