## 仮想環境構築
venvにて環境を構築  
```
% python3 -m venv .venv
```
一応、pipをupgrade
```
% pip install --upgrade pip
```

## Flaskのインストール
```
% pip install Flask
```
この状態でのパッケージをrequirements.txtに保存
```
% pip freeze >requirements.txt
```

## とりあえずHello World!
```
% flask --app recipt run --debug
```