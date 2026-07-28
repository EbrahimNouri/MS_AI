import random
from quizen.quiz import Quiz


# ============ بانک ۱۰۰ سوالی ============
def create_question_bank():
    questions = {}

    # ===== سوالات پایه (۱۰ سوال) =====
    base_questions = {
        "خروجی دستور print(2 ** 3) چیست؟": ["5", "6", "8", "9"],
        "خروجی دستور print(10 // 3) چیست؟": ["3", "3.33", "4", "1"],
        "خروجی دستور print(10 % 3) چیست؟": ["1", "3", "0", "10"],
        "خروجی دستور print('hello' + 'world') چیست؟": [
            "helloworld",
            "hello world",
            "hello+world",
            "error",
        ],
        "خروجی دستور print('hello' * 3) چیست؟": [
            "hellohellohello",
            "hello hello hello",
            "hhheeellllllooo",
            "error",
        ],
        "کدام یک از موارد زیر یک دیکشنری معتبر است؟": [
            "{'name': 'ali', 'age': 25}",
            "['name', 'ali', 'age', 25]",
            "('name', 'ali', 'age', 25)",
            "{'name', 'ali', 'age', 25}",
        ],
        "برای دریافت ورودی از کاربر از کدام تابع استفاده می‌شود؟": [
            "input()",
            "scan()",
            "get()",
            "read()",
        ],
        "خروجی دستور len('python') چیست؟": ["6", "5", "7", "4"],
        "خروجی دستور type(3.14) چیست؟": ["float", "int", "str", "list"],
        "کدام یک از موارد زیر یک لیست معتبر است؟": [
            "[1, 2, 3]",
            "{1, 2, 3}",
            "(1, 2, 3)",
            "{'a': 1, 'b': 2}",
        ],
    }
    questions.update(base_questions)

    # ===== سوالات حلقه‌ها (۱۰ سوال) =====
    loop_questions = {
        "خروجی کد زیر چیست؟\nfor i in range(3):\n    print(i, end=' ')": [
            "0 1 2",
            "1 2 3",
            "0 1 2 3",
            "1 2",
        ],
        "خروجی کد زیر چیست؟\nfor i in range(1, 4):\n    print(i, end=' ')": [
            "1 2 3",
            "0 1 2",
            "1 2 3 4",
            "2 3 4",
        ],
        "خروجی کد زیر چیست؟\nfor i in range(0, 10, 2):\n    print(i, end=' ')": [
            "0 2 4 6 8",
            "1 3 5 7 9",
            "0 2 4 6 8 10",
            "2 4 6 8",
        ],
        "خروجی کد زیر چیست؟\nfor i in range(5, 0, -1):\n    print(i, end=' ')": [
            "5 4 3 2 1",
            "1 2 3 4 5",
            "5 4 3 2",
            "4 3 2 1",
        ],
        "خروجی کد زیر چیست؟\nfor i in 'python':\n    print(i, end='-')": [
            "p-y-t-h-o-n",
            "python",
            "p y t h o n",
            "p-y-t-h-o-n-",
        ],
        "چند بار حلقه زیر اجرا می‌شود؟\nfor i in range(5):\n    pass": [
            "5",
            "4",
            "6",
            "0",
        ],
        "خروجی کد زیر چیست؟\ns = 0\nfor i in range(1, 4):\n    s += i\nprint(s)": [
            "6",
            "3",
            "10",
            "4",
        ],
        "خروجی کد زیر چیست؟\ns = 0\nfor i in range(10):\n    if i % 2 == 0:\n        s += i\nprint(s)": [
            "20",
            "25",
            "30",
            "15",
        ],
        "خروجی کد زیر چیست؟\nfor i in range(3):\n    for j in range(2):\n        print(i, j)": [
            "6 مقدار",
            "5 مقدار",
            "4 مقدار",
            "3 مقدار",
        ],
        "کدام یک از موارد زیر برای حلقه‌های نامتناهی استفاده می‌شود؟": [
            "while True:",
            "for i in range(10):",
            "while i < 10:",
            "for i in []:",
        ],
    }
    questions.update(loop_questions)

    # ===== سوالات شرط‌ها (۱۰ سوال) =====
    condition_questions = {
        "خروجی کد زیر چیست؟\nx = 5\nif x > 3:\n    print('A')\nelse:\n    print('B')": [
            "A",
            "B",
            "AB",
            "خطا",
        ],
        "خروجی کد زیر چیست؟\nx = 2\nif x > 3:\n    print('A')\nelif x > 1:\n    print('B')\nelse:\n    print('C')": [
            "B",
            "A",
            "C",
            "BC",
        ],
        "خروجی کد زیر چیست؟\nx = 10\nif x > 5:\n    print('A')\nif x > 8:\n    print('B')\nif x > 12:\n    print('C')": [
            "A B",
            "A",
            "B",
            "A B C",
        ],
        "خروجی کد زیر چیست؟\nx = 7\nif x % 2 == 0:\n    print('Even')\nelse:\n    print('Odd')": [
            "Odd",
            "Even",
            "خطا",
            "None",
        ],
        "کدام عملگر برای بررسی برابری استفاده می‌شود؟": ["==", "=", "!=", "==="],
        "کدام عملگر برای بررسی نابرابری استفاده می‌شود؟": ["!=", "==", "<>", "!=="],
        "خروجی کد زیر چیست؟\nif True:\n    print('A')\nelse:\n    print('B')": [
            "A",
            "B",
            "AB",
            "هیچکدام",
        ],
        "خروجی کد زیر چیست؟\nif False:\n    print('A')\nelse:\n    print('B')": [
            "B",
            "A",
            "AB",
            "هیچکدام",
        ],
        "خروجی کد زیر چیست؟\nx = 0\nif x:\n    print('True')\nelse:\n    print('False')": [
            "False",
            "True",
            "خطا",
            "None",
        ],
        "خروجی کد زیر چیست؟\nx = -1\nif x:\n    print('True')\nelse:\n    print('False')": [
            "True",
            "False",
            "خطا",
            "None",
        ],
    }
    questions.update(condition_questions)

    # ===== سوالات لیست‌ها (۱۵ سوال) =====
    list_questions = {
        "خروجی کد زیر چیست؟\nmy_list = [1, 2, 3, 4]\nprint(my_list[0])": [
            "1",
            "2",
            "3",
            "4",
        ],
        "خروجی کد زیر چیست؟\nmy_list = [1, 2, 3, 4]\nprint(my_list[-1])": [
            "4",
            "1",
            "3",
            "2",
        ],
        "خروجی کد زیر چیست؟\nmy_list = [1, 2, 3, 4]\nprint(len(my_list))": [
            "4",
            "3",
            "5",
            "2",
        ],
        "خروجی کد زیر چیست؟\nmy_list = [1, 2, 3]\nmy_list.append(4)\nprint(my_list)": [
            "[1, 2, 3, 4]",
            "[1, 2, 3]",
            "[1, 2, 3, [4]]",
            "خطا",
        ],
        "خروجی کد زیر چیست؟\nmy_list = [1, 2, 3]\nmy_list.insert(1, 5)\nprint(my_list)": [
            "[1, 5, 2, 3]",
            "[1, 2, 5, 3]",
            "[5, 1, 2, 3]",
            "خطا",
        ],
        "خروجی کد زیر چیست؟\nmy_list = [1, 2, 3]\nmy_list.remove(2)\nprint(my_list)": [
            "[1, 3]",
            "[1, 2, 3]",
            "[2, 3]",
            "خطا",
        ],
        "خروجی کد زیر چیست؟\nmy_list = [1, 2, 3]\nmy_list.pop()\nprint(my_list)": [
            "[1, 2]",
            "[2, 3]",
            "[1, 3]",
            "[1, 2, 3]",
        ],
        "خروجی کد زیر چیست؟\nmy_list = [3, 1, 4, 2]\nmy_list.sort()\nprint(my_list)": [
            "[1, 2, 3, 4]",
            "[3, 1, 4, 2]",
            "[4, 3, 2, 1]",
            "خطا",
        ],
        "خروجی کد زیر چیست؟\nmy_list = [1, 2, 3, 4]\nprint(my_list[1:3])": [
            "[2, 3]",
            "[1, 2, 3]",
            "[2, 3, 4]",
            "[1, 2]",
        ],
        "خروجی کد زیر چیست؟\nmy_list = [1, 2, 3]\nmy_list.reverse()\nprint(my_list)": [
            "[3, 2, 1]",
            "[1, 2, 3]",
            "[2, 1, 3]",
            "خطا",
        ],
        "کدام متد برای اضافه کردن عنصر به انتهای لیست استفاده می‌شود؟": [
            "append()",
            "add()",
            "insert()",
            "extend()",
        ],
        "کدام متد برای حذف آخرین عنصر لیست استفاده می‌شود؟": [
            "pop()",
            "remove()",
            "delete()",
            "clear()",
        ],
        "خروجی کد زیر چیست؟\nmy_list = [1, 2, 3, 2, 4]\nprint(my_list.count(2))": [
            "2",
            "1",
            "3",
            "0",
        ],
        "خروجی کد زیر چیست؟\nmy_list = [1, 2, 3]\nmy_list.extend([4, 5])\nprint(my_list)": [
            "[1, 2, 3, 4, 5]",
            "[1, 2, 3]",
            "[1, 2, 3, [4, 5]]",
            "خطا",
        ],
        "خروجی کد زیر چیست؟\nmy_list = [1, 2, 3]\nmy_list.clear()\nprint(my_list)": [
            "[]",
            "[1, 2, 3]",
            "خطا",
            "None",
        ],
    }
    questions.update(list_questions)

    # ===== سوالات دیکشنری (۱۰ سوال) =====
    dict_questions = {
        "خروجی کد زیر چیست؟\nmy_dict = {'a': 1, 'b': 2}\nprint(my_dict['a'])": [
            "1",
            "2",
            "خطا",
            "None",
        ],
        "خروجی کد زیر چیست؟\nmy_dict = {'a': 1, 'b': 2}\nmy_dict['c'] = 3\nprint(my_dict)": [
            "{'a': 1, 'b': 2, 'c': 3}",
            "{'a': 1, 'b': 2}",
            "خطا",
            "None",
        ],
        "خروجی کد زیر چیست؟\nmy_dict = {'a': 1, 'b': 2}\ndel my_dict['a']\nprint(my_dict)": [
            "{'b': 2}",
            "{'a': 1}",
            "خطا",
            "{}",
        ],
        "خروجی کد زیر چیست؟\nmy_dict = {'a': 1, 'b': 2}\nprint(my_dict.get('c', 0))": [
            "0",
            "خطا",
            "None",
            "2",
        ],
        "خروجی کد زیر چیست؟\nmy_dict = {'a': 1, 'b': 2}\nprint(len(my_dict))": [
            "2",
            "1",
            "3",
            "0",
        ],
        "خروجی کد زیر چیست؟\nmy_dict = {'a': 1, 'b': 2}\nprint('a' in my_dict)": [
            "True",
            "False",
            "خطا",
            "None",
        ],
        "خروجی کد زیر چیست؟\nmy_dict = {'a': 1, 'b': 2}\nprint(my_dict.keys())": [
            "dict_keys(['a', 'b'])",
            "['a', 'b']",
            "{'a', 'b'}",
            "('a', 'b')",
        ],
        "خروجی کد زیر چیست؟\nmy_dict = {'a': 1, 'b': 2}\nprint(my_dict.values())": [
            "dict_values([1, 2])",
            "[1, 2]",
            "{1, 2}",
            "(1, 2)",
        ],
        "کدام یک از موارد زیر یک دیکشنری خالی است؟": ["{}", "[]", "()", "set()"],
        "خروجی کد زیر چیست؟\nmy_dict = {'a': 1, 'b': 2}\nmy_dict.update({'c': 3})\nprint(my_dict)": [
            "{'a': 1, 'b': 2, 'c': 3}",
            "{'a': 1, 'b': 2}",
            "خطا",
            "None",
        ],
    }
    questions.update(dict_questions)

    # ===== سوالات توابع (۱۵ سوال) =====
    function_questions = {
        "خروجی کد زیر چیست؟\ndef my_func():\n    return 5\nprint(my_func())": [
            "5",
            "None",
            "خطا",
            "0",
        ],
        "خروجی کد زیر چیست؟\ndef my_func(x):\n    return x * 2\nprint(my_func(3))": [
            "6",
            "3",
            "9",
            "2",
        ],
        "خروجی کد زیر چیست؟\ndef my_func(x, y):\n    return x + y\nprint(my_func(2, 3))": [
            "5",
            "6",
            "2",
            "3",
        ],
        "خروجی کد زیر چیست؟\ndef my_func(x=5):\n    return x * 2\nprint(my_func())": [
            "10",
            "5",
            "2",
            "0",
        ],
        "خروجی کد زیر چیست؟\ndef my_func(x=5):\n    return x * 2\nprint(my_func(3))": [
            "6",
            "10",
            "3",
            "2",
        ],
        "خروجی کد زیر چیست؟\ndef my_func():\n    print('Hello')\n    return\nmy_func()": [
            "Hello",
            "None",
            "خطا",
            "0",
        ],
        "خروجی کد زیر چیست؟\ndef my_func():\n    pass\nprint(my_func())": [
            "None",
            "0",
            "خطا",
            "pass",
        ],
        "خروجی کد زیر چیست؟\ndef my_func(x, y=5):\n    return x + y\nprint(my_func(3))": [
            "8",
            "3",
            "5",
            "15",
        ],
        "خروجی کد زیر چیست؟\ndef my_func(*args):\n    return sum(args)\nprint(my_func(1, 2, 3))": [
            "6",
            "3",
            "1",
            "0",
        ],
        "خروجی کد زیر چیست؟\ndef my_func(x):\n    if x > 0:\n        return 'positive'\n    elif x < 0:\n        return 'negative'\n    return 'zero'\nprint(my_func(0))": [
            "zero",
            "positive",
            "negative",
            "None",
        ],
        "خروجی کد زیر چیست؟\ndef my_func(lst):\n    return len(lst)\nprint(my_func([1, 2, 3]))": [
            "3",
            "2",
            "4",
            "1",
        ],
        "خروجی کد زیر چیست؟\ndef outer():\n    x = 5\n    def inner():\n        return x\n    return inner()\nprint(outer())": [
            "5",
            "خطا",
            "None",
            "10",
        ],
        "خروجی کد زیر چیست؟\ndef my_func(x):\n    x = 10\n    return x\nx = 5\nprint(my_func(x))": [
            "10",
            "5",
            "15",
            "خطا",
        ],
        "خروجی کد زیر چیست؟\ndef my_func(lst):\n    lst.append(4)\n    return lst\nmy_list = [1, 2, 3]\nprint(my_func(my_list))": [
            "[1, 2, 3, 4]",
            "[1, 2, 3]",
            "[4]",
            "خطا",
        ],
        "کدام کلمه کلیدی برای تعریف تابع استفاده می‌شود؟": [
            "def",
            "function",
            "define",
            "func",
        ],
    }
    questions.update(function_questions)

    # ===== سوالات پیشرفته (۱۰ سوال) =====
    advanced_questions = {
        "خروجی کد زیر چیست؟\nprint(list(range(5)))": [
            "[0, 1, 2, 3, 4]",
            "[1, 2, 3, 4, 5]",
            "[0, 1, 2, 3]",
            "range(0, 5)",
        ],
        "خروجی کد زیر چیست؟\nprint(len(range(10)))": ["10", "9", "11", "خطا"],
        "خروجی کد زیر چیست؟\nprint(sum(range(5)))": ["10", "15", "5", "0"],
        "خروجی کد زیر چیست؟\nprint(max([1, 5, 3, 9, 2]))": ["9", "5", "1", "2"],
        "خروجی کد زیر چیست؟\nprint(min([1, 5, 3, 9, 2]))": ["1", "5", "2", "9"],
        "خروجی کد زیر چیست؟\nprint(sorted([3, 1, 4, 2]))": [
            "[1, 2, 3, 4]",
            "[3, 1, 4, 2]",
            "[4, 3, 2, 1]",
            "خطا",
        ],
        "خروجی کد زیر چیست؟\nprint('hello'.upper())": ["HELLO", "Hello", "hello", "H"],
        "خروجی کد زیر چیست؟\nprint('HELLO'.lower())": ["hello", "HELLO", "Hello", "h"],
        "خروجی کد زیر چیست؟\nprint('hello world'.split())": [
            "['hello', 'world']",
            "['hello world']",
            "['h', 'e', 'l', 'l', 'o']",
            "خطا",
        ],
        "خروجی کد زیر چیست؟\nprint('-'.join(['a', 'b', 'c']))": [
            "a-b-c",
            "abc",
            "['a', 'b', 'c']",
            "a,b,c",
        ],
    }
    questions.update(advanced_questions)

    # ===== سوالات کلاس‌ها و شیءگرایی (۵ سوال) =====
    oop_questions = {
        "خروجی کد زیر چیست؟\nclass MyClass:\n    pass\nobj = MyClass()\nprint(type(obj))": [
            "<class '__main__.MyClass'>",
            "MyClass",
            "object",
            "class",
        ],
        "خروجی کد زیر چیست؟\nclass MyClass:\n    x = 5\nobj = MyClass()\nprint(obj.x)": [
            "5",
            "خطا",
            "None",
            "0",
        ],
        "خروجی کد زیر چیست؟\nclass MyClass:\n    def __init__(self, x):\n        self.x = x\nobj = MyClass(10)\nprint(obj.x)": [
            "10",
            "5",
            "خطا",
            "None",
        ],
        "برای ساخت یک شیء از یک کلاس از چه کلمه کلیدی استفاده می‌شود؟": [
            "new",
            "class",
            "create",
            "هیچکدام (فقط اسم کلاس)",
        ],
        "خروجی کد زیر چیست؟\nclass MyClass:\n    def my_method(self):\n        return 'Hello'\nobj = MyClass()\nprint(obj.my_method())": [
            "Hello",
            "خطا",
            "None",
            "0",
        ],
    }
    questions.update(oop_questions)

    # ===== سوالات Exception Handling (۵ سوال) =====
    exception_questions = {
        "خروجی کد زیر چیست؟\ntry:\n    print(10 / 0)\nexcept ZeroDivisionError:\n    print('Error')": [
            "Error",
            "خطا",
            "0",
            "None",
        ],
        "خروجی کد زیر چیست؟\ntry:\n    print(10 / 2)\nexcept:\n    print('Error')\nelse:\n    print('Success')": [
            "5",
            "Success",
            "5 Success",
            "5 Error",
        ],
        "خروجی کد زیر چیست؟\ntry:\n    print(10 / 0)\nexcept:\n    print('Error')\nfinally:\n    print('Finally')": [
            "Error",
            "Finally",
            "Error Finally",
            "خطا",
        ],
        "برای گرفتن همه استثناء‌ها از کدام کلمه کلیدی استفاده می‌شود؟": [
            "except:",
            "catch:",
            "except Exception:",
            "finally:",
        ],
        "خروجی کد زیر چیست؟\ntry:\n    print(int('abc'))\nexcept ValueError:\n    print('ValueError')\nexcept:\n    print('Error')": [
            "ValueError",
            "Error",
            "خطا",
            "None",
        ],
    }
    questions.update(exception_questions)

    return questions


