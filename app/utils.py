class Base62:
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = 62

    def encoder(self, url_id):
        if url_id < 0:
            raise ValueError("Value less than 0")
        if url_id < self.base:
            return self.chars[url_id]
        return self.encoder(url_id // self.base) + self.chars[url_id % self.base]

    def decoder(self, code):
        res, length = 0, len(code)
        for i, val in enumerate(code):
            power = (length - i - 1)
            res += self.chars.find(val) * self.base ** power
        return res
