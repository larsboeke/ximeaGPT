import tiktoken

class TokenCounter:
    def num_tokens_from_string(self, string: str, encoding_name = "cl100k_base") -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens
