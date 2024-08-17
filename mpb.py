import tkinter as tk
import tkinter.messagebox as msg
import tkinter.filedialog as fdia
import json
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
from threading import Thread
from glob import glob
from pygame import mixer
from random import shuffle
from time import sleep

# 定数
APP_VERSION = "1.0.0"
CONFIG_VERSION = 1
CONFIG_PATH = "./config.json"
SETTING_ICON_PATH = os.path.join(sys._MEIPASS, "setting_icon.png")
PLAYLIST_ICON_PATH = os.path.join(sys._MEIPASS, "playlist_icon.png")
PLAYLIST_FILE_NAME = "playlist.json"

# グローバル変数
isPaused = False
isPlayList = False
isStop = False

def GetConfig(key: str):
  return config[key]

def SetConfig(key: str, value):
  config[key] = value
  with open(CONFIG_PATH, "w") as file:
    json.dump(config, file, indent=2)

def WindowClose():
  try:
    if GetConfig("windowCloseConfirm") == True:
      isWindowClose = msg.askyesno(u"確認", u"音楽プレーヤーを終了しますか？\n" +
                                  "再生中の音楽は停止します。")
      if isWindowClose:
        root.destroy()
    else:
      root.destroy()
  except:
    msg.showerror(ErrorCode(10), u"configデータのwindowCloseConfirmを読み込めませんでした。")
    root.destroy()

def ErrorCode(code: int) -> str:
  return u"エラーコード: " + str(code).zfill(4)

def GetFileName(path: str) -> str:
  return os.path.splitext(os.path.basename(path))[0]

def FileOpen():
  ftype = [(".mp3 or .json", "*")]
  iniDir = "./"
  filePath = fdia.askopenfilename(filetypes=ftype, initialdir=iniDir)
  fileForm.delete("0", tk.END)
  fileForm.insert("0", filePath)
  musTitle["text"] = GetFileName(filePath)

def PlayInit():
  playButton["text"] = u"再生中"
  playButton["state"] = tk.DISABLED
  pauseButton["state"] = tk.NORMAL
  stopButton["state"] = tk.NORMAL
  mixer.init()

def PlayFinalize():
  global isStop
  playButton["state"] = tk.NORMAL
  playButton["text"] = u"再生"
  pauseButton["text"] = u"一時停止"
  pauseButton["state"] = tk.DISABLED
  stopButton["state"] = tk.DISABLED
  isStop = False

def GetPlaylistMusicPath(playlistPath: str) -> list[str]:
  with open(playlistPath, "r") as file:
    musicListConfig = json.load(file)
  tracks = musicListConfig["tracks"]
  playlist = []
  for i in range(tracks):
    playlist.append(musicListConfig[f"music{i}"])
  return playlist

def PlayMusic():
  global isPlayList
  musicFilePathList = []
  openFilePath = fileForm.get()

  # 開いたファイルのパスが空欄なら弾く
  if openFilePath == "":
    msg.showerror(ErrorCode(0), u"ファイルが選択されていません。")
    return
  
  openFileDirName = os.path.dirname(openFilePath)
  openFileExtension = os.path.splitext(openFilePath)[1]

  if not openFileExtension == ".json":
    # 開いたファイルの拡張子がjson以外の場合
    isPlayList = False
    musicFilePathList.append(openFilePath)
  else:
    # 開いたファイルの拡張子がjsonの場合
    isPlayList = True
    musicFilePathList = GetPlaylistMusicPath(openFilePath)
    # 相対パスを絶対パスに変換
    musicFilePathList = list(map(lambda path: f"{openFileDirName}/{path}", musicFilePathList))

  def Play():
    isAlwaysPlayList = False
    PlayInit()
    playLoops = int(playCountFrom.get())
    playListLoops = 1

    # ループ回数を設定
    if isPlayList:
      if playLoops == 0:
        isAlwaysPlayList = True
      else:
        playListLoops = playLoops
    else:
      if playLoops == 0:
        playLoops = -1

    while playListLoops > 0 or isAlwaysPlayList:
      playListLoops -= 1

      # シャッフルモードならプレイリストをシャッフル
      if playOrderVar.get() == 1:
        shuffle(musicFilePathList)
      
      for path in musicFilePathList:
        musTitle["text"] = GetFileName(path)

        try:
          mixer.music.load(path)
        except:
          msg.showerror(ErrorCode(4), u"ファイルの読み込みに失敗しました。\n" +
                        u"ファイルが存在していない、または非対応のファイル形式です。")
          PlayFinalize()
          return
        
        try:
          sleep(GetConfig("musicSleepTime"))
        except:
          msg.showerror(ErrorCode(5), u"configデータのmusicSleepTimeを読み込めませんでした。")
        
        if not isPlayList:
          # 単体ファイル再生の場合
          try:
            mixer.music.play(loops=playLoops)
          except:
            msg.showerror(ErrorCode(6), u"再生に失敗しました。")
            PlayFinalize()
            return
        else:
          # プレイリスト再生の場合
          mixer.music.play(loops=1)
        
        while mixer.music.get_busy() or isPaused:
          sleep(0.1)
          if isStop:
            break
        
        if isStop:
          break
      if isStop:
        break
    PlayFinalize()
  
  Thread(target=Play).start()

