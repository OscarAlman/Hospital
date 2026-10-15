list=[5, 2, 8, 1, 9, 3, 4, 7, 6, 0, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
min_value = min(list)
print("The minimum value in the list is:", min_value)
max_value = max(list)
print("The maximum value in the list is:", max_value)


def minMaxExtractor(list):
   largest=list[0]
   smallest=list[0]
   
   for item in list:
       if item>largest:
           largest=item
       if item<smallest:
           smallest=item
   return smallest, largest
smallest, largest = minMaxExtractor(list)
print("The minimum value in the list is:", smallest)
print("The maximum value in the list is:", largest)



mylist=[5,6,4,2,7,3,7,9,1,2,34,5]



smallest, largest = minMaxExtractor(mylist)
print("The minimum value in the list is:", smallest)
print("The maximum value in the list is:", largest)