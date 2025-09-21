from flask import Flask, render_template

# 建立 Flask 應用程式實例
app = Flask(__name__)

# 建立根節點 (route)
# 當使用者連線到網站根目錄 (/) 時，會執行 home 函式
@app.route('/')
def home():
    return render_template('index.html')

# 判斷這個檔案是否被直接執行 (而不是被當作模組匯入)
if __name__ == '__main__':
    # 執行 Flask 應用程式
    # host='0.0.0.0' 表示監聽所有公開的 IP 位址，允許來自區域網路中其他裝置的連線
    # debug=True 啟用除錯模式，當程式碼變更時會自動重啟伺服器
    app.run(host='0.0.0.0', port=5000, debug=True)