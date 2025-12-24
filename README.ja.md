# Steam ゲーム整理ツール (Steam Game Manager)

長い間遊んでいないSteamゲームを見つけ、整理（アンインストール）するためのシンプルツールです。

![Steam Game Manager Screenshot](assets/app_screenshot.png)

[English README is here](README.md)

## 使い方

「run.bat」をダブルクリックして起動してください。

## 機能

### 1. ゲーム一覧表示
- インストールされているSteamゲームを一覧表示します。
- サイズと「最終更新日時」（最後に遊んだ日時の目安）を表示します。
- デフォルトでは、最終更新日時が古い順（最近遊んでいない順）に並んでいます。

### 2. 並び替え
- 「Size (GB)」をクリックするとサイズ順に並び替わります。
- 「Last Updated/Played」をクリックすると日付順に並び替わります。

### 3. アンインストール
- 削除したいゲームを選択します（CtrlキーやShiftキーで複数選択可能）。
- 「Uninstall Selected」ボタンをクリックします。
- Steamの公式アンインストール画面が立ち上がりますので、指示に従って削除してください。

### 4. 場所を開く
- ゲームを選択して「Open Location」をクリックすると、そのゲームのインストールフォルダが開きます。

## 動作環境

- Python 3
- "vdf" ライブラリ (`pip install -r requirements.txt` でインストール済み)
