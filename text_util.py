import re

def text_quality(text):
    total_chars = len(text)
    if total_chars == 0:
        return 0

    non_alpha = re.findall(r'[^a-zA-Z0-9\s,.!?;:áéíóúãõçÁÉÍÓÚÃÕÇ]', text)
    weird_ratio = len(non_alpha) / total_chars

    words = text.split()
    avg_word_len = sum(len(w) for w in words) / len(words) if words else 0
    avg_words_per_line = len(words) / (text.count('\n') + 1)

    return {
        'weird_char_ratio': weird_ratio,
        'avg_word_len': avg_word_len,
        'avg_words_per_line': avg_words_per_line,
        'empty': total_chars < 30
    }

def apply_ocr(text) -> list:
    """    Verifica a qualidade do texto e retorna uma lista de possíveis causas de baixa qualidade.
    Args:
        text (str): Texto a ser analisado.
    Returns:
        list: Lista de possíveis causas de baixa qualidade do texto.
    """
    couse = []
    quality = text_quality(text)
    if quality == 0:
        couse = ["texto vazio"]
        return couse
    # Verifica se a qualidade do texto é ruim e o motivo
    if quality['weird_char_ratio'] > 0.1 :
        couse.append("mais de 10% de caracteres 'estranhos'")
    if quality['avg_word_len'] < 3 :
        couse.append("palavras médias muito curtas")
    if quality['avg_words_per_line'] < 1.5:
        couse.append("média de palavras por linha muito baixa")
    if quality['empty'] :
        couse.append("página quase vazia")

    return couse
    