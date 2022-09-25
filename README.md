# pymigemo

[![Python CI](https://github.com/oguna/pymigemo/actions/workflows/action.yml/badge.svg)](https://github.com/oguna/pymigemo/actions/workflows/action.yml)
[![PyPI version](https://badge.fury.io/py/pymigemo.svg)](https://badge.fury.io/py/pymigemo)

## インストール
```
> pip install pymigemo
```

## CLIで実行

```
> pymigemo
> QUERY: kensaku
PATTERN: (研削|建策|羂索|献策|検索|憲[冊作]|けんさく|ｋｅｎｓａｋｕ|kensaku)
```

## スクリプトから利用

```
> python
>>> import migemo
>>> m = migemo.Migemo()
>>> m.query("kensaku")
'(賢作|謙作|腱索|羂索|研削|県作|献策|検索|憲作|建策|兼作|健[策作]|けんさく|ｋｅｎｓａｋｕ|kensaku)'
```

## ライセンス

BSDライセンスの辞書ファイルを同梱しています。

パッケージ全体はBSDライセンスで配布しています。