# ============ برنامه اصلی با نمره‌دهی ============
def main():
    print("=" * 60)
    print("📝 آزمون جامع پایتون - ۱۰۰ سوال چهارگزینه‌ای")
    print("=" * 60)
    print()

    # دریافت تعداد سوالات از کاربر
    while True:
        try:
            num_questions = int(input("چند سوال می‌خواهید پاسخ دهید؟ (1 تا 100): "))
            if 1 <= num_questions <= 100:
                break
            else:
                print("❌ لطفاً عددی بین 1 تا 100 وارد کنید.")
        except ValueError:
            print("❌ لطفاً یک عدد معتبر وارد کنید.")

    print()

    # ایجاد بانک سوالات
    all_questions = create_question_bank()
    question_list = list(all_questions.items())

    # انتخاب تصادفی سوالات
    selected_questions = random.sample(question_list, num_questions)

    # اجرای آزمون با کتابخانه quizen
    quiz = Quiz(dict(selected_questions), player="کاربر")
    results = quiz.play()

    # نمایش نتیجه نهایی
    print("\n" + "=" * 60)
    print("📊 نتیجه نهایی آزمون:")
    print(f"تعداد سوالات: {num_questions}")
    print(f"پاسخ‌های صحیح: {results['score']}")
    print(f"پاسخ‌های غلط: {num_questions - results['score']}")
    print(f"درصد موفقیت: {(results['score'] / num_questions) * 100:.1f}%")
    print("=" * 60)

    # پیام تشویقی
    percentage = (results["score"] / num_questions) * 100
    if percentage == 100:
        print("🌟 عالی! شما استاد پایتون هستید! 🏆")
    elif percentage >= 80:
        print("👏 خیلی خوب! تسلط بالایی دارید.")
    elif percentage >= 60:
        print("👍 خوب! اما جای پیشرفت دارید.")
    elif percentage >= 40:
        print("📖 متوسط. بیشتر تمرین کنید!")
    else:
        print("💪 نیاز به مطالعه جدی‌تر دارید! ناامید نشوید.")

    print("=" * 60)


if __name__ == "__main__":
    main()
