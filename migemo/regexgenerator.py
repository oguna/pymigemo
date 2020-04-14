# -*- coding: utf-8 -*-
from typing import List

from . import regexoperator


class RegexGenerator:
    class Node:
        def __init__(self, code: chr):
            self.code = code
            self.child = None
            self.next = None

        def add(self, query: str, offset: int, generated: bool):
            code = query[offset]
            node = self
            while node and node.code != code:
                node = node.next
            a = False
            if not node:
                node = RegexGenerator.Node(code)
                node.next = self
                a = True
            elif (not node.child) and (not generated):
                return self
            if len(query) == offset + 1:
                node.child = None
            else:
                generated = False
                if node.child is None:
                    node.child = RegexGenerator.Node(query[1 + offset])
                    generated = True
                node.child = node.child.add(query, offset + 1, generated)
            return node if a else self

    def __init__(self, operator: regexoperator.RegexOperator):
        self.operator = operator
        self.node: RegexGenerator.Node = None

    def add(self, word: str):
        if not word:
            return
        generated = False
        if not self.node:
            self.node = RegexGenerator.Node(word[0])
            generated = True
        self.node = self.node.add(word, 0, generated)

    def generate_stub(self, buf: List[chr], node: Node):
        escape_characters = "\\.[]{}()*+-?^$|"
        escape = '\\'
        brother = 1
        has_child = 0
        tmp = node
        while tmp:
            if tmp.next:
                brother = brother + 1
            if tmp.child:
                has_child = has_child + 1
            tmp = tmp.next
        no_child = brother - has_child

        if brother > 1 and has_child > 0:
            buf.append(self.operator.nest_in)

        if no_child > 0:
            if no_child > 1:
                buf.append(self.operator.select_in)
            tmp = node
            while tmp:
                if tmp.child:
                    tmp = tmp.next
                    continue
                if tmp.code in escape_characters:
                    buf.append('\\')
                buf.append(tmp.code)
                tmp = tmp.next
            if no_child > 1:
                buf.append(self.operator.select_out)

        # 子のあるノードを出力
        if has_child > 0:
            if no_child > 0:
                buf.append(self.operator._or)
            tmp = node
            while tmp.child is None:
                tmp = tmp.next
            while True:
                if tmp.code in escape_characters:
                    buf.append('\\')
                buf.append(tmp.code)
                if self.operator.newline:
                    buf.append(self.operator.newline)
                self.generate_stub(buf, tmp.child)
                tmp = tmp.next
                while tmp and tmp.child is None:
                    tmp = tmp.next
                if tmp is None:
                    break
                if has_child > 1:
                    buf.append(self.operator._or)
        if brother > 1 and has_child > 0:
            buf.append(self.operator.nest_out)

    def generate(self) -> str:
        if self.node is None:
            return ''
        else:
            result = []
            self.generate_stub(result, self.node)
            return ''.join(result)
