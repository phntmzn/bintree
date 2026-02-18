from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, TypeVar, Generic

T = TypeVar("T")

@dataclass
class BinNode(Generic[T]):
    value: T
    left: Optional["BinNode[T]"] = None
    right: Optional["BinNode[T]"] = None

def inorder(root: Optional[BinNode[T]]) -> List[T]:
    out: List[T] = []
    def rec(n: Optional[BinNode[T]]) -> None:
        if not n: return
        rec(n.left)
        out.append(n.value)
        rec(n.right)
    rec(root)
    return out
