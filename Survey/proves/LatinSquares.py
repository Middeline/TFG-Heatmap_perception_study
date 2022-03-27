import numpy as np

latin_squares = []

def Latin_Squares(n):

   final_prim_meitat = n + 1

   for i in range(1, n + 1):
      prim_meitat = final_prim_meitat
      while (prim_meitat <= n):
         print(prim_meitat, end=" ")
         latin_squares.append(prim_meitat)
         prim_meitat += 1

      for seg_meitat in range(1, final_prim_meitat):
         print(seg_meitat, end=" ")
         latin_squares.append(seg_meitat)

      final_prim_meitat -= 1
      print()
   print()

   return (np.array_split(latin_squares, n))


result = Latin_Squares(5)
print(latin_squares)
print("res", result)
