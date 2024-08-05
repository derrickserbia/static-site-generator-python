import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    def test_constructor(self):
        html_node = HTMLNode("div", "testing", None, None)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(html_node.value, "testing")
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, None)

    def test_props_to_html_prop_is_none(self):
        html_node = HTMLNode("div", "this is a div", None, None)
        expected_props = ""
        self.assertEqual(html_node.props_to_html(), expected_props)

    def test_props_to_html_prop_is_empty(self):
        html_node = HTMLNode("div", "this is a div", None, "")
        expected_props = ""
        self.assertEqual(html_node.props_to_html(), expected_props)

    def test_props_to_html_prop_is_not_specified(self):
        html_node = HTMLNode("div", "this is a div")
        expected_props = ""
        self.assertEqual(html_node.props_to_html(), expected_props)

    def test_props_to_html_single_prop(self):
        html_node = HTMLNode("link", "this is a link", None, {"href": "https://boot.dev"})
        expected_props = " href=\"https://boot.dev\""
        self.assertEqual(html_node.props_to_html(), expected_props)
    
    def test_props_to_html_multiple_prop(self):
        html_node = HTMLNode("link", "this is a link", None, {"href": "https://boot.dev", "target": "_blank"})
        expected_props = " href=\"https://boot.dev\" target=\"_blank\""
        self.assertEqual(html_node.props_to_html(), expected_props)

class TestLeafNode(unittest.TestCase):
    def test_constructor(self):
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "This is a paragraph")

    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph")
        expected = "<p>This is a paragraph</p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected = "<a href=\"https://www.google.com\">Click me!</a>"
        self.assertEqual(node.to_html(), expected)

class TestParentNode(unittest.TestCase):
    def test_parent_without_children(self):
        with self.assertRaises(ValueError):
            parent = ParentNode("p", None, None)
            self.assertEqual(parent.to_html(), "<p></p>")
    
    def test_parent_with_one_child(self):
        child = LeafNode("p", "this is a child paragraph")
        parent = ParentNode("div",  [child])
        self.assertEqual(parent.to_html(), "<div><p>this is a child paragraph</p></div>")

    def test_parent_with_children(self):
        child_1 = LeafNode("p", "this is child paragraph 1")
        child_2 = LeafNode("p", "this is child paragraph 2")
        parent = ParentNode("div", [child_1, child_2])
        self.assertEqual(parent.to_html(), "<div><p>this is child paragraph 1</p><p>this is child paragraph 2</p></div>")

    def test_parent_with_children_complex(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parent_within_parent_with_children(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ]
                )
            ],
            {"class": "bold"}
        )
        expected = "<div class=\"bold\"><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>"
        self.assertEqual(node.to_html(), expected)

        