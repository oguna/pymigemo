# pymigemo

[![Python package](https://github.com/oguna/pymigemo/actions/workflows/action.yml/badge.svg)](https://github.com/oguna/pymigemo/actions/workflows/action.yml)

## インストール
```
> python setup.py install
```

## テスト
```
> python setup.py test
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
'(研削|建策|羂索|献策|検索|憲[冊作]|けんさく|ｋｅｎｓａｋｕ|kensaku)'
```

## ライセンス

`migemo/dict/migemo-compact-dict` はGPLv3です。
それ以外のファイルはBSDライセンスです。