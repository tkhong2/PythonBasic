import pandas as pd
import re
import difflib
import numpy as np
from rich.console import Console
from rich.table import Table
import json

ListBooks = []
ListCustomers = []
ListOrders = []
Books = {}
Customers = {}
Orders = {}


def readFileJson(ListBooks,ListCustomers):
    csl = Console()
    found = False
    try:
        found = True
        with open('book.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for value in data:
                Books = {
                    'id': value['id'],
                    'name': value['name'],
                    'author': value['author'],
                    'publicationYear': value['publicationYear'],
                    'quantity': value['quantity'],
                    'price': value['price']
                }
                ListBooks.append(Books)
    except FileNotFoundError:
        print("File book.json không tồn tại.")
    except json.JSONDecodeError:
        print("Lỗi định dạng trong file book.json")
    try:
        found = True
        with open('customer.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for customer in data:
                Customers = {
                    'id': customer['id'],
                    'name': customer['name'],
                    'phone': customer['phone'],
                    'email': customer['email'],
                    'gender':customer['gender'],
                    'address': customer['address'],
                    'total': customer['total'],
                    'history': customer['history']
                }
                    
                ListCustomers.append(Customers)
    except FileNotFoundError:
        print("File customer.json không tồn tại.")
    except json.JSONDecodeError:
        print("Lỗi định dạng trong file customer.json")
    if not found:
        csl.print("[bold red]Lỗi đọc file json")
    else:
        csl.print("[bold green]Đọc file json thành công")
def Menu():
    print("==========================================")
    print("=======QUẢN LÝ CỬA HÀNG SÁCH ONLINE=======")
    print("==========================================")
    print("1. Thêm sách mới.")
    print("2. Hiển thị thông tin sách.")
    print("3. Tìm kiếm sách theo mã hoặc tên sách.")
    print("4. Sửa sách theo mã hoặc tên sách.")
    print("5. Xóa sách theo mã hoặc tên sách.")
    print("6. Tổng số lượng tất cả sách trong kho.")
    print('7. Sách có giá tiền cao nhất và thấp nhất.')
    print('8. Sách có năm xuất bản lâu đời nhất và mới nhất.')
    print('9. Tác giả sáng tác nhiều sách nhất')
    print('10. Sắp xếp sách theo giá tiền (từ nhỏ đến lớn)')
    print('11. Thêm khách hàng')
    print('12. Danh sách khách hàng')
    print('13. Tìm kiếm khách hàng theo mã hoặc tên khách hàng')
    print('14. Sửa khách hàng theo mã hoặc tên khách hàng')
    print('15. Xóa khách hàng theo mã hoặc tên khách hàng')
    print('16. Tạo đơn hàng bán sách theo mã')
    print('17. Xem lịch sử mua hàng khách hàng theo mã')
    print('18. Danh sách lịch sử mua hàng của các khách hàng')
    print('19. Tổng doanh thu bán bán sách')
    print('20. Ghi danh sách khách hàng, sách, đơn hàng ra file excel')
    print('21. Sắp xếp đơn hàng có giá tiền từ nhỏ đến lớn')
    print('22. Lấy dữ liệu từ file (.json)')
    print("0. Thoát")

def addBook():
    n = 0
    while True:
        try:
            n = int(input('Nhập vào số lượng sách mà bạn muốn: '))
            if n <= 0:
                print("Số lượng phải là số dương. Vui lòng nhập lại.")
                continue
            break
        except ValueError:
            print("Lỗi: Vui lòng nhập số nguyên hợp lệ.")
    for i in range(n):  
        print(f"\nNhập thông tin sách thứ {i+1}:")
        while True:
            id = input("Nhập vào mã sách: ").strip()
            if id != "":
                if any(book['id'] == id for book in ListBooks):
                    print("Mã sách đã tồn tại. Vui lòng nhập mã khác.")
                    continue
                else:
                    break
            else:
                print("Mã sách không được để trống. Vui lòng nhập lại.")
        while True:
            nameBook = input("Nhập tên sách: ").strip()
            if nameBook != "":
                if any(book['name'] == nameBook for book in ListBooks):
                    print("Tên sách đã tồn tại. Vui lòng nhập tên khác.")
                    continue
                else:
                    break
            else:
                print("Tên sách không được để trống. Vui lòng nhập lại.")
        while True:
            bookAuthor = input("Nhập tác giả: ").strip()
            if bookAuthor != "":
                break
            else:
                print("Tên tác giả không được để trống. Vui lòng nhập lại.")
        while True:
            try:
                publication_year = int(input("Nhập năm xuất bản: "))
                if len(str(publication_year)) == 4 :
                    break
                else:
                    print("Năm xuất bản phải lớn hơn 0. Vui lòng nhập lại.")
            except ValueError:
                print("Lỗi: Vui lòng nhập năm xuất bản hợp lệ (số nguyên).")
        while True:
            try:
                price = float(input("Nhập giá sách: "))
                if price > 0:
                    break
                else:
                    print("Giá sách phải lớn hơn 0. Vui lòng nhập lại.")
            except ValueError:
                print("Lỗi: Vui lòng nhập giá sách hợp lệ (số thực).")
        while True:
            try:
                quantity = int(input("Nhập số lượng: "))
                if quantity > 0:
                    break
                else:
                    print("Số lượng sách phải lớn hơn 0. Vui lòng nhập lại.")
            except ValueError:
                print("Lỗi: Vui lòng nhập số lượng hợp lệ (số nguyên).")
        Books = {
            "id": id,
            "name": nameBook,
            "author": bookAuthor,
            "publicationYear": publication_year,
            "price": price,
            "quantity": quantity
        }
        ListBooks.append(Books)
    
    return ListBooks

def displayBooks():
    console = Console()
    if len(ListBooks) == 0:
        console.print("[bold red]Danh sách sách trống.[/bold red]")
        return
    table = Table(title="Danh sách các sách đã nhập")
    table.add_column("Mã Sách", style="white", no_wrap=True)
    table.add_column("Tên Sách", style="white")
    table.add_column("Tác Giả", style="white")
    table.add_column("Năm Xuất Bản", style="white")
    table.add_column("Giá", style="white")
    table.add_column("Số lượng", style="white")
    for book in ListBooks:
        table.add_row(str(book['id']), str(book['name']), str(book['author']),str(book['publicationYear']), str(book['price']),str(book['quantity']))
    console.print(table)
    
def searchBook(ListBooks):
    console = Console()
    search_type = input("Bạn muốn tìm kiếm bằng mã sách (1) hay tên sách (2)? Nhập 1 hoặc 2: ").strip()
    if search_type == '1':
        id = input("Nhập mã sách cần tìm: ").strip()
        found_books = [book for book in ListBooks if book['id'] == id]
        if found_books:
            console.print(f"\n[bold yellow]Kết quả tìm kiếm cho mã sách:[/bold yellow] [bold green]{id}[/bold green]")
            table = Table(title="Kết quả tìm kiếm")
            table.add_column("Tên sách", style="white")
            table.add_column("Tác giả", style="white")
            table.add_column("Năm xuất bản", style="white")
            table.add_column("Giá tiền", style="white")
            table.add_column("Số lượng", style="white")
            for book in found_books:
                table.add_row(book['name'], book['author'], str(book['publicationYear']), str(book['price']), str(book['quantity']))
            console.print(table)
            return found_books[0]
        else:
            console.print("[bold red]Không tìm thấy sách với mã sách này.[/bold red]")
    elif search_type == '2':
        name = input("Nhập tên sách cần tìm: ").strip()
        found_books = [book for book in ListBooks if re.search(name, book['name'], re.IGNORECASE)]
        if found_books:
            console.print(f"\n[bold yellow]Kết quả tìm kiếm cho từ khóa:[/bold yellow] [bold green]{name}[/bold green]")
            table = Table(title="Kết quả tìm kiếm")
            table.add_column("Mã sách", style="white")
            table.add_column("Tác giả", style="white")
            table.add_column("Năm xuất bản", style="white")
            table.add_column("Giá tiền", style="white")
            table.add_column("Số lượng", style="white")
            for book in found_books:
                table.add_row(book['id'], book['author'], str(book['publicationYear']), str(book['price']), str(book['quantity']))
            console.print(table)
            return found_books[0]
        else:
            book_names = [book['name'] for book in ListBooks]
            close_matches = difflib.get_close_matches(name, book_names, n=3, cutoff=0.6)
            if close_matches:
                console.print(f"\n[bold red]Không tìm thấy sách với tên:[/bold red] [bold green]{name}[/bold green], nhưng có thể bạn muốn tìm:")
                table = Table(title="Kết quả gần đúng")
                table.add_column("Tên sách", style="white")
                table.add_column("Tác giả", style="white")
                table.add_column("Năm xuất bản", style="white")
                table.add_column("Giá tiền", style="white")
                table.add_column("Số lượng", style="white")
                for match in close_matches:
                    for book in ListBooks:
                        if book['name'] == match:
                            table.add_row(book['name'], book['author'], str(book['publicationYear']), str(book['price']), str(book['quantity']))
                            break
                console.print(table)
                return found_books[0]
            else:
                console.print(f"[bold red]Không tìm thấy sách với tên '{name}'.[/bold red]")
    else:
        console.print("[bold red]Lựa chọn không hợp lệ. Vui lòng nhập 1 hoặc 2.[/bold red]")

def updateBookInfo(book):
    print("\nBạn muốn sửa thông tin gì?")
    print("1. Tên sách")
    print("2. Tác giả")
    print("3. Năm xuất bản")
    print("4. Giá tiền")
    print("5. Số lượng")
    print("6. Sửa tất cả")
    choice = input("Nhập lựa chọn của bạn (1-6): ").strip()
    if choice == '1':
        book['name'] = str(input("Nhập tên sách mới: "))
    elif choice == '2':
        book['author'] = str(input("Nhập tác giả mới: "))
    elif choice == '3':
        book['publicationYear'] = int(input("Nhập năm xuất bản mới: "))
    elif choice == '4':
        book['price'] = float(input("Nhập giá tiền mới: "))
    elif choice == '5':
        book['quantity'] = int(input("Nhập số lượng mới: "))
    elif choice == '6':
        book['name'] = str(input("Nhập tên sách mới: "))
        book['author'] = str(input("Nhập tác giả mới: "))
        book['publicationYear'] = input("Nhập năm xuất bản mới: ")
        book['price'] = float(input("Nhập giá tiền mới: "))
        book['quantity'] = int(input("Nhập số lượng mới: "))
    else:
        print("Lựa chọn không hợp lệ.")

def updateBook(ListBooks):
    console = Console()
    search_type = input("Bạn muốn sửa sách bằng mã sách (1) hay tên sách (2)? Nhập 1 hoặc 2: ").strip()
    if search_type == '1':
        id = input("Nhập mã sách cần sửa: ").strip()
        found_books = [book for book in ListBooks if book['id'] == id]
        if found_books:
            console.print("\n[bold yellow]Kết quả tìm kiếm chính xác:[/bold yellow]")
            table = Table(title="Sách tìm thấy")
            table.add_column("STT", style="white")
            table.add_column("Tên sách", style="white")
            table.add_column("Tác giả", style="cyan")
            table.add_column("Năm xuất bản", style="green")
            table.add_column("Giá tiền", style="yellow")
            table.add_column("Số lượng", style="blue")
            for i, book in enumerate(found_books):
                table.add_row(str(i+1), book['name'], book['author'], str(book['publicationYear']), str(book['price']), str(book['quantity']))
            console.print(table)
            confirm = input("Bạn có chắc chắn muốn sửa tất cả sách này? (y/n): ").strip().lower()
            if confirm == 'y':
                for book in found_books:
                    updateBookInfo(book)  
                console.print("[bold green]Sửa thông tin sách thành công.[/bold green]")
            else:
                console.print("[bold yellow]Hủy bỏ thao tác sửa.[/bold yellow]")
        else:
            console.print("[bold red]Không tìm thấy mã sách.[/bold red]")
    elif search_type == '2':
        name = input("Nhập tên sách cần sửa: ").strip()
        found_books = [book for book in ListBooks if re.search(name, book['name'], re.IGNORECASE)]
        close_matches = []
        if not found_books:
            book_names = [book['name'] for book in ListBooks]
            close_matches = difflib.get_close_matches(name, book_names, n=3, cutoff=0.6)
        if found_books:
            console.print("\n[bold yellow]Kết quả tìm kiếm chính xác:[/bold yellow]")
            table = Table(title="Sách tìm thấy")
            table.add_column("STT", style="white")
            table.add_column("Tên sách", style="white")
            table.add_column("Tác giả", style="cyan")
            table.add_column("Năm xuất bản", style="green")
            table.add_column("Giá tiền", style="yellow")
            table.add_column("Số lượng", style="blue")
            for i, book in enumerate(found_books):
                table.add_row(str(i+1), book['name'], book['author'], str(book['publicationYear']), str(book['price']), str(book['quantity']))
            console.print(table)
            confirm = input("Bạn có chắc chắn muốn sửa tất cả sách này? (y/n): ").strip().lower()
            if confirm == 'y':
                for book in found_books:
                    updateBookInfo(book) 
                console.print("[bold green]Sửa thông tin sách thành công.[/bold green]")
            else:
                console.print("[bold yellow]Hủy bỏ thao tác sửa.[/bold yellow]")
        elif close_matches:
            console.print(f"\n[bold red]Không tìm thấy sách với tên chính xác, nhưng có thể bạn muốn sửa sách gần giống:[/bold red]")
            for i, match in enumerate(close_matches):
                console.print(f"{i+1}. {match}")
            index = int(input(f"Nhập số thứ tự sách bạn muốn sửa (1-{len(close_matches)}): ")) - 1
            if 0 <= index < len(close_matches):
                matched_book = next(book for book in ListBooks if book['name'] == close_matches[index])
                console.print("\n[bold yellow]Kết quả tìm kiếm chính xác:[/bold yellow]")
                table = Table(title="Sách tìm thấy")
                table.add_column("STT", style="white")
                table.add_column("Tên sách", style="white")
                table.add_column("Tác giả", style="cyan")
                table.add_column("Năm xuất bản", style="green")
                table.add_column("Giá tiền", style="yellow")
                table.add_column("Số lượng", style="blue")
                for i, book in enumerate(found_books):
                    table.add_row(str(i+1), book['name'], book['author'], str(book['publicationYear']), str(book['price']), str(book['quantity']))
                console.print(table)
                confirm = input("Bạn có chắc chắn muốn sửa tất cả sách này? (y/n): ").strip().lower()
                if confirm == 'y':
                    updateBookInfo(matched_book)  
                    console.print("[bold green]Sửa thông tin sách thành công.[/bold green]")
                else:
                    console.print("[bold yellow]Hủy bỏ thao tác sửa.[/bold yellow]")
            else:
                console.print("[bold red]Lựa chọn không hợp lệ.[/bold red]")
        else:
            console.print(f"[bold red]Không tìm thấy sách với tên '{name}'.[/bold red]")
    else:
        console.print("[bold red]Lựa chọn không hợp lệ. Vui lòng nhập 1 hoặc 2.[/bold red]")

def deleteBook(ListBooks):
    console = Console()
    search_type = input("Bạn muốn tìm sách để xóa bằng mã sách (1) hay tên sách (2)? Nhập 1 hoặc 2: ").strip()
    if search_type == '1':
        id = input("Nhập mã sách cần xóa: ").strip()
        found_books = []
        for book in ListBooks:
            if book['id'] == id:
                found_books.append(book)
        if found_books:
            console.print("\n[bold yellow]Kết quả tìm kiếm chính xác:[/bold yellow]")
            table = Table(title="Sách tìm thấy")
            table.add_column("STT", style="white")
            table.add_column("Tên sách", style="white")
            table.add_column("Tác giả", style="cyan")
            table.add_column("Năm xuất bản", style="green")
            table.add_column("Giá tiền", style="yellow")
            table.add_column("Số lượng", style="blue")
            for i, book in enumerate(found_books):
                table.add_row(str(i+1), book['name'], book['author'], str(book['publicationYear']), str(book['price']), str(book['quantity']))
            console.print(table)
            confirm = input("Bạn có chắc chắn muốn xóa tất cả sách này? (y/n): ").strip().lower()
            if confirm == 'y':
                ListBooks[:] = [book for book in ListBooks if book['id'] != id] 
                console.print("[bold green]Xóa tất cả thông tin sách thành công.[/bold green]")
            else:
                console.print("[bold yellow]Hủy bỏ thao tác xóa.[/bold yellow]")
        else:
            console.print("[bold red]Không tìm thấy mã sách.[/bold red]")
    elif search_type == '2':
        name = input("Nhập tên sách cần xóa: ").strip()
        found_books = []
        close_matches = []
        for book in ListBooks:
            if re.search(name, book['name'], re.IGNORECASE):
                found_books.append(book)
        if not found_books:
            book_names = [book['name'] for book in ListBooks] 
            close_matches = difflib.get_close_matches(name, book_names, n=3, cutoff=0.6)
        if found_books:
            console.print("\n[bold yellow]Kết quả tìm kiếm chính xác:[/bold yellow]")
            table = Table(title="Sách tìm thấy")
            table.add_column("STT", style="white")
            table.add_column("Mã sách", style="white")
            table.add_column("Tác giả", style="cyan")
            table.add_column("Năm xuất bản", style="green")
            table.add_column("Giá tiền", style="yellow")
            table.add_column("Số lượng", style="blue")
            for i, book in enumerate(found_books):
                table.add_row(str(i+1), book['id'], book['author'], str(book['publicationYear']), str(book['price']), str(book['quantity']))
            console.print(table)
            confirm = input("Bạn có chắc chắn muốn xóa tất cả sách này? (y/n): ").strip().lower()
            if confirm == 'y':
                ListBooks[:] = [book for book in ListBooks if book not in found_books]  
                console.print("[bold green]Xóa toàn bộ sách thành công.[/bold green]")
            else:
                console.print("[bold yellow]Hủy bỏ thao tác xóa.[/bold yellow]")
        elif close_matches:
            console.print("\n[bold red]Không tìm thấy sách với tên chính xác, nhưng có thể bạn muốn xóa sách gần giống:[/bold red]")
            table = Table(title="Kết quả gần đúng")
            table.add_column("STT", style="white")
            table.add_column("Mã sách", style="white")
            table.add_column("Tác giả", style="cyan")
            table.add_column("Năm xuất bản", style="green")
            table.add_column("Giá tiền", style="yellow")
            table.add_column("Số lượng", style="blue")
            for i, match in enumerate(close_matches):
                for book in ListBooks:
                    if book['name'] == match:
                        table.add_row(str(i+1), book['id'], book['author'], str(book['publicationYear']), str(book['price']), str(book['quantity']))
            console.print(table)
            confirm = input("Bạn có chắc chắn muốn xóa tất cả sách này? (y/n): ").strip().lower()
            if confirm == 'y':
                ListBooks[:] = [book for book in ListBooks if book['name'] not in close_matches]  
                console.print("[bold green]Xóa toàn bộ sách gần đúng thành công.[/bold green]")
            else:
                console.print("[bold yellow]Hủy bỏ thao tác xóa.[/bold yellow]")
        else:
            console.print(f"[bold red]Không tìm thấy sách với tên '{name}'.[/bold red]")
    else:
        console.print("[bold red]Lựa chọn không hợp lệ. Vui lòng nhập 1 hoặc 2.[/bold red]")

def totalBooksQuantity(ListBooks):
    console = Console()
    quantities = np.array([book['quantity'] for book in ListBooks])
    if quantities.size == 0:
        print("Không có sách nào có số lượng.")
        return
    total_quantity = np.sum(quantities)
    console.print(f"[bold green]Tổng số lượng sách là: {total_quantity}")

def findBookPrices(ListBooks):
    csl = Console()
    if len(ListBooks) <= 0:
        csl.print("[bold red]Danh sách trống!")
        return
    else:
        prices = np.array([book['price'] for book in ListBooks])
        names = np.array([book['name'] for book in ListBooks])
        max_price = np.max(prices)
        min_price = np.min(prices)
        max_book_name = names[prices == max_price][0]
        min_book_name = names[prices == min_price][0]
        csl.print(f"[bold green]Sách {max_book_name} có giá tiền cao nhất với giá tiền là: {max_price}")
        csl.print(f"[bold green]Sách {min_book_name} có giá tiền thấp nhất với giá tiền là: {min_price}")

def findPublicationYears(ListBooks):
    console = Console()
    years = np.array([book['publicationYear'] for book in ListBooks])
    names = np.array([book['name'] for book in ListBooks])
    if years.size == 0:
        console.print("[bold red]Không có sách nào có năm xuất bản.")
        return
    max_year = np.max(years)
    min_year = np.min(years)
    min_year_book_name = names[years == min_year][0]
    max_year_book_name = names[years == max_year][0]
    console.print(f"[bold green]Sách {min_year_book_name} có năm xuất bản lâu nhất năm: {min_year}")
    console.print(f"[bold green]Sách {max_year_book_name} có năm xuất bản mới nhất năm: {max_year}")

def countAuthors(list_books):
    console = Console()
    if len(list_books) <= 0:
        console.print("[bold red]Danh sách trống!")
        return
    else:
        authors = [book['author'] for book in list_books]
        unique_authors, counts = np.unique(authors, return_counts=True)
        max_author = unique_authors[np.argmax(counts)]
        console.print(f"[bold green]Tác giả {max_author} sáng tác nhiều cuốn nhất.")

def displayBookPrices(ListBooks):
    console = Console()
    if len(ListBooks) <= 0:
        console.print("[bold red]Danh sách trống!")
        return
    prices = np.array([book['price'] for book in ListBooks])
    sorted_indices = np.argsort(prices)
    table = Table(title="Bảng giá sách sắp xếp tăng dần")
    table.add_column('Mã sách', justify="center", no_wrap=True)
    table.add_column("Tên sách")
    table.add_column("Tác giả")
    table.add_column("Năm xuất bản")
    table.add_column("Giá tiền")
    table.add_column('Số lượng')
    for idx in sorted_indices:
        book = ListBooks[idx]
        table.add_row(str(book['id']),book['name'], book['author'], str(book['publicationYear']), str(book['price']),str(book['quantity']))
    console.print(table)

def addCustomer():
    n = 0
    while True:
        try:
            n = int(input('Nhập vào số lượng khách hàng mà bạn muốn:'))
            if n <= 0:
                print("Số lượng khách hàng phải lớn hơn 0.")
                continue
            break
        except ValueError:
            print("Lỗi: Vui lòng nhập vào số dương!")
    for i in range(n):
        print(f"Nhập thông tin khách hàng thứ {i+1}:")
        while True:
            try:
                id = str(input("Nhập vào mã khách hàng:")).strip()
                if id != "":
                    if any(customer['id'] == id for customer in ListCustomers):
                        print("Mã khách hàng đã tồn tại! Vui lòng nhập mã khác.")
                    else:
                        break
                else:
                    print("Mã khách hàng không được để trống ! Vui lòng nhập lại")
            except ValueError:
                print("Lỗi không được nhập mã hợp lệ!")
        while True:
            try:
                nameCustomer = str(input("Nhập vào tên khách hàng:")).strip()
                if nameCustomer != "":
                    break
                else:
                    print('Tên khách hàng không được để trống! Vui lòng nhập lại')
            except ValueError:
                print("Lỗi: Vui lòng nhập tên hợp lệ!")
        while True:
            try:
                numPhone = str(input("Nhập vào số điện thoại khách hàng:")).strip()
                if len(str(numPhone)) == 10 :
                    if any(customer['phone'] == numPhone for customer in ListCustomers):
                        print("Số điện thoại đã tồn tại! Vui lòng nhập số điện thoại khác.")
                        continue
                    else:
                        break
                else:
                    print('Số điện thoại phải đúng quy chuẩn 10 số! Vui lòng nhập lại')
            except ValueError:
                print("Lỗi: Vui lòng nhập số điện thoại hợp lệ!")
        while True:
            try:
                email = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
                emailCustomer = str(input('Nhập vào email khách hàng:'))
                if re.match(email,emailCustomer) is not None:
                    if any(customer['email'] == emailCustomer for customer in ListCustomers):
                        print("Email khách hàng đã tồn tại! Vui lòng nhập email khác.")
                        continue
                    else:
                        break
                else:
                    print("Email khách hàng không được để trống hoặc không hợp lệ! Vui lòng nhập lại")
            except ValueError:
                print("Lỗi: Vui lòng nhập email hợp lệ!")
        while True:
            try:
                gender = str(input("Nhập giới tính khách hàng (Nam/Nữ): "))
                if gender in ['Nam', 'Nữ', 'nam', 'nữ']:
                    break
                else:
                    print("Giới tính khách hàng phải là Nam hoặc Nữ.")
            except ValueError:
                print("Lỗi: Vui lòng nhập giới tính hợp lệ!")
        while True:
            try:
                address = str(input("Nhập địa chỉ khách hàng: "))
                if address != "":
                    break
                else:
                    print("Địa chỉ khách hàng không được để trống! Vui lòng nhập lại")
            except ValueError:
                print("Lỗi: Vui lòng nhập địa chỉ hợp lệ!")
        Customers = {
            "id": id,
            "name": nameCustomer,
            "phone": numPhone,
            "email": emailCustomer,
            "gender": gender,
            "address": address,
            "total": 0.0,
            "history": [],
        }
        ListCustomers.append(Customers)

def displayCustomer():
    if len(ListCustomers) == 0:
        console = Console()
        console.print("[bold red]Danh sách khách hàng trống.[/bold red]")
        return
    table = Table(title="Danh sách khách hàng")
    table.add_column("STT", justify="center", style="white", no_wrap=True)
    table.add_column("Mã KH", style="white")
    table.add_column("Tên", style="white")
    table.add_column("Số điện thoại", style="white")
    table.add_column("Email", style="white")
    table.add_column("Giới tính", style="white")
    table.add_column("Địa chỉ", style="white")
    for i, customer in enumerate(ListCustomers):
        table.add_row(str(i+1), str(customer['id']), str(customer['name']), str(customer['phone']), str(customer['email']), str(customer['gender']), str(customer['address']))
    console = Console()
    console.print(table)

def updateCustomerInfo(customer):
    print("\nBạn muốn sửa thông tin gì?")
    print('1. Mã khách hàng')
    print("2. Tên khách hàng")
    print("3. Số điện thoại")
    print("4. Email")
    print("5. Giới tính")
    print("6. Địa chỉ")
    print("7. Sửa tất cả")

    choice = input("Nhập lựa chọn của bạn (1-6): ").strip()

    if choice == '1':
        customer['id'] = str(input("Nhập mã khách hàng mới: "))
    elif choice == '2':
        customer['name'] = str(input("Nhập tên khách hàng mới: "))
    elif choice == '3':
        customer['phone'] = str(input("Nhập số điện thoại mới: "))
    elif choice == '4':
        customer['email'] = str(input("Nhập email mới: "))
    elif choice == '5':
        customer['gender'] = str(input("Nhập giới tính mới: "))
    elif choice == '6':
        customer['address'] = str(input("Nhập địa chỉ mới: "))
    elif choice == '7':
        customer['id'] = input("Nhập mã mới: ")
        customer['name'] = input("Nhập tên mới: ")
        customer['phone'] = input("Nhập số điện thoại mới: ")
        customer['email'] = float(input("Nhập email mới: "))
        customer['gender'] = int(input("Nhập giới tính mới: "))
        customer['address'] = str(input('Nhập vào địa chỉ mới:'))
    else:
        print("Lựa chọn không hợp lệ.")

def updateCustomer(ListCustomers):
    console = Console()
    search_type = input("Bạn muốn sửa sách bằng mã (1) hay tên khách hàng (2)? Nhập 1 hoặc 2: ").strip()
    if search_type == '1':
        id = input("Nhập mã khách hàng cần sửa: ").strip()
        found_customers = [cus for cus in ListCustomers if cus['id'] == id]
        if found_customers:
            console.print("\n[bold yellow]Kết quả tìm kiếm chính xác:[/bold yellow]")
            table = Table(title="Tìm thấy khách hàng")
            table.add_column("STT", style="white")
            table.add_column("Mã khách hàng", style="white")
            table.add_column("Tên khách hàng", style="white")
            table.add_column("Số điện thoại", style="cyan")
            table.add_column("Email", style="green")
            table.add_column("Giới tính", style="yellow")
            table.add_column("Địa chỉ", style="blue")
            for i, cus in enumerate(found_customers):
                table.add_row(str(i+1),cus['id'], cus['name'], cus['phone'], str(cus['email']), str(cus['gender']), str(cus['address']))
            console.print(table)
            confirm = input("Bạn có chắc chắn muốn sửa tất cả khách hàng này? (y/n): ").strip().lower()
            if confirm == 'y':
                for cus in found_customers:
                    updateCustomerInfo(cus)  
                console.print("[bold green]Sửa thông tin khách hàng thành công.[/bold green]")
            else:
                console.print("[bold yellow]Hủy bỏ thao tác sửa.[/bold yellow]")
        else:
            console.print("[bold red]Không tìm thấy mã khách hàng.[/bold red]")
    elif search_type == '2':
        name = input("Nhập tên khách hàng cần sửa: ").strip()
        found_customers = [cus for cus in ListCustomers if re.search(name, cus['name'], re.IGNORECASE)]
        close_matches = []
        if not found_customers:
            customer_names = [cus['name'] for cus in ListCustomers]
            close_matches = difflib.get_close_matches(name, customer_names, n=3, cutoff=0.6)
        if found_customers:
            console.print("\n[bold yellow]Kết quả tìm kiếm chính xác:[/bold yellow]")
            table = Table(title="Tìm thấy khách hàng")
            table.add_column("STT", style="white")
            table.add_column("Mã khách hàng", style="white")
            table.add_column("Tên khách hàng", style="white")
            table.add_column("Số điện thoại", style="cyan")
            table.add_column("Email", style="green")
            table.add_column("Giới tính", style="yellow")
            table.add_column("Địa chỉ", style="blue")
            for i, cus in enumerate(found_customers):
                table.add_row(str(i+1), cus['id'],cus['name'], cus['phone'], str(cus['email']), str(cus['gender']), str(cus['address']))
            console.print(table)
            confirm = input("Bạn có chắc chắn muốn sửa tất cả khách hàng này? (y/n): ").strip().lower()
            if confirm == 'y':
                for cus in found_customers:
                    updateCustomerInfo(cus) 
                console.print("[bold green]Sửa thông tin khách hàng thành công.[/bold green]")
            else:
                console.print("[bold yellow]Hủy bỏ thao tác sửa.[/bold yellow]")
        elif close_matches:
            console.print(f"\n[bold red]Không tìm thấy khách hàng với tên chính xác, nhưng có thể bạn muốn sửa khách hàng gần giống:[/bold red]")
            for i, match in enumerate(close_matches):
                console.print(f"{i+1}. {match}")
            index = int(input(f"Nhập số thứ tự khách hàng bạn muốn sửa (1-{len(close_matches)}): ")) - 1
            if 0 <= index < len(close_matches):
                matched_cus = next(cus for cus in ListCustomers if cus['name'] == close_matches[index])
                console.print("\n[bold yellow]Kết quả tìm kiếm chính xác:[/bold yellow]")
                console.print("\n[bold yellow]Kết quả tìm kiếm chính xác:[/bold yellow]")
                table = Table(title="Tìm thấy khách hàng")
                table.add_column("STT", style="white")
                table.add_column("Mã khách hàng", style="white")
                table.add_column("Tên khách hàng", style="white")
                table.add_column("Số điện thoại", style="cyan")
                table.add_column("Email", style="green")
                table.add_column("Giới tính", style="yellow")
                table.add_column("Địa chỉ", style="blue")
                for i, cus in enumerate(found_customers):
                    table.add_row(str(i+1), cus['id'],cus['name'], cus['phone'], str(cus['email']), str(cus['gender']), str(cus['address']))
                console.print(table)
                confirm = input("Bạn có chắc chắn muốn sửa tất cả khách hàng này? (y/n): ").strip().lower()
                if confirm == 'y':
                    updateCustomerInfo(matched_cus)  
                    console.print("[bold green]Sửa thông tin khách hàng thành công.[/bold green]")
                else:
                    console.print("[bold yellow]Hủy bỏ thao tác sửa.[/bold yellow]")
            else:
                console.print("[bold red]Lựa chọn không hợp lệ.[/bold red]")
        else:
            console.print(f"[bold red]Không tìm thấy khách hàng với tên '{name}'.[/bold red]")
    else:
        console.print("[bold red]Lựa chọn không hợp lệ. Vui lòng nhập 1 hoặc 2.[/bold red]")

def deleteCustomer():
    console = Console()
    search_type = input("Bạn muốn tìm khách hàng để xóa bằng mã (1) hay tên khách hàng (2)? Nhập 1 hoặc 2: ").strip()
    if search_type == '1':
        id = input("Nhập mã khách hàng cần xóa: ").strip()
        found_customers = []
        for cus in ListCustomers:
            if cus['id'] == id:
                found_customers.append(cus)
        if found_customers:
            console.print("\n[bold yellow]Kết quả tìm kiếm chính xác:[/bold yellow]")
            table = Table(title="Tìm thấy khách hàng")
            table.add_column("STT", style="white")
            table.add_column("Tên khách hàng", style="white")
            table.add_column("Số điện thoại", style="cyan")
            table.add_column("Email", style="green")
            table.add_column("Giới tính", style="yellow")
            table.add_column("Địa chỉ", style="blue")
            for i, cus in enumerate(found_customers):
                table.add_row(str(i+1), cus['name'], cus['phone'], str(cus['email']), str(cus['gender']), str(cus['address']))
            console.print(table)
            confirm = input("Bạn có chắc chắn muốn xóa khách hàng này? (y/n): ").strip().lower()
            if confirm == 'y':
                ListCustomers[:] = [cus for cus in ListCustomers if cus['id'] != id] 
                console.print("[bold green]Xóa tất cả thông tin khách hàng thành công.[/bold green]")
            else:
                console.print("[bold yellow]Hủy bỏ thao tác xóa.[/bold yellow]")
        else:
            console.print("[bold red]Không tìm thấy mã khách hàng.[/bold red]")
    elif search_type == '2':
        name = input("Nhập tên khách hàng cần xóa: ").strip()
        found_customers = []
        close_matches = []
        for cus in ListCustomers:
            if re.search(name, cus['name'], re.IGNORECASE):
                found_customers.append(cus)
        if not found_customers:
            customer_names = [cus['name'] for cus in ListCustomers] 
            close_matches = difflib.get_close_matches(name, customer_names, n=3, cutoff=0.6)
        if found_customers:
            console.print("\n[bold yellow]Kết quả tìm kiếm chính xác:[/bold yellow]")
            table = Table(title="Tìm thấy khách hàng")
            table.add_column("STT", style="white")
            table.add_column("Mã khách hàng", style="white")
            table.add_column("Số điện thoại", style="cyan")
            table.add_column("Email", style="green")
            table.add_column("Giới tính", style="yellow")
            table.add_column("Địa chỉ", style="blue")
            for i, cus in enumerate(found_customers):
                table.add_row(str(i+1), cus['id'], cus['phone'], str(cus['email']), str(cus['gender']), str(cus['address']))
            console.print(table)
            confirm = input("Bạn có chắc chắn muốn xóa khách hàng này? (y/n): ").strip().lower()
            if confirm == 'y':
                ListCustomers[:] = [cus for cus in ListCustomers if cus not in found_customers]  
                console.print("[bold green]Xóa toàn bộ khách hàng thành công.[/bold green]")
            else:
                console.print("[bold yellow]Hủy bỏ thao tác xóa.[/bold yellow]")
        elif close_matches:
            console.print("\n[bold red]Không tìm thấy khách hàng với tên chính xác, nhưng có thể bạn muốn xóa khách hàng gần giống:[/bold red]")
            table = Table(title="Kết quả gần đúng")
            table.add_column("STT", style="white")
            table.add_column("Mã khách hàng", style="white")
            table.add_column("Số điện thoại", style="cyan")
            table.add_column("Email", style="green")
            table.add_column("Giới tính", style="yellow")
            table.add_column("Địa chỉ", style="blue")
            for i, match in enumerate(close_matches):
                for cus in ListCustomers:
                    if cus['name'] == match:
                        table.add_row(str(i+1), cus['id'], cus['phone'], str(cus['email']), str(cus['gender']), str(cus['address']))
            console.print(table)
            confirm = input("Bạn có chắc chắn muốn xóa khách hàng này? (y/n): ").strip().lower()
            if confirm == 'y':
                ListCustomers[:] = [cus for cus in ListCustomers if cus['name'] not in close_matches]  
                console.print("[bold green]Xóa toàn bộ khách hàng gần đúng thành công.[/bold green]")
            else:
                console.print("[bold yellow]Hủy bỏ thao tác xóa.[/bold yellow]")
        else:
            console.print(f"[bold red]Không tìm thấy khách hàng với tên '{name}'.[/bold red]")
    else:
        console.print("[bold red]Lựa chọn không hợp lệ. Vui lòng nhập 1 hoặc 2.[/bold red]")

def displayOrderHistory():
        csl = Console()
        if len(ListCustomers) == 0:
            csl.print("[bold red]Danh sách khách hàng trống.")
            return
        for customer in ListCustomers:
            csl.print(f"Lịch sử mua hàng cho khách hàng {customer['name']} (Mã: {customer['id']}):", style="bold cyan")
            if len(customer['history']) == 0:
                csl.print("Không có lịch sử mua hàng.",style="bold yellow")
            else:
                if len(customer['history']) == 1:
                    table = Table(title="Lịch sử mua hàng")
                    table.add_column("STT", style="white")
                    table.add_column("Mã sách", style="white")
                    table.add_column("Tên sách", style="white")
                    table.add_column("Tác giả", style="white")
                    table.add_column("Giá tiền", style="white")
                    table.add_column("Số lượng", style="white")
                    table.add_column("Tổng tiền", style="white")
                    for i, order in enumerate(customer['history']):
                        total = round(order['total'],2)
                        table.add_row(
                            str(i + 1),
                            str(order['book_id']),
                            order['bookName'],
                            order['author'],
                            str(order['price']),
                            str(order['quantity']),
                            str(total)
                        )
                    csl.print(table)
                else:
                    print('Không có lịch sử mua hàng')

def findCustomer(ListCustomers):
    console = Console()
    search_type = input("Bạn muốn tìm kiếm bằng mã (1) hay tên khách hàng (2)? Nhập 1 hoặc 2: ").strip()
    if search_type == '1':
        id = input("Nhập mã khách hàng cần tìm: ").strip()
        found_customers = [cus for cus in ListCustomers if cus['id'] == id]
        if found_customers:
            console.print(f"\n[bold yellow]Kết quả tìm kiếm cho mã khách hàng:[/bold yellow] [bold green]{id}[/bold green]")
            table = Table(title="Kết quả tìm kiếm")
            table.add_column("Tên khách", style="white")
            table.add_column("Số điện thoại", style="white")
            table.add_column("Email", style="white")
            table.add_column("Giới tính", style="white")
            table.add_column("Địa chỉ", style="white")
            for cus in found_customers:
                table.add_row(cus['name'], cus['phone'], str(cus['email']), str(cus['gender']), str(cus['address']))
            console.print(table)
            return found_customers[0]
        else:
            console.print("[bold red]Không tìm thấy khách hàng với mã khách hàng này.[/bold red]")
    elif search_type == '2':
        name = input("Nhập tên khách hàng cần tìm: ").strip()
        found_customers = [cus for cus in ListCustomers if re.search(name, cus['name'], re.IGNORECASE)]
        if found_customers:
            console.print(f"\n[bold yellow]Kết quả tìm kiếm cho từ khóa:[/bold yellow] [bold green]{name}[/bold green]")
            table = Table(title="Kết quả tìm kiếm")
            table.add_column("Tên khách hàng", style="white")
            table.add_column("Số điện thoại", style="white")
            table.add_column("Email", style="white")
            table.add_column("Giới tính", style="white")
            table.add_column("Địa chỉ", style="white")
            for cus in found_customers:
                table.add_row(cus['name'], cus['phone'], str(cus['email']), str(cus['gender']), str(cus['address']))
            console.print(table)
            return found_customers[0]
        else:
            customer_names = [cus['name'] for cus in ListCustomers]
            close_matches = difflib.get_close_matches(name, customer_names, n=3, cutoff=0.6)
            if close_matches:
                console.print(f"\n[bold red]Không tìm thấy khách hàng với tên:[/bold red] [bold green]{name}[/bold green], nhưng có thể bạn muốn tìm:")
                table = Table(title="Kết quả gần đúng")
                table.add_column("Tên khách hàng", style="white")
                table.add_column("Số điện thoại", style="white")
                table.add_column("Email", style="white")
                table.add_column("Giới tính", style="white")
                table.add_column("Địa chỉ", style="white")
                for match in close_matches:
                    for cus in ListCustomers:
                        if cus['name'] == match:
                            table.add_row(cus['name'], cus['phone'], str(cus['email']), str(cus['gender']), str(cus['address']))
                            break
                console.print(table)
                return found_customers[0]
            else:
                console.print(f"[bold red]Không tìm thấy khách hàng với tên '{name}'.[/bold red]")
    else:
        console.print("[bold red]Lựa chọn không hợp lệ. Vui lòng nhập 1 hoặc 2.[/bold red]")
        
def exportToExcel():
    csl = Console()
    if len(ListBooks) > 0:
        df_books = pd.DataFrame(ListBooks)
    else:
        df_books = pd.DataFrame(columns=["ID", "Name", "Author", "PublicationYear", "Price", "Quantity"])
    
    if len(ListCustomers) > 0:
        df_customers = pd.DataFrame(ListCustomers)
    else:
        df_customers = pd.DataFrame(columns=["ID", "Name", "Phone", "Email", "Gender", "Address", "Total"])
    order_data = []
    for customer in ListCustomers:
        for order in customer['history']:
            order_data.append({
                'customer_id': customer['id'],
                'customer_name': customer['name'],
                'book_id': order['book_id'],
                'book_name': order['bookName'],
                'author': order['author'],
                'price': order['price'],
                'quantity': order['quantity'],
                'total': order['total']
            })
    if len(order_data) > 0:
        df_orders = pd.DataFrame(order_data)
    else:
        df_orders = pd.DataFrame(columns=["customerId", "customerName", "bookId", "bookName", "Author", "Price", "Quantity"])
    with pd.ExcelWriter("QuanLySachOnline.xlsx", engine='openpyxl') as writer:
        df_books.to_excel(writer, sheet_name='Books', index=False)
        df_customers.to_excel(writer, sheet_name='Customers', index=False)
        df_orders.to_excel(writer, sheet_name='Orders', index=False)
    csl.print("[bold green]Ghi dữ liệu thành công ra file QuanLySachOnline.xlsx")

def sortOrderPrice():
    csl = Console()
    all_orders = []
    for customer in ListCustomers:
        if len(customer['history']) == 0:
            csl.print(f'[bold red]Khách hàng {customer["name"]} chưa có lịch sử mua hàng nào.')
        else:
            for order in customer['history']:
                order_with_customer = {
                    'customer_name': customer['name'],
                    'bookName': order['bookName'],
                    'quantity': order['quantity'],
                    'total': order['total']
                }
                all_orders.append(order_with_customer)

    all_orders.sort(key=lambda x: x['total'], reverse=False)
    table = Table(title="Sắp xếp đơn hàng có tổng tiền từ nhỏ đến lớn cho tất cả khách hàng")
    table.add_column('STT', justify='center', style='white', no_wrap=True)
    table.add_column('Tên Khách Hàng', style='white')
    table.add_column('Tên Sách', style='white')
    table.add_column('Số lượng', style='white')
    table.add_column('Tổng tiền', style='white')
    stt = 1
    for order in all_orders:
        table.add_row(str(stt), order['customer_name'], order['bookName'], str(order['quantity']), str(order['total']))
        stt += 1
    csl.print(table)

def createOrder():
    csl = Console()
    customer = findCustomer(ListCustomers)
    if customer:
        book = searchBook(ListBooks)
        if book:
            qty = int(input('Nhập vào số lượng muốn mua:'))
            if qty <= book['quantity']:
                totalPrice = qty * book['price']
                order = input(f'Tổng tiền đơn hàng {totalPrice:.2f}. Xác nhận mua(y/n)?').lower()
                if order == 'y' or order == 'Y':
                    book['quantity'] -= qty
                    Orders = {
                            
                            "book_id": book['id'],
                            "bookName": book['name'],
                            "author": book['author'],
                            "price": book['price'],
                            "publicationYear":book['publicationYear'],
                            "quantity": qty,
                            "total": totalPrice
                        }
                    customer['history'].append(Orders)
                    customer['total'] += totalPrice
                    csl.print(f"[bold green]Đơn hàng đã được thanh toán tổng số tiền là: {totalPrice:.2f}")
                else:
                    csl.print("[bold red]Hủy đơn hàng")
            else:
                csl.print("[bold yellow]Số lượng trong kho không đủ")
        else:
            csl.print("[bold red]Không tìm thấy mã sách!")
    else:
        csl.print('[bold red]Không tìm thấy mã khách hàng')

def totalRevenue():
    total = 0
    csl = Console()
    if len(ListCustomers) <= 0:
        csl.print("[bold red]Không có khách hàng nào trong danh sách!")
    else:
        for customer in ListCustomers:
            for order in customer['history']:
                total += order['total']
        csl.print(f'[bold green]Tổng doanh thu bán sách là: {total}')

def historyCustomer():
    csl = Console()
    customer = findCustomer(ListCustomers)
    if customer:
        
        if len(customer['history']) > 0:
            table = Table(title=f"Lịch sử mua hàng của khách hàng {customer['name']} có mã là: {customer['id']}")
            table.add_column("STT",justify="center",style='white',no_wrap=True)
            table.add_column("Mã Sách", style="white", no_wrap=True)
            table.add_column("Tên sách", style="white")
            table.add_column("Tác giả", style="white")
            table.add_column("Giá", style="white")
            table.add_column("Năm xuất bản", style="white")
            table.add_column("Số lượng", style="white")
            table.add_column("Tổng tiền", style="white")
            for i, order in enumerate(customer['history']):
                total = round(order['total'],2)
                table.add_row(f"{i + 1}", str(order['book_id']), order['bookName'],order['author'],str(order['price']),str(order['publicationYear']), str(order['quantity']),str(total))
            csl.print(table)
        else:
            print(f'Khách hàng {customer['name']} chưa có lịch sử mua hàng nào.')
    else:
        print("Không tìm thấy mã khách hàng.")

if __name__ == "__main__":
    while True:
        Menu()
        choice = int(input("Chọn chức năng: "))
        if choice == 0: 
            print("Thoát chương trình.")
            break
        elif choice == 1:
            addBook()
        elif choice == 2:
            displayBooks()
        elif choice == 3:
            searchBook(ListBooks)
        elif choice == 4:
            updateBook(ListBooks)
        elif choice == 5:
            deleteBook(ListBooks)   
        elif choice == 6:
            totalBooksQuantity(ListBooks)
        elif choice == 7:
            findBookPrices(ListBooks)
        elif choice == 8:
            findPublicationYears(ListBooks) 
        elif choice == 9:
            countAuthors(ListBooks)
        elif choice == 10:
            displayBookPrices(ListBooks) 
        elif choice == 11:
            addCustomer()
        elif choice == 12:
            displayCustomer()
        elif choice == 13:
            findCustomer(ListCustomers)
        elif choice == 14:
            updateCustomer(ListCustomers)
        elif choice == 15:
            deleteCustomer()
        elif choice == 16:
            createOrder()
        elif choice == 17:
            historyCustomer()
        elif choice == 18:
            displayOrderHistory()
        elif choice == 19:   
            totalRevenue()
        elif choice == 20:
            exportToExcel()
        elif choice == 21:
            sortOrderPrice()
        elif choice == 22:
            readFileJson(ListBooks,ListCustomers)
