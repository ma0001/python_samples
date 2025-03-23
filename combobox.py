import tkinter as tk
from tkinter import ttk
import json
import os
import appdirs

# Tkinterで編集可能なコンボボックスを作成するクラス
# ・ユーザーが入力したものを自動で記憶して、次回からドロップダウンリストに表示
# ・選んだアイテムは自動的にリストの一番上に移動
# ・appdirsを使って前回の状態を記憶する
# ・履歴の最大はデフォルトで20

# JSONファイルからデータを読み込む関数
def load_data(app_name, defaults=None):
    """
    アプリ名に対応するJSONデータをすべて読み込む
    存在しないキーはデフォルト値で初期化する
    
    :param app_name: アプリケーション名
    :param defaults: デフォルト値の辞書 {key: default_value}
    :return: 読み込まれたデータ
    """
    data = {}
    
    # デフォルト値が指定されていれば、それでデータを初期化
    if defaults:
        data = defaults.copy()
    
    try:
        data_dir = appdirs.user_data_dir(app_name)
        data_file = os.path.join(data_dir, f"{app_name}.json")
        
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
                # 読み込んだデータで上書き
                data.update(loaded_data)
    except Exception as e:
        print(f"読み込みエラー: {e}")
    
    return data

# JSONファイルにデータを保存する関数
def save_data(app_name, data):
    """アプリ名に対応するJSONデータをすべて保存する"""
    try:
        data_dir = appdirs.user_data_dir(app_name)
        os.makedirs(data_dir, exist_ok=True)
        data_file = os.path.join(data_dir, f"{app_name}.json")
        
        # データを書き込む
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        return data_file
    except Exception as e:
        print(f"保存エラー: {e}")
        return None

class EditableComboBox:
    def __init__(self, master, items, max_items=20):
        # 参照をそのまま使用（コピーしない）
        self.items = items
        self.max_items = max_items
        
        # 最大数を超えていたら切り詰める
        while len(self.items) > self.max_items:
            self.items.pop()
        
        self.var = tk.StringVar()
        
        # コンボボックスの作成
        self.combo = ttk.Combobox(master, textvariable=self.var)
        self.combo['values'] = self.items
        
        # 最初のアイテムを選択状態にする
        if self.items:
            self.var.set(self.items[0])
            
        # イベントバインディング
        self.combo.bind('<<ComboboxSelected>>', self.on_select)
        self.combo.bind('<Return>', self.on_edit)
    
    def on_select(self, event):
        """ユーザーがリストから選択した時のハンドラ"""
        selected_item = self.var.get()
        
        # 選択したアイテムをリストの先頭に移動
        if selected_item in self.items:
            self.items.remove(selected_item)
        self.items.insert(0, selected_item)
        
        # 最大数を超えたら切り詰める
        while len(self.items) > self.max_items:
            self.items.pop()
        
        # コンボボックスの値を更新
        self.combo['values'] = self.items
            
    def on_edit(self, event):
        """ユーザーがテキストを編集して Enter キーを押した時のハンドラ"""
        edited_text = self.var.get()
        
        # 空の場合は何もしない
        if not edited_text.strip():
            return
        
        # 編集されたテキストを先頭に追加（同じものがあれば削除）
        if edited_text in self.items:
            self.items.remove(edited_text)
        
        # 先頭に追加
        self.items.insert(0, edited_text)
        
        # 最大数を超えたら切り詰める
        while len(self.items) > self.max_items:
            self.items.pop()
        
        # コンボボックスの値を更新
        self.combo['values'] = self.items
        
    def pack(self, **kwargs):
        """パックジオメトリマネージャへのショートカット"""
        self.combo.pack(**kwargs)
        
    def grid(self, **kwargs):
        """グリッドジオメトリマネージャへのショートカット"""
        self.combo.grid(**kwargs)
        
    def place(self, **kwargs):
        """プレースジオメトリマネージャへのショートカット"""
        self.combo.place(**kwargs)
        
    def get(self):
        """現在選択されているアイテムを取得"""
        return self.var.get()
        
    def get_items(self):
        """現在の選択リストを取得"""
        return self.items

# 使用例
if __name__ == "__main__":
    root = tk.Tk()
    root.title("履歴保存機能付きコンボボックス")
    
    # アプリケーション名とリスト名を定義
    APP_NAME = "MyApp"
    FRUITS_LIST = "fruits"
    COLORS_LIST = "colors"
    
    # 保存先ファイルパスの取得（表示用）
    data_dir = appdirs.user_data_dir(APP_NAME)
    data_file = os.path.join(data_dir, f"{APP_NAME}.json")
    
    # デフォルト値を辞書にまとめる
    default_values = {
        FRUITS_LIST: ["りんご", "バナナ", "みかん", "ぶどう", "いちご"],
        COLORS_LIST: ["赤", "青", "緑", "黄色", "紫"]
    }
    
    # 保存データを一度に読み込む（デフォルト値を渡して自動初期化）
    data = load_data(APP_NAME, default_values)
    
    # ラベル
    label1 = tk.Label(root, text="果物を選択または編集してね:")
    label1.pack(pady=5)
    
    # コンボボックス（参照で渡す）
    combo1 = EditableComboBox(root, data[FRUITS_LIST])
    combo1.pack(pady=5)
    
    # ラベル
    label2 = tk.Label(root, text="色を選択または編集してね:")
    label2.pack(pady=5)
    
    # 2つ目のコンボボックス（参照で渡す）
    combo2 = EditableComboBox(root, data[COLORS_LIST])
    combo2.pack(pady=5)
    
    # 選択ボタン
    def show_selection():
        selected1 = combo1.get()
        items1 = combo1.get_items()
        selected2 = combo2.get()
        items2 = combo2.get_items()
        result_label.config(text=f"果物: {selected1}\n果物リスト: {', '.join(items1)}\n"
                            f"色: {selected2}\n色リスト: {', '.join(items2)}")
    
    button = tk.Button(root, text="選択したものを表示", command=show_selection)
    button.pack(pady=5)
    
    # 結果表示用ラベル
    result_label = tk.Label(root, text="")
    result_label.pack(pady=5)
    
    # 保存ディレクトリ情報
    info_label = tk.Label(root, text=f"保存先: {data_file}", font=("", 8))
    info_label.pack(pady=5)
    
    # アプリケーション終了時にデータを保存する
    def on_closing():
        # データはすでに参照で更新されているので、そのまま保存する
        save_data(APP_NAME, data)
        root.destroy()
    
    # ウィンドウの閉じるボタンにイベントをバインド
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()
