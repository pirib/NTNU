/*
	by Piri Babayev

	The code is commented out where it was deemed necessary. To run the code, simply compile and check out the terminal for the messages!
*/

functor
import
   System
define
   
% Task 3b

/*
The following behavior is possible because of the support of the concurrency that Oz provides. In a nutshell, a thread will block usage of a variable, in this case, because not enough information is gathered, e.g. it is underfined yet and will wait until that is not so anymore. This provides extra flexibility in coding and an excellent support for concurrency in the application.
*/


% The first function as in the task description
   
fun {Min X Y}
   if X < Y then
      X
   else
      Y
   end
end

{System.showInfo 'Printing the Min between 30 and 300'}
{System.showInfo {Min 30 300}}

% Task 4a

fun {Max X Y}
   if X > Y then
      X
   else
      Y
   end
end
   
{System.showInfo 'Printing the Max between 30 and 300'}
{System.showInfo {Max 30 300}}
	 

% Task 4b 

proc {PrintGreater X Y}
   if X > Y then
      {System.showInfo X}
   else
      {System.showInfo Y}
   end
end

{System.showInfo 'Calling the proc to print out max between 50 and 500'}
{PrintGreater 50 500}

   
% Task 5
% Is this how the local was supposed to be used?

local
   A
   D
   C
   Pi=3.14
in
   proc {Circle R}
      A = Pi * R * R
      D = 2 * R
      C = Pi * D
      {System.showInfo A}
      {System.showInfo D}
      {System.showInfo C}
   end         
end

  % {Circle 3.3}
  % Cannot call the function above really, type error persist because of the Pi being not an integer.
  %  Works just fine if Pi and function argument are integers though

   
% Task 6

% For Debugging
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

{System.showInfo 'Calculating factorial of 5'#{Factorial 5}#' '}

% Task 7a
   
% Count the elements using recursion
A = [1 2 3 4 5]

fun {Length List}
   if List == nil then
      0
   else
      1 + {Length List.2}
   end
end

{System.showInfo 'Length of the List A is ' # {Length A} }

% Task 7b

fun {Take List Count}
   if Count >= {Length List} then
      List
   elseif Count == 0 then
      nil
   else
      List.1 | {Take List.2 Count-1}
   end
end

{PrintList{Take A 3}}


% Task 7c

fun {Drop List Count}
   if Count >= {Length List} then
      nil
   elseif Count == 1 then
      List.2
   else
      {Drop List.2 Count-1 }
   end
end

{PrintList {Drop A 3 } }


% Task 7d
B = [1 6]
C = [8 9]

fun {Append List1 List2}
   if {Length List1} > 1 then
      List1.1 | {Append List1.2 List2}
   else
      List1.1 | List2
   end
end

{System.showInfo 'Printing out the Merger between B and C'}
{PrintList {Append B C}}
   
   
% Task 7e
   
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

{System.showInfo 'Lets see if 7 is in the List A [1 2 3 4 5]'}
% Awkward debugging, dont judge me it is late in the night
if {Member A 7} then
   {System.showInfo 'YEP, it is in the list!'}
else
   {System.showInfo 'NOPE, not in the list!'}
end


% Task 7f

% Returns -1 if the element is not in the list
fun {Position List Element} C = 1 in
   % the task said to assume that the element is in the list, but i am a rebel 
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

{System.showInfo {Position A 6}}




end
