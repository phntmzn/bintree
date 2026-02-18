from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Iterable, Generator, TypeVar, Generic

T = TypeVar("T")

@dataclass
class Node(Generic[T]):
    key: T
    left: Optional["Node[T]"] = None
    right: Optional["Node[T]"] = None


class BinarySearchTree(Generic[T]):
    def __init__(self, items: Optional[Iterable[T]] = None):
        self.root: Optional[Node[T]] = None
        if items:
            for x in items:
                self.insert(x)

    # -------- core ops --------

    def insert(self, key: T) -> None:
        """Insert key (ignores duplicates)."""
        if self.root is None:
            self.root = Node(key)
            return

        cur = self.root
        while True:
            if key == cur.key:
                return  # ignore duplicates
            elif key < cur.key:
                if cur.left is None:
                    cur.left = Node(key)
                    return
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = Node(key)
                    return
                cur = cur.right

    def contains(self, key: T) -> bool:
        return self.find(key) is not None

    def find(self, key: T) -> Optional[Node[T]]:
        """Return node with key, or None."""
        cur = self.root
        while cur is not None:
            if key == cur.key:
                return cur
            cur = cur.left if key < cur.key else cur.right
        return None

    def min(self) -> Optional[T]:
        cur = self.root
        if cur is None:
            return None
        while cur.left is not None:
            cur = cur.left
        return cur.key

    def max(self) -> Optional[T]:
        cur = self.root
        if cur is None:
            return None
        while cur.right is not None:
            cur = cur.right
        return cur.key

    def delete(self, key: T) -> bool:
        """Delete key if present. Returns True if deleted."""
        self.root, deleted = self._delete(self.root, key)
        return deleted

    def _delete(self, node: Optional[Node[T]], key: T) -> tuple[Optional[Node[T]], bool]:
        if node is None:
            return None, False

        if key < node.key:
            node.left, deleted = self._delete(node.left, key)
            return node, deleted
        if key > node.key:
            node.right, deleted = self._delete(node.right, key)
            return node, deleted

        # key == node.key: delete this node
        if node.left is None:
            return node.right, True
        if node.right is None:
            return node.left, True

        # Two children: replace with inorder successor (min of right subtree)
        succ_parent = node
        succ = node.right
        while succ.left is not None:
            succ_parent = succ
            succ = succ.left

        node.key = succ.key  # copy successor key into node
        # delete successor node
        if succ_parent is node:
            succ_parent.right, _ = self._delete(succ_parent.right, succ.key)
        else:
            succ_parent.left, _ = self._delete(succ_parent.left, succ.key)

        return node, True

    # -------- traversals --------

    def inorder(self) -> List[T]:
        return list(self._inorder_gen(self.root))

    def preorder(self) -> List[T]:
        return list(self._preorder_gen(self.root))

    def postorder(self) -> List[T]:
        return list(self._postorder_gen(self.root))

    def _inorder_gen(self, node: Optional[Node[T]]) -> Generator[T, None, None]:
        if node is None:
            return
        yield from self._inorder_gen(node.left)
        yield node.key
        yield from self._inorder_gen(node.right)

    def _preorder_gen(self, node: Optional[Node[T]]) -> Generator[T, None, None]:
        if node is None:
            return
        yield node.key
        yield from self._preorder_gen(node.left)
        yield from self._preorder_gen(node.right)

    def _postorder_gen(self, node: Optional[Node[T]]) -> Generator[T, None, None]:
        if node is None:
            return
        yield from self._postorder_gen(node.left)
        yield from self._postorder_gen(node.right)
        yield node.key

    # -------- utilities --------

    def height(self) -> int:
        """Height in nodes (empty tree = 0)."""
        return self._height(self.root)

    def _height(self, node: Optional[Node[T]]) -> int:
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))

    def is_valid_bst(self) -> bool:
        return self._is_valid(self.root, lo=None, hi=None)

    def _is_valid(self, node: Optional[Node[T]], lo: Optional[T], hi: Optional[T]) -> bool:
        if node is None:
            return True
        if lo is not None and node.key <= lo:
            return False
        if hi is not None and node.key >= hi:
            return False
        return self._is_valid(node.left, lo, node.key) and self._is_valid(node.right, node.key, hi)


if __name__ == "__main__":
    bst = BinarySearchTree([7, 3, 9, 1, 5, 8, 10, 4, 6])
    print("inorder:", bst.inorder())        # sorted
    print("min/max:", bst.min(), bst.max())
    print("contains 5:", bst.contains(5))
    print("height:", bst.height(), "valid:", bst.is_valid_bst())

    bst.delete(3)
    print("after delete 3:", bst.inorder())
