from papan import papan


def main():
    print("selamat datang di permaian Pencarian Kata")
    size = input(
        "inputkan ukuran Grid (Default = 20x20): ")
    color = input("Color (Return/Enter for Default): ")
    file_name = input(
        "inputkan Nama File apabila ingin menggunakan file baru dibuat (Return/Enter untuk memakai kumpulan_kata.txt sebagai default): ")
    check = "a"
    words = []
    while check:
        check = input(
            "(Kosongkan dan kembali/Enter untuk langsung menjalankan sistem): ")
        words.append(check)

    size = int(size) if size else 20
    color = color if color else "orange"
    file_name = file_name if file_name else "kumpulan_kata.txt"
    words = words[:-1] if words[:-1] else None

    papan(size=size, color=color, file_name=file_name, words=words)


if __name__ == "__main__":
    main()
