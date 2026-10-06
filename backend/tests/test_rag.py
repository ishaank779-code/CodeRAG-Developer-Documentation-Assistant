from app.text_utils import tokenize

def test_tokenize_removes_common_words():
    assert tokenize("How can I use React components?") == ["use", "react", "components"]
