import pytest

class TestPrase:
    def test_inp_phrase(self):
        phrase = input("Set a phrase: ")
        assert len(phrase) <= 15, "Введенная фраза имеет больше 15 символов"