def PauseMusic():
  global isPaused
  if not isPaused:
    mixer.music.pause()
    isPaused = True
    pauseButton["text"] = u"一時停止中"
  else:
    mixer.music.unpause()
    isPaused = False
    pauseButton["text"] = u"再開中"

def StopMusic():
  global isPaused, isStop
  mixer.music.stop()
  isPaused = False
  isStop = True

def OpenSettings():
  def SaveSettings():
    isWinCloseConf = winCloseConfirm.var.get()
    musicSleepTime = float(musicSleepForm.get())
    SetConfig("windowCloseConfirm", isWinCloseConf)
    SetConfig("musicSleepTime", musicSleepTime)
    msg.showinfo(u"設定", u"設定を保存しました。")
    settingMenu.destroy()
  
  settingMenu = tk.Toplevel()
  settingMenu.title(u"設定")
  settingMenu.geometry("300x230")
  settingMenu.resizable(False, False)
  settingMenu.attributes("-topmost", True)

  checkBoxFrame = tk.LabelFrame(settingMenu, width=280, height=60, relief=tk.GROOVE, bd=2, text=u"チェック設定")
  checkBoxFrame.pack_propagate(0)
  formFrame = tk.LabelFrame(settingMenu, width=280, height=60, relief=tk.GROOVE, bd=2, text=u"入力設定")
  formFrame.pack_propagate(0)
  musciSleepFram = tk.Frame(formFrame, width=300, height=30)
  musciSleepFram.pack_propagate(0)

  settingMenuTitle = tk.Label(settingMenu, text=u"設定メニュー", font=("MSゴシック", 12, "bold"))
  saveButton = tk.Button(settingMenu, text=u"設定を保存", command=SaveSettings, width=10, height=2)
  winCloseConfirmVar = tk.BooleanVar(value=GetConfig("windowCloseConfirm"))
  winCloseConfirm = tk.Checkbutton(checkBoxFrame, variable=winCloseConfirmVar, text=u"ウィンドウを閉じるときに確認メッセージを表示")
  winCloseConfirm.var = winCloseConfirmVar # 非ウィジェットの関数終了時の破棄防止
  musicSleepForm = tk.Entry(musciSleepFram, width=6)
  musicSleepForm.insert(0, GetConfig("musicSleepTime"))
  musicSleepLabel1 = tk.Label(musciSleepFram, text=u"曲と曲のインターバル: ")
  musicSleepLabel2 = tk.Label(musciSleepFram, text=u"秒")

  settingMenuTitle.pack()
  checkBoxFrame.pack()
  formFrame.pack()
  musciSleepFram.pack()
  saveButton.pack(pady=20)

  winCloseConfirm.pack()
  musicSleepLabel1.pack(side=tk.LEFT)
  musicSleepForm.pack(side=tk.LEFT)
  musicSleepLabel2.pack(side=tk.LEFT)

