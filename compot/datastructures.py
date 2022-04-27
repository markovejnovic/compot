#!/usr/bin/env python

from abc import abstractmethod, ABC
from dataclasses import dataclass, field
from typing import Callable, Generic, List, Any, Optional, TypeVar


class Tree(ABC):
    @abstractmethod
    def apply(self, predicate: Callable[[Any], Any]) -> 'Tree':
        """Traverses through the tree applying the callable."""


TreeNode = TypeVar('TreeNode')

@dataclass
class GeneralTree(Tree, Generic[TreeNode]):
    node: TreeNode
    children: List[Tree] = field(default_factory=lambda: [])

    def apply(self, predicate: Callable[[TreeNode], Any]) -> 'Tree':
        """DFS traverses through the tree applying the callable."""
        new_tree = GeneralTree(
            predicate(self.node),
            [c.apply(predicate) for c in self.children]
        )

        return new_tree

    def __str__(self) -> str:
        return (f'GTree<node={self.node}, '
                f'children={[str(c) for c in self.children]}>')
