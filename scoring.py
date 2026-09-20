

def decode(message):

    words = message.split()
    translated_count = 0

    for word in words:

        if word.isdigit():           # all digits = still an alien code
            continue

        translated_count = translated_count + 1

    return translated_count / len(words)