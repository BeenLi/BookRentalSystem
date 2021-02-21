img = b'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'