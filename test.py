import random

# لیست شما
my_list = [" ", "apple", "banana", " ", "cherry", " ", "date"]

# فیلتر کردن ایندکس‌هایی که رشته‌های غیرخالی دارند (بعد از حذف فاصله‌ها)
non_empty_indices = [i for i, item in enumerate(my_list) if item.strip()]

# انتخاب رندوم از ایندکس‌های غیرخالی
selected_index = random.choice(non_empty_indices)

# پرینت ایندکس و مقدار انتخاب شده
print(f"Index: {selected_index}, Selected Item: {my_list[selected_index]}")



for i in my_list:
    print(i.index(my_list))