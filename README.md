---

# MPB 音楽プレイヤー

**バージョン**: 1.0.0  
**作者**: Clover

MPB音楽プレイヤーをダウンロードいただき、ありがとうございます。本READMEでは、MPBの使い方や設定方法について説明します。

## 目次
1. [動作環境](#動作環境)
2. [ファイル一覧](#ファイル一覧)
3. [インストール手順](#インストール手順)
4. [操作方法](#操作方法)
5. [プレイリストファイルについて](#プレイリストファイルについて)
6. [config.jsonファイルについて](#configjsonファイルについて)
7. [既知の問題と解決策](#既知の問題と解決策)
8. [ライセンス情報](#ライセンス情報)
9. [お問い合わせ](#お問い合わせ)

## 動作環境
MPB音楽プレイヤーを正常に動作させるための最低要件は以下の通りです:

- **OS**: Windows 10以上
- **RAM**: 2GB以上
- **サウンドカード**: 標準サウンドカード

## ファイル一覧
MPB音楽プレイヤーには、以下のファイルが含まれています:

- `mpb.exe`
- `config.json`
- `Sample_play_list`
  - `playlist.json`
- `Readme.txt`

## インストール手順
1. ダウンロードしたファイルを解凍します。
2. `mpb.exe`を任意のディレクトリに配置します。
3. 必要に応じて、`config.json`を編集してください（詳細は[config.jsonファイルについて](#configjsonファイルについて)を参照）。

## 操作方法
1. `mpb.exe`を実行して、MPB音楽プレイヤーを起動します。
2. 画面右下の「開く」ボタンをクリックし、ファイル選択ウィンドウを表示します。
3. 再生したい音楽ファイル（mp3形式）またはプレイリストファイル（json形式）を選択します。
4. 再生ボタンをクリックすると、音楽が再生されます。

   - **一時停止ボタン**: 音楽を一時的に停止します。再度クリックで再生が再開します。
   - **停止ボタン**: 音楽の再生を完全に停止します。
   
5. オプション設定で、再生順序や再生回数をカスタマイズできます。

## プレイリストファイルについて
プレイリストファイルは、複数の音楽ファイルを一つのリストとして管理するjson形式のファイルです。`mpb.exe`から簡単に作成できます。

### プレイリストファイルの構造
プレイリストファイルは以下のような構造を持ちます:

```json
{
  "tracks": 3,
  "music0": "song1.mp3",
  "music1": "song2.mp3",
  "music2": "song3.mp3"
}
```

**注意**: プレイリストファイルと同じディレクトリに音楽ファイルを配置してください。

具体的な例として、付属の`playlist.json`をご参照ください。

## config.jsonファイルについて
`config.json`はMPB音楽プレイヤーの設定ファイルです。以下の項目を変更できます:

- `"windowCloseConfirm": true`  
  - **説明**: ソフト終了時に確認画面を表示するかどうか。
  
- `"musicSleepTime": 2.0`  
  - **説明**: 曲と曲の間のインターバル時間（秒単位）。
  
- `"version": 1`  
  - **説明**: configファイルのバージョン。

## 既知の問題と解決策
- **音楽ファイルが再生されない**  
  - **対策**: mp3ファイルが正しく配置されているか確認してください。また、ファイル名に特殊文字が含まれていないか確認してください。

- **プレイリストが正しく読み込まれない**  
  - **対策**: プレイリストファイルがjson形式で正しく記述されているか確認してください。

## ライセンス情報
MPB音楽プレイヤーは[MITライセンス](https://opensource.org/licenses/MIT)の下で配布されています。詳細についてはLICENSEファイルをご覧ください。

## お問い合わせ
何かご不明な点がございましたら、以下の方法でお問い合わせください:

- **Discord**: holo_clover
- **メール**: fkokiff@gmail.com

---
