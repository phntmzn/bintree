from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Callable, TypeVar, Generic, Iterable, Deque
from collections import deque

T = TypeVar("T")

@dataclass
class TreeNode(Generic[T]):
    value: T
    children: List["TreeNode[T]"] = field(default_factory=list)

    def add(self, child: "TreeNode[T]") -> "TreeNode[T]":
        self.children.append(child)
        return child

def dfs_preorder(root: Optional[TreeNode[T]]) -> List[T]:
    """Root, then children left-to-right."""
    out: List[T] = []
    def rec(n: TreeNode[T]) -> None:
        out.append(n.value)
        for c in n.children:
            rec(c)
    if root:
        rec(root)
    return out

def bfs_level_order(root: Optional[TreeNode[T]]) -> List[T]:
    out: List[T] = []
    if not root:
        return out
    q: Deque[TreeNode[T]] = deque([root])
    while q:
        n = q.popleft()
        out.append(n.value)
        q.extend(n.children)
    return out

# demo
if __name__ == "__main__":
    root = TreeNode("root")
    a = root.add(TreeNode("A"))
    b = root.add(TreeNode("B"))
    a.add(TreeNode("A1"))
    a.add(TreeNode("A2"))
    b.add(TreeNode("B1"))

    print("DFS:", dfs_preorder(root))
    print("BFS:", bfs_level_order(root))