def OpenPlaylist():
  def OpenDir():
    playlistForm["state"] = tk.NORMAL
    playlistDir = fdia.askdirectory(initialdir="./")
    playlistFilePath = f"{playlistDir}/{PLAYLIST_FILE_NAME}"
    dirForm.delete(0, tk.END)
    dirForm.insert(0, playlistDir)
    if os.path.isfile(playlistFilePath):
      # プレイリストファイルが存在する場合
      mp3List = GetPlaylistMusicPath(playlistFilePath)
    else:
      # プレイリストファイルが存在しない場合
      mp3List = glob(f"{playlistDir}/*.mp3")
    
    playlistForm.delete(1.0, tk.END)
    for i in range(len(mp3List)):
      mp3List[i] = os.path.basename(mp3List[i])
      playlistForm.insert(tk.END, f"{i}: {mp3List[i]}\n")
    playlistForm["state"] = tk.DISABLED
  
  def CreatePlaylist():
    playlistDir = dirForm.get()
    playlistFilePath = f"{playlistDir}/{PLAYLIST_FILE_NAME}"
    order = orderEntryForm.get()
    if order == "":
      tracks = len(glob(f"{playlistDir}/*.mp3"))
      for i in range(tracks):
        order += f"{i},"
      order = order[:-1]
    
    order = order.split(",")
    order = list(map(int, order))
    if os.path.isfile(playlistFilePath):
      mp3List = GetPlaylistMusicPath(playlistFilePath)
    else:
      mp3List = glob(f"{playlistDir}/*.mp3")
      mp3List = list(map(lambda path: os.path.basename(path), mp3List))
    
    newMp3List = []
    for i in range(len(order)):
      newMp3List.append(mp3List[order[i]])

    playlistData = {"tracks": len(newMp3List)}
    for i in range(len(newMp3List)):
      playlistData.update({f"music{i}": newMp3List[i]})
    
    with open(f"{playlistDir}/playlist.json", "w") as file:
      json.dump(playlistData, file, indent=2)
    msg.showinfo(u"メッセージ", "プレイリストを作成しました。")
    playlistMenu.destroy()

  playlistMenu = tk.Toplevel()
  playlistMenu.title(u"プレイリストの作成")
  playlistMenu.geometry("300x300")
  playlistMenu.resizable(False, False)
  playlistMenu.attributes("-topmost", True)

  dirOpenFrame = tk.Frame(playlistMenu, width=300, height=30)
  dirOpenFrame.pack_propagate(0)
  playlistFormFrame = tk.Frame(playlistMenu, width=300, height=150)
  playlistFormFrame.pack_propagate(0)
  bottomFrame = tk.Frame(playlistMenu, width=300, height=100)
  bottomFrame.pack_propagate(0)
  orderEntryFrame = tk.Frame(bottomFrame, width=300, height=50)
  orderEntryFrame.pack_propagate(0)

  playlistMenuTitle = tk.Label(playlistMenu, text=u"プレイリスト作成メニュー", font=("MSゴシック", 12, "bold"))
  dirForm = tk.Entry(dirOpenFrame, width=35)
  dirOpenBtn = tk.Button(dirOpenFrame, text=u"開く", width=6, height=1, command=OpenDir)
  playlistFormTitle = tk.Label(playlistFormFrame, text=u"プレイリスト順番")
  playlistForm = tk.Text(playlistFormFrame, wrap=tk.NONE, state=tk.DISABLED, bg="#cccccc")
  orderEntryLablel = tk.Label(orderEntryFrame, text=u"順番を入力 (カンマ区切り)")
  orderEntryForm = tk.Entry(orderEntryFrame, width=35)
  createButton = tk.Button(bottomFrame, text=u"作成", width=10, height=2, command=CreatePlaylist)

  playlistMenuTitle.pack()
  dirOpenFrame.pack()
  playlistFormFrame.pack()
  bottomFrame.pack()
  orderEntryFrame.pack()

  dirForm.pack(side=tk.LEFT, padx=10)
  dirOpenBtn.pack(side=tk.LEFT, padx=10)
  playlistFormTitle.pack()
  playlistForm.pack()
  orderEntryLablel.pack()
  orderEntryForm.pack()
  createButton.pack()

def ConfigDataExist() -> bool:
  try:
    GetConfig("windowCloseConfirm")
    GetConfig("musicSleepTime")
    return True
  except:
    msg.showerror(ErrorCode(11), u"configデータの読み込みに失敗しました。")
    return False


