/* 
Oh boy do i miss declarations from C++

PrintList List
Length List
Take List Count
Drop List Count
Append List1 List2
Member List Element
Position List Element

*/

proc {PrintList List}
   if {Length List} > 0 then
      {System.showInfo List.1}
      {PrintList List.2}
   end
end

fun {Factorial N}
   if N==0 then
      1
   else
      N * {Factorial N-1}
   end
end


fun {Length List}
   if List == nil then
      0
   else
      1 + {Length List.2}
   end
end


fun {Take List Count}
   if Count >= {Length List} then
      List
   elseif Count == 0 then
      nil
   else
      List.1 | {Take List.2 Count-1}
   end
end


fun {Drop List Count}
   if Count >= {Length List} then
      nil
   elseif Count == 1 then
      List.2
   else
      {Drop List.2 Count-1 }
   end
end


fun {Append List1 List2}
   if {List1 == nil } then
      List2
   elseif {Length List1} > 1 then
      List1.1 | {Append List1.2 List2}
   else
      List1.1 | List2
   end
end

   
fun {Member List Element}
   if {Length List} > 0 then
      if Element == List.1 then
	      true
      else
	      {Member List.2 Element}
      end 
   else
      false
   end
end

% Returns -1 if the element is not in the list
fun {Position List Element} C = 1 in
   if {Member List Element} then
      if Element == List.1 then
	 C
      else
	 C + {Position List.2 Element}
      end
   else
      ~1
   end
end