if __name__ == "__main__":
  # config load
  try:
    with open(CONFIG_PATH, "r") as file:
      config = json.load(file)
  except:
    msg.showerror(ErrorCode(7), u"config.json が読み込めませんでした。\n" +
                  u"config.json が存在するか確認してください。")
    exit()
  
  # config version check
  try:
    if GetConfig("version") > CONFIG_VERSION:
      msg.showerror(ErrorCode(8), u"configバージョンとの互換性がありません。\n" +
                    f"config version: {GetConfig("version")}")
      exit()
  except:
    msg.showerror(ErrorCode(9), u"configデータのversionを読み込めませんでした。")
    exit()
  
  if not ConfigDataExist():
    exit()

  root = tk.Tk()
  root.title("Music Playback")
  root.geometry("400x430")
  root.resizable(False, False)
  root.iconbitmap(default=os.path.join(sys._MEIPASS, "icon.ico"))
  root.protocol("WM_DELETE_WINDOW", WindowClose)

  # ウィジェット作成
  # フレーム
  topFrame = tk.Frame(root, width=400, height=100)
  topFrame.pack_propagate(0)
  fileFrame = tk.Frame(root, width=400, height=60)
  fileFrame.pack_propagate(0)
  optFrame = tk.Frame(root, width=400, height=80)
  optFrame.pack_propagate(0)
  playOrderFrame = tk.LabelFrame(optFrame, width=120, height=80, relief=tk.GROOVE, bd=2, text=u"再生順序")
  playOrderFrame.pack_propagate(0)
  playCountFrame = tk.LabelFrame(optFrame, width=120, height=80, relief=tk.GROOVE, bd=2, text=u"再生回数")
  playCountFrame.pack_propagate(0)
  playBtnFrame = tk.Frame(root, width=400, height=80)
  playBtnFrame.pack_propagate(0)
  settingsFrame = tk.Frame(root, width=400, height=80, relief=tk.GROOVE, bd=2)
  settingsFrame.pack_propagate(0)
  versionFrame = tk.Frame(root, width=400, height=30, relief=tk.GROOVE, bd=2)
  versionFrame.pack_propagate(0)

  # トップフレーム
  appTitle = tk.Label(topFrame, text=u"音楽プレーヤー", font=("MSゴシック", 20, "bold"))
  musTitle = tk.Label(topFrame, text=u"曲名がここに表示されます", font=("MSゴシック", 12, "bold"))
  # ファイルフレーム
  fileHelp = tk.Label(fileFrame, text=u"音楽ファイルを選択：")
  fileForm = tk.Entry(fileFrame, width=55)
  fileOpenBtn = tk.Button(fileFrame, text=u"開く", command=FileOpen)
  # 再生順序フレーム
  playOrderVar = tk.IntVar()
  playOrderItem = ["順番", "シャッフル"]
  for i in range(len(playOrderItem)):
    tk.Radiobutton(playOrderFrame,
                   value=i,
                   variable=playOrderVar,
                   text=playOrderItem[i]).pack(anchor=tk.W)
  # 再生回数フレーム
  playCountFrom = tk.Spinbox(playCountFrame, width=8, justify="center", from_=0, to=999)
  playCountHelp = tk.Label(playCountFrame, text=u"0回でループ再生", font=("MSゴシック", 8, "bold"))
  # 再生ボタンフレーム
  playButton = tk.Button(playBtnFrame, text=u"再生", width=14, height=3, command=PlayMusic)
  pauseButton = tk.Button(playBtnFrame, text=u"一時停止", width=14, height=3, state=tk.DISABLED, command=PauseMusic)
  stopButton = tk.Button(playBtnFrame, text=u"停止", width=14, height=3, state=tk.DISABLED, command=StopMusic)
  # 設定フレーム
  settingIcon = tk.PhotoImage(file=SETTING_ICON_PATH)
  playlistIcon = tk.PhotoImage(file=PLAYLIST_ICON_PATH)
  settingButton = tk.Button(settingsFrame, image=settingIcon, command=OpenSettings)
  createPlaylistButton = tk.Button(settingsFrame, image=playlistIcon, command=OpenPlaylist)
  # バージョンフレーム
  version = tk.Label(versionFrame, text=f"version: {APP_VERSION}")
  author = tk.Label(versionFrame, text="author: by Clover")

  # レイアウト
  topFrame.pack()
  fileFrame.pack()
  optFrame.pack()
  playOrderFrame.pack(side=tk.LEFT, padx=10)
  playCountFrame.pack(side=tk.LEFT, padx=10)
  playBtnFrame.pack()
  settingsFrame.pack()
  versionFrame.pack()
  
  appTitle.pack(pady=20)
  musTitle.pack(side=tk.BOTTOM)
  fileHelp.pack()
  fileForm.pack(side=tk.LEFT, padx=(10, 0))
  fileOpenBtn.pack(side=tk.LEFT, padx=10)
  playCountFrom.pack(pady=8)
  playCountHelp.pack(pady=4)
  playButton.pack(side=tk.LEFT, pady=10, padx=10)
  pauseButton.pack(side=tk.LEFT, pady=10, padx=10)
  stopButton.pack(side=tk.LEFT, pady=10, padx=10)
  settingButton.pack(side=tk.LEFT, padx=10)
  createPlaylistButton.pack(side=tk.LEFT, padx=10)
  version.pack(side=tk.LEFT, padx=10)
  author.pack(side=tk.RIGHT, padx=10)

  root.mainloop()
